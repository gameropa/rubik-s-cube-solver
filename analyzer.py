class CubeAnalyzer:
    # Ziel-Positionen für jede Ecke und Kante
    CORNERS = {
        ('W', 'G', 'R'): [('U', 8), ('F', 2), ('R', 0)],
        ('W', 'G', 'O'): [('U', 6), ('F', 0), ('L', 2)],
        ('W', 'B', 'R'): [('U', 2), ('B', 0), ('R', 2)],
        ('W', 'B', 'O'): [('U', 0), ('B', 2), ('L', 0)],
        ('Y', 'G', 'R'): [('D', 2), ('F', 8), ('R', 6)],
        ('Y', 'G', 'O'): [('D', 0), ('F', 6), ('L', 8)],
        ('Y', 'B', 'R'): [('D', 8), ('B', 6), ('R', 8)],
        ('Y', 'B', 'O'): [('D', 6), ('B', 8), ('L', 6)],
    }

    EDGES = {
        ('W', 'G'): [('U', 7), ('F', 1)],
        ('W', 'R'): [('U', 5), ('R', 1)],
        ('W', 'B'): [('U', 1), ('B', 1)],
        ('W', 'O'): [('U', 3), ('L', 1)],
        ('G', 'R'): [('F', 5), ('R', 3)],
        ('G', 'O'): [('F', 3), ('L', 5)],
        ('B', 'R'): [('B', 3), ('R', 5)],
        ('B', 'O'): [('B', 5), ('L', 3)],
        ('Y', 'G'): [('D', 1), ('F', 7)],
        ('Y', 'R'): [('D', 5), ('R', 7)],
        ('Y', 'B'): [('D', 7), ('B', 7)],
        ('Y', 'O'): [('D', 3), ('L', 7)],
    }

    def __init__(self, cube):
        self.cube = cube

    def get_facelet(self, face, index):
        return self.cube.state[face][index]

    def get_piece_colors(self, positions):
        return tuple(self.get_facelet(face, idx) for face, idx in positions)

    def is_edge_correct(self, colors):
        positions = self.EDGES.get(colors) or self.EDGES.get(colors[::-1])
        if not positions:
            return False
        actual = self.get_piece_colors(positions)
        return set(actual) == set(colors)

    def is_corner_correct(self, colors):
        positions = self.CORNERS.get(colors) or self.CORNERS.get(colors[::-1])
        if not positions:
            return False
        actual = self.get_piece_colors(positions)
        return set(actual) == set(colors)

    def get_phase_flags(self):
        return {
            "cross_done": all(self.is_edge_correct(colors) for colors in [('W','G'),('W','R'),('W','B'),('W','O')]),
            "f2l_done": all(self.is_edge_correct(colors) for colors in [('G','R'),('G','O'),('B','R'),('B','O')]) and
                        all(self.is_corner_correct(colors) for colors in [('W','G','R'),('W','G','O'),('W','B','R'),('W','B','O')]),
            "oll_done": all(color == 'Y' for color in self.cube.state['U']),
            "pll_done": all(all(facelet == face[0] for facelet in face) for key, face in self.cube.state.items() if key in ['F', 'R', 'B', 'L']),
            "solved": self.is_fully_solved()
        }

    def is_fully_solved(self):
        # Alle Seiten müssen einheitlich sein
        return all(all(tile == face[0] for tile in face) for face in self.cube.state.values())

    def get_wrong_edges(self):
        return [colors for colors in self.EDGES if not self.is_edge_correct(colors)]

    def get_wrong_corners(self):
        return [colors for colors in self.CORNERS if not self.is_corner_correct(colors)]
