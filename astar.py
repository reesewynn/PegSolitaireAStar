from solitaire import Solitaire
from collections import defaultdict
from pq import PQ
import numpy as np


been = {}
def move_path(pos, came_from):
    # skip first parent to ensure 1 move solutions work
    path = []

    curr = pos
    while curr in came_from:
        curr, move = came_from[curr]
        path.append(move)

    return path[::-1]

# TODO: Try DFS?

def astar_bfs(position, heuristic):
    # a* search
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[position] = 0

    f_score = defaultdict(lambda: float('inf'))
    f_score[position] = heuristic.evaluate(position)
    
    open_set = PQ(position, 0)
    # import pdb
    while not open_set.is_empty():
        # pdb.set_trace()
        current = open_set.pop()
        if been.get(current):
            continue
        if current.game_over() and current.winner():
            return move_path(current, came_from) # todo backtrack
        for move in current.legal_moves():
            result = current.result(move)
            if not apply_pagoda(result):
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[result]:
                came_from[result] = (current, move)
                g_score[result] = tentative_g
                f_score[result] = g_score[result] + heuristic.evaluate(result)
                if not open_set.contains(result):
                    open_set.add(result, f_score[result])
        been[current] = True
    return [] # failed to find a path

def astar_bfs_no_rot(position, heuristic):
    # a* search
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[position] = 0

    f_score = defaultdict(lambda: float('inf'))
    f_score[position] = heuristic.evaluate(position)
    
    open_set = PQ(position, 0)
    # import pdb
    while not open_set.is_empty():
        # pdb.set_trace()
        current = open_set.pop()
        if been.get(current):
            continue
        if current.game_over() and current.winner():
            return move_path(current, came_from) # todo backtrack
        for move in current.legal_moves():
            result = current.result(move, True)
            if not apply_pagoda(result):
                continue
            # if result.get_pegs_left() > 27:
            # result.recompute_hash_with_rotation()
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[result]:
                came_from[result] = (current, move)
                g_score[result] = tentative_g
                f_score[result] = g_score[result] + heuristic.evaluate(result)
                if not open_set.contains(result):
                    open_set.add(result, f_score[result])
        been[current] = True
    return [] # failed to find a path
        
STD_PAGODA_4 = np.array([[0,0,0,1,0,0,0], 
            [0,0,0,0,0,0,0],
            [-1,1,0,1,0,1,-1],
            [0,0,0,0,0,0,0],
            [-1,1,0,1,0,1,-1],
            [0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0]])
def apply_pagoda(pos):
    # import pdb;pdb.set_trace()
    return np.sum(pos.get_board() * STD_PAGODA_4) >= 0

