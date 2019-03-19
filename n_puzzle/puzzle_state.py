import numpy as np
from enum import Enum
import copy


# Enum of operation in EightPuzzle problem
class Move(Enum):
    """
    The class of move operation
    NOTICE: The direction denotes the 'blank' space move
    """
    Up = 0
    Down = 1
    Left = 2
    Right = 3


# EightPuzzle state
class PuzzleState(object):
    """
    Class for state in EightPuzzle-Problem
    Attr:
        square_size: Chessboard size, e.g: In 8-puzzle problem, square_size = 3
        state: 'square_size' x 'square_size square', '-1' indicates the 'blank' block  (For 8-puzzle, state is a 3 x 3 array)
        g: The cost from initial state to current state
        h: The value of heuristic function
        pre_move:  The previous operation to get to current state
        pre_state: Parent state of this state
    """
    def __init__(self, square_size = 3):
        self.square_size = square_size
        self.state = None
        self.g = 0
        self.h = 0
        self.pre_move = None
        self.pre_state = None

        self.generate_state()

    def __eq__(self, other):
        return (self.state == other.state).all()

    def blank_pos(self):
        """
        Find the 'blank' position of current state
        :return:
            row: 'blank' row index, '-1' indicates the current state may be invalid
            col: 'blank' col index, '-1' indicates the current state may be invalid
        """
        index = np.argwhere(self.state == -1)
        row = -1
        col = -1
        if index.shape[0] == 1:  # find blank
            row = index[0][0]
            col = index[0][1]
        return row, col

    def num_pos(self, num):
        """
        Find the 'num' position of current state
        :return:
            row: 'num' row index, '-1' indicates the current state may be invalid
            col: 'num' col index, '-1' indicates the current state may be invalid
        """
        index = np.argwhere(self.state == num)
        row = -1
        col = -1
        if index.shape[0] == 1:  # find number
            row = index[0][0]
            col = index[0][1]
        return row, col

    def is_valid(self):
        """
        Check current state is valid or not (A valid state should have only one 'blank')
        :return:
            flag: boolean, True - valid state, False - invalid state
        """
        row, col = self.blank_pos()
        if row == -1 or col == -1:
            return False
        else:
            return True

    def clone(self):
        """
        Return the state's deepcopy
        :return:
        """
        return copy.deepcopy(self)

    def generate_state(self, random=False, seed=None):
        """
        Generate a new state
        :param random: True - generate state randomly, False - generate a normal state
        :param seed: Choose the seed of random, only used when random = True
        :return:
        """
        self.state = np.arange(0, self.square_size ** 2).reshape(self.square_size, -1)
        self.state[self.state == 0] = -1  # Set blank

        if random:
            np.random.seed(seed)
            np.random.shuffle(self.state)

    def display(self):
        """
        Print state
        :return:
        """
        print("----------------------")
        for i in range(self.state.shape[0]):
            # print("{}\t{}\t{}\t".format(self.state[i][0], self.state[i][1], self.state[i][2]))
            # print(self.state[i, :])
            for j in range(self.state.shape[1]):
                if j == self.state.shape[1] - 1:
                    print("{}\t".format(self.state[i][j]))
                else:
                    print("{}\t".format(self.state[i][j]), end='')
        print("----------------------\n")


def check_move(curr_state, move):
    """
    Check the operation 'move' can be performed on current state 'curr_state'
    :param curr_state: Current puzzle state
    :param move: Operation to be performed
    :return:
        valid_op: boolean, True - move is valid; False - move is invalid
        src_row: int, current blank row index
        src_col: int, current blank col index
        dst_row: int, future blank row index after move
        dst_col: int, future blank col index after move
    """
    # assert isinstance(move, Move)  # Check operation type
    assert curr_state.is_valid()

    if not isinstance(move, Move):
        move = Move(move)

    src_row, src_col = curr_state.blank_pos()
    dst_row, dst_col = src_row, src_col
    valid_op = False

    if move == Move.Up:  # Number moves up, blank moves down
        dst_row -= 1
    elif move == Move.Down:
        dst_row += 1
    elif move == Move.Left:
        dst_col -= 1
    elif move == Move.Right:
        dst_col += 1
    else:  # Invalid operation
        dst_row = -1
        dst_col = -1

    if dst_row < 0 or dst_row > curr_state.state.shape[0] - 1 or dst_col < 0 or dst_col > curr_state.state.shape[1] - 1:
        valid_op = False
    else:
        valid_op = True

    return valid_op, src_row, src_col, dst_row, dst_col


