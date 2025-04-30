import yaml
from analyzer import CubeAnalyzer

class BeginnerSolver:
    def __init__(self, cube, algorithm_file="algorithms.yaml"):
        self.cube = cube
        self.analyzer = CubeAnalyzer(cube)
        self.algorithms = self.load_algorithms(algorithm_file)

    def load_algorithms(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def parse_move(self, move):
        face = move[0]
        modifier = move[1:] if len(move) > 1 else ""
        if modifier == "'":
            return [(face, False)]
        elif modifier == "2":
            return [(face, True), (face, True)]
        return [(face, True)]

    def execute_algorithm(self, steps):
        for move in steps:
            for face, clockwise in self.parse_move(move):
                self.cube.rotate(face, clockwise)

    def log_wrong_pieces(self):
        wrong_edges = self.analyzer.get_wrong_edges()
        wrong_corners = self.analyzer.get_wrong_corners()
        print(f"❌ Falsche Kanten: {wrong_edges}")
        print(f"❌ Falsche Ecken: {wrong_corners}")

    def solve(self):
        phase_flags = self.analyzer.get_phase_flags()

        for phase in self.algorithms['beginner_method']:
            name = phase['name'].lower()
            skip = (
                ('cross' in name and phase_flags['cross_done']) or
                ('corner' in name and phase_flags['f2l_done']) or
                ('second layer' in name and phase_flags['f2l_done']) or
                ('yellow cross' in name and phase_flags['oll_done']) or
                ('orient yellow corners' in name and phase_flags['oll_done']) or
                ('position yellow corners' in name and phase_flags['pll_done']) or
                ('position yellow edges' in name and phase_flags['pll_done'] and phase_flags['oll_done'])
            )

            if skip:
                print(f"✅ Phase übersprungen: {phase['name']}")
                continue

            print(f"🔧 Löse Phase: {phase['name']}")

            if 'strategies' in phase:
                for strat in phase['strategies']:
                    print(f"📌 Strategie: {strat['description']}")
                    self.execute_algorithm(strat['steps'])
            elif 'steps' in phase:
                self.execute_algorithm(phase['steps'])

            print(f"📊 Status nach Phase '{phase['name']}':")
            self.log_wrong_pieces()
