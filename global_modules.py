def import_all_modules(config_file="config.yaml"):
    """Importiert alle Module aus der Konfiguration und injiziert ihre Symbole in den globalen Namespace."""
    import os
    import yaml
    import importlib

    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    for name, path in config.get("modules", {}).items():
        module = importlib.import_module(path)
        globals()[name] = module
        for attr in dir(module):
            if not attr.startswith("_"):
                globals()[attr] = getattr(module, attr)

if __name__ == "__main__":
    import_all_modules()
    print("Module erfolgreich importiert und in den globalen Namespace injiziert.")