def once_move(curr_state, move):
    """
    Perform once move to current state
    :param curr_state:
    :param move:
    :return:
        valid_op: boolean, flag of this move is valid or not. True - valid move, False - invalid move
        next_state: EightPuzzleState, state after this move
    """
    valid_op, src_row, src_col, dst_row, dst_col = check_move(curr_state, move)

    next_state = curr_state.clone()

    if valid_op:
        it = next_state.state[dst_row][dst_col]
        next_state.state[dst_row][dst_col] = -1
        next_state.state[src_row][src_col] = it
        next_state.pre_state = curr_state
        next_state.pre_move = move
        return True, next_state
    else:
        return False, next_state


def check_state(src_state, dst_state):
    """
    Check current state is same as destination state
    :param src_state:
    :param dst_state:
    :return:
    """
    return (src_state.state == dst_state.state).all()


def run_moves(curr_state, dst_state, moves):
    """
    Perform list of move to current state, and check the final state is same as destination state or not
    Ideally, after we perform moves to current state, we will get a state same as the 'dst_state'
    :param curr_state: EightPuzzleState, current state
    :param dst_state: EightPuzzleState, destination state
    :param moves: List of Move
    :return:
        flag of moves: True - We can get 'dst_state' from 'curr_state' by 'moves'
    """
    pre_state = curr_state.clone()
    next_state = None

    for move in moves:
        valid_move, next_state = once_move(pre_state, move)

        if not valid_move:
            return False

        pre_state = next_state.clone()

    if check_state(next_state, dst_state):
        return True
    else:
        return False


def runs(curr_state, moves):
    """
    Perform list of move to current state, get the result state
    NOTICE: The invalid move operation would be ignored
    :param curr_state:
    :param moves:
    :return:
    """
    pre_state = curr_state.clone()
    next_state = None

    for move in moves:
        valid_move, next_state = once_move(pre_state, move)
        pre_state = next_state.clone()
    return next_state


def print_moves(init_state, moves):
    """
    While performing the list of move to current state, this function will also print how each move is performed
    :param init_state: The initial state
    :param moves: List of move
    :return:
    """
    print("Initial state")
    init_state.display()

    pre_state = init_state.clone()
    next_state = None

    for idx, move in enumerate(moves):
        if move == Move.Up:  # Number moves up, blank moves down
            print("{} th move. Goes up.".format(idx))
        elif move == Move.Down:
            print("{} th move. Goes down.".format(idx))
        elif move == Move.Left:
            print("{} th move. Goes left.".format(idx))
        elif move == Move.Right:
            print("{} th move. Goes right.".format(idx))
        else:  # Invalid operation
            print("{} th move. Invalid move: {}".format(idx, move))

        valid_move, next_state = once_move(pre_state, move)

        if not valid_move:
            print("Invalid move: {}, ignore".format(move))

        next_state.display()

        pre_state = next_state.clone()

    print("We get final state: ")
    next_state.display()


def generate_moves(move_num = 30):
    """
    Generate a list of move in a determined length randomly
    :param move_num:
    :return:
        move_list: list of move
    """
    move_dict = {}
    move_dict[0] = Move.Up
    move_dict[1] = Move.Down
    move_dict[2] = Move.Left
    move_dict[3] = Move.Right

    index_arr = np.random.randint(0, 4, move_num)
    index_list = list(index_arr)

    move_list = [move_dict[idx] for idx in index_list]

    return move_list


def convert_moves(moves):
    """
    Convert moves from int into Move type
    :param moves:
    :return:
    """
    if len(moves):
        if isinstance(moves[0], Move):
            return moves
        else:
            return [Move(move) for move in moves]
    else:
        return moves


