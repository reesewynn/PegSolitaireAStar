from solitaire import Solitaire
from heuristic import Heuristic
import numpy as np

class Manhattan(Heuristic):
    def __init__(self, init_board):
        super().__init__(init_board)
        self._dists = np.zeros(init_board.get_shape())
        c_x, c_y = np.shape(self._dists)[0] // 2, np.shape(self._dists)[1] //2
        for row in range(np.shape(self._dists)[0]):
            for col in range(np.shape(self._dists)[1]):
                self._dists[row][col] = abs(row - c_x) + abs(col - c_y)

    def evaluate(self, pos):
        return np.sum(self._dists * pos.get_board())
