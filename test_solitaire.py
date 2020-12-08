if __name__ == '__main__':
    # Introduction
    print("For the final project I have implemented a solver for the game peg solitaire.")
    print("Peg solitare is a board game where a user attempts to remove pegs until only one remains in the center.")
    print("For more information, please see: https://en.wikipedia.org/wiki/Peg_solitaire")
    print("The agent below uses an A* Search (with Manhattan Distance as the heuristic) and Pagoda functions to find a solution")

    # Limitations
    print("This solver agent actually works on all centered boards that only rely on up/down/left/right jumps")
    print("One of the more interesting optimizations is through Pagoda functions. These may only be applied on a standard board layout")
    print("The canonical 33 slot traditional board works best.")

    # Usage
    print("Any board (solvable or not) may be input into the system using the following input")
    print("./Solitaire_Solver [algorithm] [board_layout]")
    print("Where mode is either --astar or --backtrack, and board layout is a board where .'s represent empty, x's are a peg, and rows are comma seperated")
    print("For example, ./Solitaire_Solver --astar ...,xx.,.xx.x.x,.xx..x.,xx...xx,.x.,...")
    print("The above command will output a solution in the form of row, col, direction for each peg that should be moved in order")
    print("For an unsolvable board, no output should be given.")

    # Results
    

    