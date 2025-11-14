"""
Componente UI de Streamlit para condiciones (bloques condicionales).
"""
import streamlit as st
from typing import Dict


def render_conditions_section(cfg_cond: dict) -> dict:
    """
    Renderiza la sección de condiciones en Streamlit.

    Args:
        cfg_cond: Configuración de variables_condicionales.yaml

    Returns:
        Diccionario con {id_condicion: "Sí"/"No"}
    """
    st.header("🔀 Bloques Condicionales")
    st.markdown(
        "Selecciona qué bloques de comentarios incluir en el informe. "
        "Si seleccionas 'Sí', se insertará el contenido del archivo Word correspondiente."
    )

    inputs = {}

    conditions = cfg_cond.get("conditions", [])

    # Mostrar en columnas para mejor visualización
    for i, cond in enumerate(conditions):
        cond_id = cond["id"]
        label = cond["label"]
        question = cond.get("question", f"¿Incluir {label}?")

        # Usar radio buttons para Sí/No
        value = st.radio(
            question,
            options=["No", "Sí"],
            key=f"cond_{cond_id}",
            horizontal=True,
            help=f"Archivo: {cond.get('word_file', 'N/A')}"
        )

        inputs[cond_id] = value

        # Añadir separador cada 3 condiciones
        if (i + 1) % 3 == 0 and i < len(conditions) - 1:
            st.divider()

    return inputs
