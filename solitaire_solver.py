from solitaire import Solitaire
from manhattan import Manhattan
from astar import astar_bfs, astar_bfs_no_rot
import pdb
from sys import argv

been = {}

def backtrack(position):
    # pdb.set_trace()
    if position.game_over():
        return position.winner()
    if been.get(position):
        return []
    for move in position.legal_moves():
        down = backtrack(position.result(move))
        if down:
            down = down if isinstance(down, list) else []
            return [move] + down
        # else:
        #     position.undo(move)
    been[position] = True
    return []

def astar(position, no_rotation):
    # build heuristic
    h = Manhattan(position)
    if no_rotation:
        return astar_bfs_no_rot(position, h)
    return astar_bfs(position, h)


if __name__ == '__main__':
    test_str = ".xx,x.x,.....x.,..xxxxx,....x.x,.x.,xx."
    # test_str = ".xx,x.x,....x..,..xx.x.,.......,.xx,x."
    test_str = "...,xx.,.xx.x.x,.xx..x.,xx...xx,.x.,..."
    # test_str = ".xx,x.x,.....x.,..xxxxx,....x.x,.x.,xx."
    if (len(argv) < 2):
        print("Usage ./solitaire_solver [mode]")
        exit(1)
    mode = argv[1]
    no_rotation = False
    board_ind = 2
    if len(argv) > 2 and argv[2] == "--no_rotation":
        no_rotation = True
        board_ind += 1
    elif len(argv) > 2:
        test_str = argv[board_ind]
    
    if no_rotation and len(argv) > 3:
        test_str = argv[board_ind]
    
    #build board to test
    board = Solitaire(test_str)
    pos = board.initial_pos()

    if mode == '--backtrack':
        path = backtrack(pos)
    else:
        path = astar(pos, no_rotation)
    if path:
        for row in path:
            print(row)
    
