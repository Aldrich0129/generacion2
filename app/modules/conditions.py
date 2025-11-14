"""
Módulo para manejar condiciones (bloques condicionales).
"""
from typing import Dict, List


def get_default_conditions(cfg_cond: dict) -> dict:
    """
    Obtiene valores por defecto para condiciones (todas en "No").

    Args:
        cfg_cond: Configuración de variables_condicionales.yaml

    Returns:
        Diccionario con valores por defecto
    """
    defaults = {}

    for cond in cfg_cond.get("conditions", []):
        cond_id = cond["id"]
        defaults[cond_id] = "No"

    return defaults


def validate_conditions(cfg_cond: dict, inputs: dict) -> list:
    """
    Valida las condiciones ingresadas.

    Args:
        cfg_cond: Configuración de condiciones
        inputs: Valores ingresados

    Returns:
        Lista de errores (vacía si todo es válido)
    """
    errors = []
    valid_values = ["Sí", "No"]

    for cond in cfg_cond.get("conditions", []):
        cond_id = cond["id"]
        label = cond["label"]

        value = inputs.get(cond_id)

        if value is not None and value not in valid_values:
            errors.append(f"El valor de '{label}' debe ser 'Sí' o 'No'")

    return errors
