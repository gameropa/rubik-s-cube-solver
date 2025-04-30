from global_modules import *

class Cube:
    def __init__(self):
        self.state = self.initialize_solved_state()

    def initialize_solved_state(self):
        return {
            'U': ['W'] * 9,
            'D': ['Y'] * 9,
            'F': ['G'] * 9,
            'B': ['B'] * 9,
            'L': ['O'] * 9,
            'R': ['R'] * 9
        }

    def rotate_face(self, face, clockwise=True):
        facelets = self.state[face]
        if clockwise:
            self.state[face] = [
                facelets[6], facelets[3], facelets[0],
                facelets[7], facelets[4], facelets[1],
                facelets[8], facelets[5], facelets[2],
            ]
        else:
            self.state[face] = [
                facelets[2], facelets[5], facelets[8],
                facelets[1], facelets[4], facelets[7],
                facelets[0], facelets[3], facelets[6],
            ]

    def rotate(self, face, clockwise=True):
        self.rotate_face(face, clockwise)
        adjacent = {
            'U': [('B', [2,1,0]), ('R', [2,1,0]), ('F', [2,1,0]), ('L', [2,1,0])],
            'D': [('F', [6,7,8]), ('R', [6,7,8]), ('B', [6,7,8]), ('L', [6,7,8])],
            'F': [('U', [6,7,8]), ('R', [0,3,6]), ('D', [2,1,0]), ('L', [8,5,2])],
            'B': [('U', [2,1,0]), ('L', [0,3,6]), ('D', [6,7,8]), ('R', [8,5,2])],
            'L': [('U', [0,3,6]), ('F', [0,3,6]), ('D', [0,3,6]), ('B', [8,5,2])],
            'R': [('U', [8,5,2]), ('B', [0,3,6]), ('D', [8,5,2]), ('F', [8,5,2])],
        }
        seq = adjacent[face]
        temp = [self.state[seq[i][0]][j] for i,j in enumerate(seq[0][1])]
        if clockwise:
            for i in range(4):
                for j, idx in enumerate(seq[i][1]):
                    self.state[seq[i][0]][idx] = self.state[seq[i-1][0]][seq[i-1][1][j]]
        else:
            for i in reversed(range(4)):
                for j, idx in enumerate(seq[i][1]):
                    self.state[seq[i][0]][idx] = self.state[seq[(i+1)%4][0]][seq[(i+1)%4][1][j]]
        for j, idx in enumerate(seq[(1 if clockwise else 3)][1]):
            self.state[seq[(1 if clockwise else 3)][0]][idx] = temp[j]

    def scramble(self, moves=25):
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        for _ in range(moves):
            face = random.choice(faces)
            direction = random.choice([True, False])
            self.rotate(face, clockwise=direction)

    def print_state(self):
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            print(f"{face}: {self.state[face]}")
