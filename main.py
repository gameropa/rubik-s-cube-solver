from module_loader import import_all_modules

# Initialisiere dynamisch alle Module und Symbole
modules = import_all_modules()
# Nur die Symbole injizieren, nicht die Modulenamen wie 'os', 'yaml', etc.
for module in modules.values():
    for attr in dir(module):
        if not attr.startswith("_"):
            globals()[attr] = getattr(module, attr)

def main():
    import os
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    algorithm_file = os.path.join(os.path.dirname(__file__), config["files"]["algorithms"])

    cube = Cube()
    analyzer = CubeAnalyzer(cube)

    print("\U0001F9CA Initialer Zustand:")
    cube.print_state()

    print("\n\U0001F500 Mische den Würfel...")
    cube.scramble()
    cube.print_state()

    print("\n\U0001F50D Analyse nach Scramble:")
    print(analyzer.get_phase_flags())

    solver = BeginnerSolver(cube, algorithm_file)
    solver.solve()

    print("\n\U0001F3AF Analyse nach Lösung:")
    print(analyzer.get_phase_flags())

    print("\n✅ Endzustand:")
    cube.print_state()

if __name__ == "__main__":
    main()