from abc import ABC, abstractmethod

class Heuristic(ABC):
    def __init__(self, init_board):
        self._board = init_board

    @abstractmethod
    def evaluate(board):
        pass
