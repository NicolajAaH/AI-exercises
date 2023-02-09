import copy

A = 'A'
B = 'B'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}

STEP_COST = {"Suck": 2, "Right": 1, "Left": 1}

GOAL_STATE = [(A, "Clean", "Clean"), (B, "Clean", "Clean")]

STATE_SPACE = {
    (A, "Dirty", "Dirty"): ["Suck", "Right"],
    (B, "Dirty", "Dirty"): ["Suck", "Left"],
    (A, "Clean", "Dirty"): ["Right", "Suck"],
    (A, "Dirty", "Clean"): ["Suck", "Right"],
    (B, "Clean", "Dirty"): ["Suck", "Left"],
    (B, "Dirty", "Clean"): ["Left", "Suck"],
    (A, "Clean", "Clean"): ["Right", "Suck"],
    (B, "Clean", "Clean"): ["Left", "Suck"],
}

HEURISTIC = {
    (A, "Dirty", "Dirty"): 4,
    (B, "Dirty", "Dirty"): 4,
    (A, "Dirty", "Clean"): 2,
    (B, "Dirty", "Clean"): 2,
    (A, "Clean", "Dirty"): 2,
    (B, "Clean", "Dirty"): 2,
    (A, "Clean", "Clean"): 0,
    (B, "Clean", "Clean"): 0
}


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)  # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


def REMOVE_CHEAPEST_SUM(fringe):
    cheapest = fringe[0]
    for node in fringe:
        st1 = (node.STATE['Current'], node.STATE[A], node.STATE[B])
        st2 = (cheapest.STATE['Current'], cheapest.STATE[A], cheapest.STATE[B])
        if node.DEPTH + HEURISTIC[st1] < cheapest.DEPTH + HEURISTIC[st2]:
            cheapest = node
    fringe.remove(cheapest)
    return cheapest


def heuristic(val):
    # print("VAL")
    # print((val['Current'], val[A], val[B]))
    return HEURISTIC.get((val['Current'], val[A], val[B]))


def TREE_SEARCH():
    fringe = []
    initial_node = Node(Environment)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_CHEAPEST_SUM(fringe)
        st = (node.STATE['Current'], node.STATE[A], node.STATE[B])
        if st == GOAL_STATE[0] or st == GOAL_STATE[1]:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


def EXPAND(node):
    successors = []
    st = (node.STATE['Current'], node.STATE[A], node.STATE[B])
    actions = successor_fn(st)
    for action in actions:
        s = Node(node)  # create node for each in state list
        s.STATE = Actuators(node, action)  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = STEP_COST[action] + node.DEPTH
        successors = INSERT(s, successors)
    return successors


def REMOVE_FIRST(queue):
    if len(queue) != 0:
        return queue.pop(0)
    return []


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


def INSERT(node, queue):
    queue.append(node)
    return queue


'''
Insert list of nodes into the fringe
'''


def INSERT_ALL(list, queue):
    for elem in list:
        queue.append(elem)  # breadth first
        # queue.insert(0, elem)  # depth first
    return queue


def Actuators(node, action):
    newState = copy.copy(node.STATE)
    location = newState['Current']
    if action == 'Suck':
        newState[location] = 'Clean'
    elif action == 'Right':
        newState['Current'] = B
    elif action == 'Left':
        newState['Current'] = A
    return newState

def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()

#The state of the search should be represented with three elemnts: a state, a path and a cost. Ultimately,
# cost is defined as the number of moves taken to achieve the goal state from the initial state.

#While moves and paths look the same as before, solutions (output) are the path, the cost of the solution and the number of explored nodes.