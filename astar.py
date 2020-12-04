from solitaire import Solitaire
from collections import defaultdict
from pq import PQ

been = {}
def move_path(pos, came_from):
    # skip first parent to ensure 1 move solutions work
    path = []

    curr = pos
    while curr in came_from:
        curr, move = came_from[curr]
        path.append(move)

    return path[::-1]

# def astar_dfs(position):
#     if position.game_over():
#         return position.winner()
#     if been.get(position):
#         return []

#     # sort by 
#     for move in position.legal_moves():
#         down = astar_dfs(position.result(move))
#         if down:
#             down = down if isinstance(down, list) else []
#             return [move] + down
#         else:
#             position.undo(move)
#     been[position] = True
#     return []

def astar_bfs(position, heuristic):
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
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[result]:
                came_from[result] = (current, move)
                g_score[result] = tentative_g
                f_score[result] = g_score[result] + heuristic.evaluate(result)
                if not open_set.contains(result):
                    open_set.add(result, f_score[result])
        been[current] = True
    return [] # failed to find a path
        
