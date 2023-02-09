current = 'min'
#  AlphaBetaDecision

def minmax_decision(state):
    infinity = float('inf')
    alpha = infinity
    beta = -infinity
    def max_value(state, alpha, beta):
        #Beta used here, alpha is assigned here
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for s in successors_of(state):
            v = max(v, min_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        #Alpha used here, beta is assigned here
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for s in successors_of(state):
            v = min(v, max_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    action = argmax(successors_of(state), lambda a: min_value(a, alpha, beta))
    return action


def is_terminal(state):
    if len(successors_of(state)) == 0:
        return True
    return False


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    if current == 'min':
        return 1
    if current == 'max':
        return -1
    return 0


def successors_of(state):
    STATES = []
    for x in state:
        half = int(x / 2)
        for i in reversed(range(half + 1, x)):
            temp = state.copy()
            temp.remove(x)
            temp.append(i)
            temp.append(x - i)
            STATES.append(temp)
    return STATES


def display(state):
    print(state)


def user_select_pile(list_of_piles):
    '''
    Given a list of piles, asks the user to select a pile and then a split.
    Then returns the new list of piles.
    '''
    print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("Which pile (from 1 to {}, must be > 2)?".format(len(list_of_piles)))
        i = -1 + int(input())

    print("Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        if list_of_piles[i] % 2 == 0:
            print(
                'How much is the first split (from 1 to {}, but not {})?'.format(
                    max_split,
                    list_of_piles[i] // 2
                )
            )
        else:
            print(
                'How much is the first split (from 1 to {})?'.format(max_split)
            )
        j = int(input())

    k = list_of_piles[i] - j

    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]

    print("    New piles: {}".format(new_list_of_piles))

    return new_list_of_piles

def computer_select_pile(state):
    new_state = minmax_decision(state)
    return new_state


def main():
    state = [7]

    while not is_terminal(state):
        state = user_select_pile(state)
        if not is_terminal(state):
            state = computer_select_pile(state)

    print("    Final state is {}".format(state))


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()

# Modify nim to play the MIN position, i.e., utility_of should return +1 for MIN and -1 for MAX
# Note:MAX is stateless, no memory of previous pile is held.
# Any pile, e.g., [1,2,3,4], can be sent to MAX which will return its move
