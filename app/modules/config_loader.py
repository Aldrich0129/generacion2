"""
Módulo para cargar y validar los archivos YAML de configuración.
"""
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Clase para cargar y validar configuraciones YAML."""

    def __init__(self, config_dir: Path = None):
        """
        Inicializa el cargador de configuración.

        Args:
            config_dir: Directorio donde se encuentran los archivos YAML.
                       Si es None, usa el directorio config relativo a este archivo.
        """
        if config_dir is None:
            # Obtener el directorio del módulo actual y subir a /app, luego /config
            module_dir = Path(__file__).parent.parent
            config_dir = module_dir / "config"

        self.config_dir = Path(config_dir)

        if not self.config_dir.exists():
            raise FileNotFoundError(f"Directorio de configuración no encontrado: {self.config_dir}")

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Carga un archivo YAML.

        Args:
            filename: Nombre del archivo YAML a cargar.

        Returns:
            Diccionario con el contenido del YAML.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            yaml.YAMLError: Si hay un error al parsear el YAML.
        """
        filepath = self.config_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data is None:
                raise ValueError(f"El archivo {filename} está vacío o no es un YAML válido")

            return data

        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error al parsear {filename}: {e}")

    def load_all_configs(self) -> tuple:
        """
        Carga todas las configuraciones necesarias.

        Returns:
            Tupla con (cfg_simple, cfg_cond, cfg_tab)

        Raises:
            Exception: Si hay algún error al cargar los archivos.
        """
        try:
            cfg_simple = self.load_yaml("variables_simples.yaml")
            cfg_cond = self.load_yaml("variables_condicionales.yaml")
            cfg_tab = self.load_yaml("tablas.yaml")

            # Validar que las estructuras básicas existan
            self._validate_simple_config(cfg_simple)
            self._validate_conditions_config(cfg_cond)
            self._validate_tables_config(cfg_tab)

            return cfg_simple, cfg_cond, cfg_tab

        except Exception as e:
            raise Exception(f"Error al cargar las configuraciones: {e}")

    def _validate_simple_config(self, cfg: Dict[str, Any]):
        """Valida la estructura del YAML de variables simples."""
        if "simple_variables" not in cfg:
            raise ValueError("El YAML de variables simples debe contener 'simple_variables'")

        for var in cfg.get("simple_variables", []):
            if "id" not in var:
                raise ValueError(f"Variable sin 'id' en variables_simples.yaml: {var}")
            if "label" not in var:
                raise ValueError(f"Variable sin 'label': {var['id']}")
            if "type" not in var:
                raise ValueError(f"Variable sin 'type': {var['id']}")

    def _validate_conditions_config(self, cfg: Dict[str, Any]):
        """Valida la estructura del YAML de condiciones."""
        if "conditions" not in cfg:
            raise ValueError("El YAML de condiciones debe contener 'conditions'")

        for cond in cfg.get("conditions", []):
            if "id" not in cond:
                raise ValueError(f"Condición sin 'id' en variables_condicionales.yaml: {cond}")
            if "marker" not in cond:
                raise ValueError(f"Condición sin 'marker': {cond['id']}")
            if "word_file" not in cond:
                raise ValueError(f"Condición sin 'word_file': {cond['id']}")

    def _validate_tables_config(self, cfg: Dict[str, Any]):
        """Valida la estructura del YAML de tablas."""
        if "tables" not in cfg:
            raise ValueError("El YAML de tablas debe contener 'tables'")

        for table_id, table_cfg in cfg.get("tables", {}).items():
            if "marker" not in table_cfg and "marker_pattern" not in table_cfg:
                raise ValueError(f"Tabla sin 'marker' o 'marker_pattern': {table_id}")
            if "columns" not in table_cfg:
                raise ValueError(f"Tabla sin 'columns': {table_id}")
