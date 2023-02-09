X = 'X'

def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    print(action)
    return action


def is_terminal(state):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    if state[0] == state[4] and state[0] == state[8]:
        return True
    if state[2] == state[4] and state[2] == state[6]:
        return True
    for i in range(0, 3):
        if state[0 + i * 3] == state[1 + i * 3] and state[0 + i * 3] == state[2 + i * 3]:
            return True
        if state[0 + i] == state[3+i] and state[0 + i] == state[6+i]:
            return True
    for x in state:
        if not (x == X or x == 'O') and 0 <= x < 10:
            return False
    return True


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    # 0 1 2
    # 3 4 5
    # 6 7 8
    if state[0] == state[4] and state[0] == state[8]: # Diagonal
        winner = state[0]
        if winner == X:
            return 1
        if winner == 'O':
            return -1
    if state[2] == state[4] and state[2] == state[6]: # Other diagonal
        winner = state[2]
        if winner == X:
            return 1
        if winner == 'O':
            return -1
    for i in range(0, 3):
        if state[0 + i * 3] == state[1 + i * 3] and state[0 + i * 3] == state[2 + i * 3]: # Rows
            winner = state[0 + i * 3]
            if winner == X:
                return 1
            if winner == 'O':
                return -1
        if state[0 + i] == state[3 + i] and state[0 + i] == state[6 + i]: # Column
            winner = state[0 + i]
            if winner == X:
                return 1
            if winner == 'O':
                return -1
    return 0 # draw


def successors_of(state):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    STATES = []
    for i in range(0, 9):
        if not state[i] == X and not state[i] == 'O': # gør det for alle hvor der ikke er dem. find alle muligheder
            countx = 0
            counto = 0
            for x in state:
                if x == X:
                    countx += 1
                if x == 'O':
                    counto += 1
            tempState = state.copy()
            minval = min(countx, counto)
            if minval == countx:
                tempState[i] = X
            else:
                tempState[i] = 'O'
            STATES.append((i, tempState))
    return STATES


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8] # initial state of the board without moves
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()

#Game Initial state: includes board position and th eplayer to move
#Successor function game: returns a list of (move, state) pairs, where move is legal
#Terminal test game: game over at some terminal state
#Utility function (objective or payoff function) game: give numeric values of a terminal state. E.g., win: +1, loss: -1, draw: 0

#Tic-tac-toe:
# Initial state: board empty, MAX turn
# Successor function: returns the list of 9 pairs (move, state)
# (0, [X, 1, 2, 3, 4, 5, 6, 7, 8])
# (1, [0, X, 2, 3, 4, 5, 6, 7, 8])
# (2, [0, 1, X, 3, 4, 5, 6, 7, 8])
# (3, [0, 1, 2, X, 4, 5, 6, 7, 8])
# (4, [0, 1, 2, 3, X, 5, 6, 7, 8])
# (5, [0, 1, 2, 3, 4, X, 6, 7, 8])
# (6, [0, 1, 2, 3, 4, 5, X, 7, 8])
# (7, [0, 1, 2, 3, 4, 5, 6, X, 8])
# (8, [0, 1, 2, 3, 4, 5, 6, 7, X])

# 0 1 2
# 3 4 5
# 6 7 8

# What is the branching factor at depth 0? At depth 1?
## At depth 0 it is 9. At depth 1 it is 8 for each. I.e. 9*8 = 72

# What is the maximal depth?
## The maximum depth is 9, since there is 9 squares

# Will a MIN move attempt to minimize or maximize the utility?
## The min move will attempt to minimize the utility

# Are states after a terminal state explored?
## Yes, since it backtracks when a terminal state is hit??? Den tjekker jo alt så derfor tjekker den også alle de andre

# Are all possible states explored to a terminal state?
## Yes, since it explores all possible states, since there is no pruning as in alpha-beta pruning

# Is this a depth-first or breadth-first search? How do you know? (see Python code)
## Depth-first since it just goes for the best all the way down
