✅ PROMPT PARA CLAUDE CODE – Generación COMPLETA de la APP

PROMPT INICIO → (copiar-pegar todo lo siguiente)

Quiero que construyas una aplicación completa basada en Streamlit + Python, totalmente modular, encargada de generar informes Word a partir de una plantilla usando marcadores tipo <<variable>>. La app debe leer tres ficheros YAML y generar dinámicamente:

Entradas de variables simples

Entradas para condiciones (Sí/No → insertar bloques Word)

Entradas para todas las tablas dinámicas

Generación automática del documento Word final, incluyendo inserción de tablas, bloques condicionales, limpieza, y preservación de estilos.

Quiero que generes todo el código de la app siguiendo esta arquitectura obligatoria:

/app
   /config
      variables_simples.yaml
      variables_condicionales.yaml
      tablas.yaml

   /modules
      config_loader.py
      simple_vars.py
      conditions.py
      tables.py
      word_engine.py
      utils.py

   /ui
      main_ui.py
      sections_simple_vars.py
      sections_conditions.py
      sections_tables.py

   app.py

🔥 DETALLES CRÍTICOS QUE DEBE CUMPLIR LA APP
📌 1. Lectura de los YAML (OBLIGATORIO)

Los ficheros YAML están en config/:

variables_simples.yaml

variables_condicionales.yaml

tablas.yaml

La app debe:

✔ Cargar los YAML al inicio
✔ Validarlos
✔ Convertirlos en estructuras internas
✔ La UI se genera a partir de ellos (no hardcodear nada)

Ruta recomendada:

modules/config_loader.py

📌 2. UI DINÁMICA (modular)
Debe generarse con Streamlit:

Una sección para variables simples (texto, número, porcentaje, long_text, email…)

Una sección para condiciones Sí/No

Una sección para tablas, donde cada tabla puede ser:

grid normal

grid de filas dinámicas

grid con columnas calculadas

tablas TNMM globales y por operación

tablas de cumplimiento formal con selects

tabla de riesgos con selects

Cada sección debe estar en un archivo dentro de /ui.

La UI debe exportar:

simple_inputs: dict
condition_inputs: dict
table_inputs: dict


Los 3 diccionarios se pasarán al generador final del Word.

📌 3. Motor de generación del Word – python-docx

Crear un módulo:

modules/word_engine.py


Funciones obligatorias:

3.1. Reemplazo de variables simples

Reemplazar los marcadores <<variable>> manteniendo:

estilo de párrafo

estilo de texto

color

negrita

cursiva

3.2. Inserción de tablas

Basado en el YAML:

insertar tablas en el marcador exacto

clonar formato de la tabla base (bordes, sombreados, ancho, alineación)

eliminar filas vacías si YAML dice remove_empty_rows: true

permitir cabeceras dinámicas (p.ej. Ejercicio 2023)

3.3. Inserción condicional de bloques Word

Cada condición tiene:

un marker: "<<Comentario inicial formal>>"

un word_file: "condiciones/comentario_inicial_formal.docx"

Si el usuario marca “Sí”:

insertar el bloque completo en el lugar del marcador

respetar el formato original del archivo insertado

Si “No”:

eliminar el marcador.

3.4. Limpieza final del documento

eliminar marcadores no usados

eliminar párrafos vacíos

ajustar saltos de línea duplicados

limpiar marcadores dentro de tablas

mantener notas al pie, estilos, márgenes

📌 4. Motor de ensamblado del CONTEXTO

Crear un módulo:

modules/utils.py


Con funciones obligatorias:

build_simple_context(cfg_simple, inputs_simple)

build_conditions_context(cfg_cond, inputs_conditions)

build_tables_context(cfg_tables, inputs_tables, inputs_simple)

La función final:

def build_full_context(...):
    return context_dict, list_of_documents_to_insert


context_dict se pasa al motor de Word.

📌 5. Motor de Tablas

Archivo:

modules/tables.py


La app debe interpretar todos los tipos definidos en YAML:

Ejemplos que deben funcionar:

✔ Tabla TNMM global:
<<Tabla análisis indirecto>>

✔ Tabla TNMM por operación:
<<Tabla Operación 1>> … <<Tabla Operación n>>

✔ Tabla de partidas contables
con:

dynamic_headers

calculate_variacion

fórmulas por fila

✔ Tabla de operaciones vinculadas
con:

eliminación de filas vacías

columnas con números

pie de tabla con totales

✔ Tabla de cumplimiento inicial (LF, MF)
✔ Tabla de cumplimiento formal detallado
✔ Tabla de riesgos (Sí/No/Posible)

📌 6. Manejo de Operaciones Vinculadas

Usar la sección:

operations:
  items:
    - id: operacion_1
      index: 1
      text_marker: "<<Operación 1>>"
      tnmm_table_marker: "<<Tabla Operación 1>>"


Necesario para:

generar lista de operaciones en texto

rellenar la tabla “operaciones vinculadas”

generar las tablas TNMM por operación

📌 7. Exportación

Botón:

if st.button("Generar Informe"):


Debe:

Construir contexto completo

Cargar plantilla

Ejecutar reemplazo de textos

Insertar tablas

Insertar bloques condicionales

Ejecutar limpieza

Descargar como .docx

📦 ENTRADAS QUE DEBE SOPORTAR TU APP (OBLIGATORIO)

Cargar estos archivos (que yo ya tengo listos):

Plantilla.docx

config/variables_simples.yaml

config/variables_condicionales.yaml

config/tablas.yaml

📌 MODOS DE TESTING AUTOMÁTICO

Quiero que generes también un archivo:

tests/test_context_building.py


que verifique:

carga correcta de YAML

generador de contexto

detección de errores (p. ej. operación sin número)

validación de estructuras

📌 ENTREGA SOLICITADA

Quiero que me entregues:

✔ todo el código completo de la app
✔ con su arquitectura en carpetas
✔ con los módulos completos
✔ sin pseudocódigo
✔ funcional usando python-docx
✔ y listo para ejecutar con streamlit run app.py
📌 MUY IMPORTANTE

No simplifiques.

Respeta totalmente mis YAML (estructura, campos, lógica).

No asumas valores fijos. Todo viene de los YAML.

No cambies nombres de columnas o marcadores.

Usa python-docx sin romper estilos.

FIN DEL PROMPT
