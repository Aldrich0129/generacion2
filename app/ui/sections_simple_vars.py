"""
Componente UI de Streamlit para variables simples.
"""
import streamlit as st
from typing import Dict


def render_simple_vars_section(cfg_simple: dict) -> dict:
    """
    Renderiza la sección de variables simples en Streamlit.

    Args:
        cfg_simple: Configuración de variables_simples.yaml

    Returns:
        Diccionario con {id_variable: valor}
    """
    st.header("📝 Variables Simples")
    st.markdown("Completa la información general del informe.")

    inputs = {}

    # Agrupar variables por categoría (según comentarios en YAML)
    st.subheader("Datos Generales")

    # Primero renderizar ejercicio_completo para extraer los años
    ejercicio_completo_value = st.text_input(
        "Ejercicio completo (formato: 2024/2025)",
        key="simple_ejercicio_completo",
        placeholder="2024/2025",
        help="Formato: YYYY/YYYY (ej: 2024/2025). Los campos 'Ejercicio comparativo' y 'Ejercicio corto' se rellenarán automáticamente."
    )
    inputs["ejercicio_completo"] = ejercicio_completo_value

    # Extraer años del ejercicio completo
    year1, year2 = "", ""
    if ejercicio_completo_value and "/" in ejercicio_completo_value:
        try:
            years = ejercicio_completo_value.split("/")
            if len(years) == 2:
                year1 = years[0].strip()
                year2 = years[1].strip()
        except:
            pass

    # Renderizar ejercicio_corto con valor por defecto
    ejercicio_corto_value = st.text_input(
        "Ejercicio corto (abreviado, p.ej. 2025)",
        key="simple_ejercicio_corto",
        value=year2 if year2 and not st.session_state.get("ejercicio_corto_manual") else st.session_state.get("simple_ejercicio_corto", year2 or ""),
        help="Se rellena automáticamente con el segundo año del ejercicio completo, pero puedes cambiarlo"
    )
    # Detectar si el usuario cambió manualmente el valor
    if ejercicio_corto_value != year2 and year2:
        st.session_state.ejercicio_corto_manual = True
    inputs["ejercicio_corto"] = ejercicio_corto_value

    # Procesar otras variables de datos generales (excluyendo ejercicio_completo, ejercicio_corto, ejercicio_anterior)
    for var in cfg_simple.get("simple_variables", [])[:5]:  # Primeras 5 variables
        var_id = var["id"]

        # Saltar las que ya procesamos
        if var_id in ["ejercicio_completo", "ejercicio_corto"]:
            continue

        label = var["label"]
        var_type = var.get("type", "text")

        # Lógica especial para ejercicio_anterior (se procesa después de ejercicio_completo)
        if var_id == "ejercicio_anterior":
            ejercicio_anterior_value = st.text_input(
                label,
                key="simple_ejercicio_anterior",
                value=year1 if year1 and not st.session_state.get("ejercicio_anterior_manual") else st.session_state.get("simple_ejercicio_anterior", year1 or ""),
                help="Se rellena automáticamente con el primer año del ejercicio completo, pero puedes cambiarlo"
            )
            # Detectar si el usuario cambió manualmente el valor
            if ejercicio_anterior_value != year1 and year1:
                st.session_state.ejercicio_anterior_manual = True
            inputs[var_id] = ejercicio_anterior_value

        # Renderizar según el tipo normal
        elif var_type == "text":
            value = st.text_input(label, key=f"simple_{var_id}")
            inputs[var_id] = value
        elif var_type == "long_text":
            value = st.text_area(label, key=f"simple_{var_id}", height=100)
            inputs[var_id] = value
        elif var_type == "number":
            value = st.number_input(label, key=f"simple_{var_id}", format="%.2f")
            inputs[var_id] = value
        elif var_type == "percent":
            value = st.number_input(
                label,
                key=f"simple_{var_id}",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.2f",
                help="Ingrese como decimal (ej: 0.35 para 35%)"
            )
            inputs[var_id] = value
        elif var_type == "email":
            value = st.text_input(label, key=f"simple_{var_id}", placeholder="correo@ejemplo.com")
            inputs[var_id] = value
        else:
            value = st.text_input(label, key=f"simple_{var_id}")
            inputs[var_id] = value

    # Documentación - Permitir de 0 a 10 documentos
    st.subheader("Documentación Facilitada")

    # Inicializar estado de sesión para documentos
    if "num_documentos" not in st.session_state:
        st.session_state.num_documentos = 4  # Empezar con 4 documentos por defecto

    # Botones para añadir/quitar documentos
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("➕ Añadir documento"):
            if st.session_state.num_documentos < 10:
                st.session_state.num_documentos += 1
                st.rerun()

    with col2:
        if st.button("➖ Quitar último"):
            if st.session_state.num_documentos > 0:
                st.session_state.num_documentos -= 1
                st.rerun()

    # Renderizar campos de documentación dinámicamente
    for i in range(1, st.session_state.num_documentos + 1):
        doc_id = f"documentacion_{i}"
        value = st.text_input(
            f"Documentación {i}",
            key=f"simple_{doc_id}",
            placeholder=f"Documento {i}"
        )
        inputs[doc_id] = value

    # Información cuantitativa
    st.subheader("Información Cuantitativa PT")
    for var in cfg_simple.get("simple_variables", [])[9:12]:  # Variables de info PT
        var_id = var["id"]
        label = var["label"]
        var_type = var.get("type", "text")

        if var_type == "percent":
            value = st.number_input(
                label,
                key=f"simple_{var_id}",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.2f",
                help="Ingrese como decimal (ej: 0.35 para 35%)"
            )
        elif var_type == "long_text":
            value = st.text_area(label, key=f"simple_{var_id}", height=150)
        else:
            value = st.text_input(label, key=f"simple_{var_id}")

        inputs[var_id] = value

    # Datos de contacto
    st.subheader("Datos de Contacto / Firma")
    for var in cfg_simple.get("simple_variables", [])[12:]:  # Variables de contacto
        var_id = var["id"]
        label = var["label"]
        var_type = var.get("type", "text")

        if var_type == "email":
            value = st.text_input(label, key=f"simple_{var_id}", placeholder="correo@mazars.es")
        else:
            value = st.text_input(label, key=f"simple_{var_id}")

        inputs[var_id] = value

    return inputs