"""
NOTICE:
1. init_state is a 3x3 numpy array, the "space" is indicated as -1, for example
    1 2 -1              1 2
    3 4 5   stands for  3 4 5
    6 7 8               6 7 8
2. moves contains directions that transform initial state to final state. Here
    0 stands for up
    1 stands for down
    2 stands for left
    3 stands for right
    We 
   There might be several ways to understand "moving up/down/left/right". Here we define
   that "moving up" means to move 'space' up, not move other numbers up. For example
    1 2 5                1 2 -1
    3 4 -1   move up =>  3 4 5
    6 7 8                6 7 8
   This definition is actually consistent with where your finger moves to
   when you are playing 8 puzzle game.
   
3. It's just a simple example of A-Star search. You can implement this function in your own design.  
"""
def astar_search_for_puzzle_problem(init_state, dst_state, heuristics='euclidean'):
    """
    Use AStar-search to find the path from init_state to dst_state
    :param init_state:  Initial puzzle state
    :param dst_state:   Destination puzzle state
    :param heuristics:  Heuristic function
    :return:  All operations needed to be performed from init_state to dst_state
        moves: list of Move. e.g: move_list = [Move.Up, Move.Left, Move.Right, Move.Up]
    """

    # Auxiliary functions
    def find_front_node(open_list):
        '''
        Find best front node by g & h
        '''
        min_cost = open_list[0].h + open_list[0].g
        curr_state = open_list[0]
        curr_idx = 0
        
        for i in range(len(open_list)):
            if open_list[i].h + open_list[i].g < min_cost:
                min_cost = open_list[i].h + open_list[i].g
                curr_state = open_list[i]
                curr_idx = i
                
        return curr_idx, curr_state


    def state_in_list(state, state_list):
        in_list = False
        match_state = None
        
        for each in state_list:
            if each == state:
                in_list = True
                match_state = each
                break

        return in_list, match_state

    def get_path(curr_state):
        # Initiate an empty move list
        moves = []

        # Fill in path recursively
        if curr_state.pre_move == None:
            return moves
        else:
            moves.append(curr_state.pre_move)
            moves += get_path(curr_state.pre_state)

        return moves

    def expand_state(curr_state):
        moves = [0, 1, 2, 3]
        childs = []

        # One-step moving
        for each in moves:
            valid_op, next_state = once_move(curr_state, each)
            if valid_op:
                childs.append(next_state)
        
        return childs

    def update_cost(child_state, dst_state, metric):
        '''
        Update child_state.h and child_state.g
        '''
        # Euclidean distance
        if metric == 'euclidean':
            curr_vec = np.reshape(child_state.state, (-1, 1))
            dst_vec = np.reshape(dst_state.state, (-1, 1))
            forward_cost = np.linalg.norm(curr_vec-dst_vec)

        # Blank position metric
        elif metric == 'blank_pos':
            dst_pos = np.argwhere(dst_state.state==-1)
            curr_pos = np.argwhere(curr_state.state==-1)
            forward_cost = np.linalg.norm(dst_pos-curr_pos, ord=1)
            
        # Chebyshev distance
        elif metric == 'chebyshev':
            dst_pos = np.argwhere(dst_state.state==-1)
            curr_pos = np.argwhere(curr_state.state==-1)
            forward_cost = np.linalg.norm(dst_pos-curr_pos, ord=np.inf)

        # The sum of distances of the tiles from their goal positions
        elif metric == 'tiles_pos':
            dst_pos = np.argwhere(dst_state.state==-1)
            curr_pos = np.argwhere(curr_state.state==-1)
            forward_cost = np.linalg.norm(dst_pos-curr_pos, ord=1)
            
            for i in range(dst_state.square_size-1):
                dst_pos = np.argwhere(dst_state.state==(i+1))
                curr_pos = np.argwhere(curr_state.state==(i+1))
                forward_cost += np.linalg.norm(dst_pos-curr_pos, ord=1)

        
        # Update child state properties
        child_state.h = forward_cost
        child_state.g += 1
        
        return child_state

    start_state = init_state.clone()
    end_state = dst_state.clone()

    open_list = []   # You can also use priority queue instead of list
    close_list = []

    move_list = []  # The operations from init_state to dst_state

    # Initial A-star
    open_list.append(start_state)

    while len(open_list) > 0:
        # Get best node from open_list
        curr_idx, curr_state = find_front_node(open_list)

        # Delete best node from open_list
        open_list.pop(curr_idx)

        # Add best node in close_list
        close_list.append(curr_state)

        # Check whether found solution
        if curr_state == dst_state:
            move_list = get_path(curr_state)
            # Arrange move order
            move_list.reverse()
            return move_list    # 'moves' is a move_list of int

        # Expand node
        childs = expand_state(curr_state)

        for child_state in childs:

            # Explored node
            in_list, match_state = state_in_list(child_state, close_list)
            if in_list:
                continue

            # Assign cost to child state. You can also do this in Expand operation
            child_state = update_cost(child_state, dst_state, heuristics)

            # Find a better state in open_list
            in_list, match_state = state_in_list(child_state, open_list)
            if in_list:
                continue

            open_list.append(child_state)  

