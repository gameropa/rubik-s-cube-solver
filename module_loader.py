def import_all_modules(config_file="config.yaml"):
    """Importiert alle Module aus der Konfiguration und gibt sie zurück."""
    import os
    import yaml
    import importlib

    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, "r") as file:
        loaded_config = yaml.safe_load(file)

    modules = {}
    for name, path in loaded_config.get("modules", {}).items():
        module = importlib.import_module(path)
        modules[name] = module
    return modules