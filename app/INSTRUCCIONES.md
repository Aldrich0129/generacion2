# 📘 Instrucciones de Uso Detalladas

## Instalación y Configuración

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalación de Dependencias

```bash
cd /home/user/generacion2/app
pip install -r requirements.txt
```

### 3. Verificar Estructura de Archivos

Asegúrate de tener la siguiente estructura:

```
/app
├── config/
│   ├── variables_simples.yaml
│   ├── variables_condicionales.yaml
│   ├── tablas.yaml
│   └── Plantilla.docx
├── condiciones/
│   ├── comentario_inicial_formal.docx
│   ├── desarrollo_comentario_formal.docx
│   └── ... (otros archivos condicionales)
├── modules/
├── ui/
└── app.py
```

## Ejecución de la Aplicación

### Método 1: Streamlit Run

```bash
cd /home/user/generacion2/app
streamlit run app.py
```

### Método 2: Python Module

```bash
python -m streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Flujo de Trabajo

### Paso 1: Variables Simples

1. Navega a la pestaña "📝 Variables Simples"
2. Completa todos los campos requeridos:
   - **Datos Generales:** Ejercicio, nombre de compañía, actividad
   - **Documentación Facilitada:** Lista de documentos
   - **Información Cuantitativa:** Porcentajes de ingresos/gastos vinculados
   - **Datos de Contacto:** Nombre y email del revisor

**Tipos de datos soportados:**
- `text`: Texto corto
- `long_text`: Texto largo (textarea)
- `number`: Números con decimales
- `percent`: Porcentajes (ingresar como decimal, ej: 0.35 para 35%)
- `email`: Dirección de correo electrónico

### Paso 2: Bloques Condicionales

1. Navega a la pestaña "🔀 Condiciones"
2. Para cada bloque, selecciona "Sí" o "No":
   - **Sí**: Se insertará el contenido del archivo Word correspondiente
   - **No**: El marcador se eliminará del documento final

**Bloques disponibles:**
- Comentario inicial formal
- Desarrollo comentario formal
- Desarrollo documentación contemporánea
- Documentación en otro idioma
- Comentarios sobre servicios intragrupo
- Comentarios sobre falta de análisis
- Comentarios sobre análisis desactualizados
- Comentarios sobre independencia de superiores
- Comentarios sobre errores en filtros
- Comentarios sobre métodos de valoración
- Comentarios sobre pérdidas
- Desarrollo de discrepancias formales

### Paso 3: Tablas

1. Navega a la pestaña "📊 Tablas"
2. Completa cada tabla según se requiera:

#### 3.1. Análisis Indirecto Global (TNMM)
- Ingresa los valores estadísticos: Min, LQ, Med, UQ, Max
- Valores en porcentaje (0-100)

#### 3.2. Operaciones Vinculadas
- Haz clic en "➕ Añadir operación" para agregar filas
- Para cada operación:
  - **Tipo de operación**: Ej: "Servicios de soporte"
  - **Entidad vinculada**: Ej: "Dell Technologies Inc."
  - **Ingreso**: Importe en EUR
  - **Gasto**: Importe en EUR
- Los totales se calculan automáticamente

#### 3.3. Análisis TNMM por Operación
- Se genera automáticamente una sección por cada operación vinculada
- Completa los rangos estadísticos para cada operación

#### 3.4. Partidas Contables
- Completa las cifras para el ejercicio actual y anterior
- Los márgenes (OM, NCP) se calculan automáticamente
- La variación porcentual se calcula automáticamente

#### 3.5. Cumplimiento Formal
- **Inicial (LF y MF)**: Resumen de cumplimiento por sección
- **Detallado (LF y MF)**: Análisis detallado de cada requisito
- Opciones: "Sí", "No", "Ver comentario"
- Si seleccionas "Ver comentario", aparecerá un campo de texto

#### 3.6. Tabla de Riesgos
- Para cada elemento de riesgo, completa:
  - **Impacto**: Sí/No/Posible
  - **Nivel Preliminar**: Sí/No/Posible
  - **Mitigadores**: Descripción de las medidas
  - **Nivel Final**: Sí/No/Posible

### Paso 4: Generar Informe

1. Haz clic en el botón "📄 Generar Informe Word"
2. El sistema validará todas las entradas
3. Si hay errores, se mostrarán en pantalla
4. Si todo es correcto:
   - Se generará el documento
   - Aparecerá un mensaje de éxito
   - Se mostrará un botón de descarga

### Paso 5: Descargar

1. Haz clic en "📥 Descargar Informe"
2. El archivo se descargará con el nombre:
   `Informe_PT_[Nombre_Empresa]_[Ejercicio].docx`

## Personalización de la Aplicación

### Modificar Variables Simples

Edita `config/variables_simples.yaml`:

```yaml
simple_variables:
  - id: mi_variable
    label: "Mi Variable Personalizada"
    marker: "<<Mi Variable>>"
    type: "text"
