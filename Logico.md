1️⃣ Supongamos esta estructura de ficheros
config/
  variables_simples.yaml
  variables_condicionales.yaml
  tablas.yaml

data/                 # aquí se guardan los datos introducidos por el usuario
  input_simple.json
  input_conditions.json
  input_tables.json


input_simple.json → respuestas a variables simples

input_conditions.json → respuestas Sí/No a condiciones

input_tables.json → datos de las tablas (listas de filas)

2️⃣ Cargar las configuraciones YAML
import yaml
from pathlib import Path

CONFIG_DIR = Path("config")

def load_yaml(name: str) -> dict:
    with open(CONFIG_DIR / name, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

cfg_simple = load_yaml("variables_simples.yaml")
cfg_cond  = load_yaml("variables_condicionales.yaml")
cfg_tab   = load_yaml("tablas.yaml")

3️⃣ Cargar los datos que vienen de la UI

Ejemplo (puedes adaptar a tu formato real):

import json
DATA_DIR = Path("data")

def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

simple_inputs     = load_json("input_simple.json")      # {id_variable: valor}
condition_inputs  = load_json("input_conditions.json")  # {id_condicion: "Sí"/"No"}
table_inputs      = load_json("input_tables.json")      # {id_tabla: [...] }


Ejemplos de contenido:

// input_simple.json
{
  "ejercicio_completo": "2023",
  "ejercicio_corto": "2023",
  "nombre_compania": "Dell Spain, S.L.",
  "actividad_principal": "Distribución mayorista de equipos informáticos",
  "ejercicio_anterior": "2022",
  "info_pt_ingresos_pct": 0.35,
  "info_pt_gastos_pct": 0.22,
  "relevancia_operaciones_texto": "Las operaciones intragrupo son relevantes...",
  "nombre_revisor": "Nombre Apellido",
  "email_revisor": "correo@mazars.es"
}

4️⃣ Construir el contexto de variables simples
def build_simple_context(cfg_simple: dict, simple_inputs: dict) -> dict:
    context = {}

    for var in cfg_simple.get("simple_variables", []):
        var_id = var["id"]
        marker = var.get("marker")  # puede ser None (ejercicio_anterior)

        value = simple_inputs.get(var_id)

        # Si no hay marcador (ejercicio_anterior) lo omitimos en plantilla,
        # pero lo podremos usar luego en tablas.
        if marker and value is not None:
            context[marker] = value

    return context

5️⃣ Construir el contexto de condiciones

Regla:

Si respuesta = “Sí” → insertaremos el contenido del Word asociado.

Si respuesta = “No” → el marcador se elimina o se sustituye por cadena vacía.

def build_conditions_context(cfg_cond: dict, condition_inputs: dict) -> dict:
    """
    Devuelve dos estructuras:
      - context_markers: { "<<Marcador>>": "" }  (para limpiar si es "No")
      - docs_to_insert:  lista de bloques {marker, filepath} para que
                         el módulo de Word copie/pegue el contenido.
    """
    context_markers = {}
    docs_to_insert = []

    for cond in cfg_cond.get("conditions", []):
        cond_id   = cond["id"]
        marker    = cond["marker"]
        word_file = cond["word_file"]

        answer = condition_inputs.get(cond_id, "No")

        if answer == "Sí":
            # En el replace de texto puedes poner un placeholder temporal
            # o dejar el marcador y luego localizarlo para insertar el bloque.
            docs_to_insert.append({
                "marker": marker,
                "file": word_file
            })
            # Si usas un motor tipo docxtpl podrías poner, por ejemplo,
            # un texto dummy que luego reemplazas por el bloque:
            context_markers[marker] = ""   # o "[[BLOCK_" + cond_id + "]]"
        else:
            # Limpieza: borrar el marcador
            context_markers[marker] = ""

    return context_markers, docs_to_insert

6️⃣ Construir el contexto de tablas

Aquí usamos tablas.yaml para saber cómo montar cada tabla a partir de table_inputs.

6.1. Ejemplo para “operaciones vinculadas”
def build_tabla_operaciones_vinculadas(cfg_tab: dict, table_inputs: dict) -> dict:
    tabla_cfg = cfg_tab["tables"]["operaciones_vinculadas"]
    marker = tabla_cfg["marker"]

    # Datos suministrados por la UI:
    # table_inputs["operaciones_vinculadas"] = [
    #   {"tipo_operacion": "...", "entidad_vinculada": "...", "ingreso_local_file": 50000, "gasto_local_file": 0},
    #   ...
    # ]
    rows = table_inputs.get("operaciones_vinculadas", [])

    # Lógica de eliminación de filas vacías según YAML
    if tabla_cfg.get("remove_empty_rows", False):
        cleaned = []
        for row in rows:
            # consideramos fila vacía si todas las columnas editables están vacías
            if any(str(row.get(col["id"], "")).strip() for col in tabla_cfg["columns"]):
                cleaned.append(row)
        rows = cleaned

    # También podemos calcular totales/pesos aquí y añadirlos como filas "footer"
    # según la especificación YAML.
    # Ejemplo simplificado: solo sumas.
    footer_totals = {}
    for col in tabla_cfg.get("footer_rows", []):
        if col["row_type"] == "sum":
            sum_row = {"_label": col["label"]}
            for col_id in col["sum_columns"]:
                sum_row[col_id] = sum(row.get(col_id, 0) or 0 for row in rows)
            footer_totals[col["id"]] = sum_row

    # El objeto resultante se lo pasas a tu módulo que pinta tablas en Word
    return {marker: {"rows": rows, "footers": footer_totals}}

6.2. Ejemplo para partidas contables
def build_tabla_partidas_contables(cfg_tab: dict, table_inputs: dict, simple_inputs: dict) -> dict:
    tabla_cfg = cfg_tab["tables"]["partidas_contables"]
    marker = tabla_cfg["marker"]

    ejercicio_actual   = simple_inputs["ejercicio_completo"]
    ejercicio_anterior = simple_inputs["ejercicio_anterior"]

    # Datos que vienen de la UI para las filas manuales (cifras):
    # table_inputs["partidas_contables"] = {
    #   "cifra_negocios": {"ejercicio_actual": 70000000, "ejercicio_anterior": 65000000},
    #   ...
    # }
    data = table_inputs.get("partidas_contables", {})

    rows_out = []

    for row_cfg in tabla_cfg["rows"]:
        rid   = row_cfg["id"]
        label = row_cfg["label"]
        mode  = row_cfg.get("input_mode", "manual")

        base = {"partida": label}

        if mode == "manual":
            vals = data.get(rid, {})
            ea = vals.get("ejercicio_actual")
            ep = vals.get("ejercicio_anterior")
        else:
            # calculadas: usamos fórmulas definidas en YAML
            # ojo: aquí simplificado; en producción evalúas la fórmula con
            # acceso al resto de filas ya calculadas
            vals = data.get(rid, {})
            ea = vals.get("ejercicio_actual")
            ep = vals.get("ejercicio_anterior")

        base["ejercicio_actual"] = ea
        base["ejercicio_anterior"] = ep

        if row_cfg.get("calculate_variacion", False) and ea is not None and ep:
            base["variacion"] = (ea - ep) / ep
        else:
            base["variacion"] = None

        rows_out.append(base)

    return {marker: {"headers": {
                        "ejercicio_actual": ejercicio_actual,
                        "ejercicio_anterior": ejercicio_anterior
                     },
                     "rows": rows_out}}

6.3. Cumplimiento formal y riesgos

Son aún más sencillas: solo hay que mapear las respuestas tipo “Sí/No/Ver comentario” o “Sí/No/Posible” a cada fila:

def build_tablas_cumplimiento_y_riesgos(cfg_tab: dict, table_inputs: dict) -> dict:
    result = {}

    for key in ["cumplimiento_inicial_LF", "cumplimiento_inicial_MF",
                "cumplimiento_formal_LF", "cumplimiento_formal_MF",
                "riesgos_pt"]:
        tabla_cfg = cfg_tab["tables"][key]
        marker    = tabla_cfg["marker"]
        rows      = table_inputs.get(key, [])

        result[marker] = {"rows": rows}

    return result

7️⃣ Montar el contexto global para la plantilla
def build_full_context(cfg_simple, cfg_cond, cfg_tab,
                       simple_inputs, condition_inputs, table_inputs):
    context = {}

    # 1. Variables simples
    context.update(build_simple_context(cfg_simple, simple_inputs))

    # 2. Condiciones (marcadores + lista de docs)
    cond_markers, docs_to_insert = build_conditions_context(cfg_cond, condition_inputs)
    context.update(cond_markers)

    # 3. Tablas
    context.update(build_tabla_operaciones_vinculadas(cfg_tab, table_inputs))
    context.update(build_tabla_partidas_contables(cfg_tab, table_inputs, simple_inputs))
    context.update(build_tablas_cumplimiento_y_riesgos(cfg_tab, table_inputs))

    # 4. Devolver contexto + info extra para el motor de Word
    return context, docs_to_insert


context te queda algo así:

{
  "<<Ejercicio completo>>": "2023",
  "<<Nombre de la Compañía>>": "Dell Spain, S.L.",
  "<<Comentario inicial formal>>": "",
  "<<Tabla operaciones vinculadas>>": {
      "rows": [ ... ],
      "footers": { ... }
  },
  "<<Tabla partidas contables>>": {
      "headers": {...},
      "rows": [...]
  },
  "<<Tabla de riesgos>>": {
      "rows": [...]
  },
  ...
}


Y docs_to_insert es una lista con los bloques condicionales a copiar/pegar en la fase de manipulación de python-docx (buscando el marcador y sustituyéndolo por el contenido del archivo asociado).
