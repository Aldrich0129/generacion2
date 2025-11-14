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

    for var in cfg_simple.get("simple_variables", [])[:5]:  # Primeras 5 variables
        var_id = var["id"]
        label = var["label"]
        var_type = var.get("type", "text")
        marker = var.get("marker")

        # Renderizar según el tipo
        if var_type == "text":
            value = st.text_input(label, key=f"simple_{var_id}")
        elif var_type == "long_text":
            value = st.text_area(label, key=f"simple_{var_id}", height=100)
        elif var_type == "number":
            value = st.number_input(label, key=f"simple_{var_id}", format="%.2f")
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
        elif var_type == "email":
            value = st.text_input(label, key=f"simple_{var_id}", placeholder="correo@ejemplo.com")
        else:
            value = st.text_input(label, key=f"simple_{var_id}")

        inputs[var_id] = value

    # Documentación
    st.subheader("Documentación Facilitada")
    for var in cfg_simple.get("simple_variables", [])[5:9]:  # Variables de documentación
        var_id = var["id"]
        label = var["label"]

        value = st.text_input(label, key=f"simple_{var_id}")
        inputs[var_id] = value

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