```

### Añadir Condiciones

Edita `config/variables_condicionales.yaml`:

```yaml
conditions:
  - id: mi_condicion
    label: "Mi Condición"
    marker: "<<Mi Condición>>"
    question: "¿Incluir mi condición?"
    word_file: "condiciones/mi_condicion.docx"
```

### Configurar Tablas

Edita `config/tablas.yaml`. Ver ejemplos existentes para la estructura.

### Modificar Plantilla

1. Abre `config/Plantilla.docx` en Word
2. Añade marcadores en el formato: `<<Nombre del Marcador>>`
3. Mantén el formato deseado (estilos, colores, negrita, etc.)
4. Guarda el archivo

## Solución de Problemas

### La aplicación no inicia

```bash
# Verifica la instalación de dependencias
pip install -r requirements.txt --upgrade

# Verifica la versión de Python
python --version  # Debe ser 3.8+
```

### Error: "Plantilla no encontrada"

- Verifica que `Plantilla.docx` esté en `/app/config/`
- Verifica los permisos del archivo

### Error: "Archivo condicional no encontrado"

- Verifica que los archivos .docx estén en `/app/condiciones/`
- Verifica que los nombres coincidan exactamente con el YAML

### Las tablas no se insertan

- Verifica que los marcadores en la plantilla coincidan exactamente
- Los marcadores son **case-sensitive**
- Formato correcto: `<<Nombre Exacto>>`

### Los estilos se pierden

- El motor preserva estilos de párrafo y texto
- Para mejores resultados, usa estilos de Word consistentes
- Evita formato manual excesivo

## Características Avanzadas

### Cálculos Automáticos

Las siguientes métricas se calculan automáticamente:

- **Variación porcentual**: Entre ejercicios
- **Operating Margin (OM)**: EBIT / Cifra de negocios
- **Net Cost Plus (NCP)**: EBIT / Total costes operativos
- **Totales de operaciones vinculadas**: Suma de ingresos/gastos

### Validaciones

La aplicación valida automáticamente:

- Campos requeridos
- Formato de emails
- Tipos de datos numéricos
- Rangos de porcentajes (0-1)

### Estado de Sesión

- La aplicación mantiene el estado mientras está abierta
- Los datos no se guardan automáticamente
- Genera el informe antes de cerrar el navegador

## Consejos de Uso

1. **Completa en orden**: Variables → Condiciones → Tablas
2. **Revisa antes de generar**: Verifica todos los datos
3. **Guarda versiones**: Descarga múltiples versiones si necesitas iterar
4. **Usa nombres descriptivos**: Para las operaciones vinculadas
5. **Consistencia**: Usa el mismo ejercicio en todas las secciones

## Soporte

Para problemas técnicos o preguntas:

1. Revisa el archivo `README.md`
2. Verifica los logs de Streamlit en la terminal
3. Revisa la consola del navegador (F12) para errores JavaScript

## Actualizaciones Futuras

Características planeadas:

- [ ] Guardar/cargar borradores
- [ ] Exportar a PDF
- [ ] Plantillas múltiples
- [ ] Importar datos desde Excel
- [ ] Historial de informes generados
