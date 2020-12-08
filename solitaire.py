import numpy as np
from enum import Enum
import os
# Default active board to determine use of pagoda/rotation hashing
DEFAULT_ACTIVE_BOARD = np.array([[0,0,1,1,1,0,0], 
                        [0,0,1,1,1,0,0],
                        [1,1,1,1,1,1,1],
                        [1,1,1,0,1,1,1],
                        [1,1,1,1,1,1,1],
                        [0,0,1,1,1,0,0],
                        [0,0,1,1,1,0,0]])

class Solitaire:
    DEFAULT_BOARD = "xxx,xxx,xxxxxxx,xxx.xxx,xxxxxxx,xxx,xxx"
    
    board_matrix = []
    active_board = []
    def __init__(self, board_string=None):
        ''' Creates a Solitaire board with the specified layout from the input string
            per side (plus two store pits) each containing the given.
            board_string -- a comma deliminated string of the board x=peg, .=empty
                NONE means default 32 peg board
        '''
        if board_string == None:
            board_string = self.DEFAULT_BOARD
        self.captured = 0
        
        # create board_matrix
        self.init_board(board_string)

    def init_board(self, board_string):
        rows = board_string.split(",")
        max_len = max([len(line) for line in rows])
        if not len(rows):
            raise Exception("must have at least one row")
        for line in rows:
            line_len = len(line)
            if line_len % 2 != 1 or not line:
                print(line_len)
                raise Exception("rows must be odd and non-zero")
            # add with padding
            with_pad =  [0 for i in range((max_len - line_len)//2)] + \
                        [0 if x == '.' else 1 for x in line] + \
                        [0 for i in range((max_len - line_len)//2)]
            # active marks all recorded valid board locations
            active_pad = [0 for i in range((max_len - line_len)//2)] + \
                        [1 for x in line] + \
                        [0 for i in range((max_len - line_len)//2)]

            self.board_matrix.append(with_pad)
            self.active_board.append(active_pad)

        self.board_matrix = np.array(self.board_matrix)
        self.active_board = np.array(self.active_board)

    def initial_pos(self):
        return Solitaire.Position(self.board_matrix, self.active_board)
    
    class Move(Enum):
        UP = (-1, 0)
        DOWN = (1, 0)
        LEFT = (0, -1)
        RIGHT = (0, 1)

        
    class Position:
        def __init__(self, board, valid_spots, rotation_hash=False):
            if board is None:
                raise ValueError('board cannot be None')
            if valid_spots is None:
                raise ValueError('valid spots to place cannot be None')
            if np.shape(valid_spots) != np.shape(board):
                raise ValueError('board and valid_spots must be same shape')

            self._board = np.copy(board)
            self._valid_spots = valid_spots
            self._legal_moves = self._find_legal_moves()

            self._pegs_left = np.sum(board)
            if not rotation_hash:
                self.hash = self._compute_hash()
            else:
                self.hash = self.recompute_hash_with_rotation()
            
        def get_shape(self):
            return np.shape(self._board)
        
        def get_board(self):
            return self._board
        def get_valid(self):
            return self._valid_spots
            
        
        def is_legal(self, x, y, dir):
            ''' Determines if sowing from the given move is legal from this position.

                p -- the index of a pit in this position
            '''
            dir_x, dir_y = dir.value
            adj_x, adj_y = x + dir_x, y + dir_y
            next_x, next_y = adj_x + dir_x, adj_y + dir_y

            
            shape = np.shape(self._board)
            return not ((adj_x < 0 or next_x < 0 or adj_x >= shape[0] or next_x >= shape[0]) \
                or (adj_y < 0 or next_y < 0 or adj_y >= shape[1] or next_y >= shape[1]) \
                or (not self._board[x][y] or not self._board[adj_x][adj_y]) \
                or (self._board[next_x][next_y] or not self._valid_spots[next_x][next_y]))
            

        
        def _find_legal_moves(self):
            ''' Returns a list of legal moves from this position.
                Outputs a tuple of x 
            '''
            moves = [Solitaire.Move.UP, Solitaire.Move.DOWN, Solitaire.Move.LEFT, Solitaire.Move.RIGHT]
            valid_moves = []
            # every spot with a one, try all dirs
            for row in range(np.shape(self._board)[0]):
                for slot in range(np.shape(self._board)[1]):
                    # if self._board[row][slot]:
                    for move in moves:
                        if self.is_legal(row, slot, move):
                            valid_moves.append((row, slot, move))
            return valid_moves

        def legal_moves(self):
            return self._legal_moves

        def update_moves_around(self, move):
            ''' Updates only potentially changed slots legal moves
                This should be an improvement over re-calculating every 
                time
            '''
            m_x, m_y, dir = move
            d_x, d_y = dir.value
            f_x, f_y = m_x + 2 * d_x, m_y + 2 * d_y

            lower_x = min(0, min(m_x, f_x))
            upper_x = max(np.shape(self._board)[0], max(m_x, f_x))
            lower_y = min(0, min(m_y, f_y))
            upper_y = max(np.shape(self._board)[1], max(m_y, f_y))
            moves = [Solitaire.Move.UP, Solitaire.Move.DOWN, Solitaire.Move.LEFT, Solitaire.Move.RIGHT]
            valid_moves = []

            for row in range(lower_x, upper_x):
                for col in range(lower_y, upper_y):
                    for move in moves:
                        if self.is_legal(row, col, move):
                            valid_moves.append((row, col, move))
            
            for old_move in self._legal_moves:
                if old_move[0] >= lower_x and old_move[0] <= upper_x \
                    and old_move[1] >= lower_y and old_move[1] <= upper_y:
                    continue
                valid_moves.append(old_move)
            self._legal_moves = valid_moves

        def do_move(self, move):
            ''' Updates the board with the specified move
                Returns true if successful, false otherwise
            '''
            m_x, m_y, dir = move
            d_x, d_y = dir.value
            if (not self.is_legal(m_x, m_y, dir)):
                return False
            self._board[m_x][m_y] = 0
            self._board[m_x + d_x][m_y + d_y] = 0
            self._board[m_x + d_x + d_x][m_y + d_y + d_y] = 1 
            self._pegs_left -= 1

            # update legal moves
            self.update_moves_around(move)
            # self.turn += 1
            return True
            


        def result(self, move, rotation_hash=False):
            ''' Returns a new Position object with move applied
            '''
            m_x, m_y, dir = move
            if (len(move) != 3 or not self.is_legal(m_x, m_y, dir)):
                raise ValueError("Invalid move")
            new_board = Solitaire.Position(self._board, self._valid_spots)
            
            # move is guaranteed to be valid. Do it
            new_board.do_move(move)
            return new_board

        def undo(self, move):
            m_x, m_y, dir = move
            d_x, d_y = dir.value
            
            self._board[m_x][m_y] = 1
            self._board[m_x + d_x][m_y + d_y] = 1
            self._board[m_x + d_x + d_x][m_y + d_y + d_y] = 0 
            
            

        def game_over(self):
            ''' Determines if this position is terminal -- whether the game is over having reached this position.
            '''
            return not self._legal_moves
        
        def winner(self):
            ''' Determines the winner of a game in this position, or None
                if this position is not final.  The return value is 1 if
                player 1 won, -1 if player 2 won, and 0 if the game is a draw.
            '''
            if not self.game_over():
                return None
            else:
                c_x, c_y = np.shape(self._board)[0]//2, np.shape(self._board)[1]//2
                return self._pegs_left == 1 and self._board[c_x][c_y]

        def __str__(self):
            ret = ""
            for row in range(np.shape(self._board)[0]):
                for col in range(np.shape(self._board)[1]):
                    val = " "
                    if self._valid_spots[row][col] and self._board[row][col]:
                        val = "x"
                    elif self._valid_spots[row][col]:
                        val = "o"
                    
                    ret += val + " "
                ret += "\n"
            ret += "Pegs Remaining: " + str(self._pegs_left) 
            return ret

        def get_pegs_left(self):
            return self._pegs_left
        
        def _compute_hash(self):
            return hash(self._board.tostring())

        def recompute_hash_with_rotation(self):
            # find all four hashes, pick the max. All rotations will hash the same
            h_1 = self.hash
            b_2 = np.rot90(self._board)
            h_2 = hash(b_2.tostring())
            b_3 = np.rot90(b_2)
            h_3 = hash(b_3.tostring())
            b_4 = np.rot90(b_3)
            h_4 = hash(b_4.tostring())
            return max([h_1, h_2, h_3, h_4])

        def __hash__(self):
            return self.hash

if __name__ == '__main__':
#    MAIN GAME PLAYABLE
    board = Solitaire()
    pos = board.initial_pos()
    print(pos)
    while(not pos.game_over()):
        print("What would you like to do? ('quit' or 'q' to exit)")
        x, y, dir = input("Please specify a row, col, and UP/DOWN/LEFT/RIGHT:\n").split()
        try:
            if x == "quit" or x == "q":
                break
            row = int(x)
            col = int(y)
            if dir == "UP":
                dir = Solitaire.Move.UP
            elif dir == "DOWN":
                dir = Solitaire.Move.DOWN
            elif dir == "LEFT":
                dir = Solitaire.Move.LEFT
            elif dir == "RIGHT":
                dir = Solitaire.Move.RIGHT
            
            result = pos.result((row, col, dir))
            pos = result
            os.system('clear')
            print(pos)
        except Exception:
            print("Bad move. Please try again!")
    if pos.winner():
        print("Great job! You won!")
    else:
        print("Almost there. You'll get it next time.")
    
