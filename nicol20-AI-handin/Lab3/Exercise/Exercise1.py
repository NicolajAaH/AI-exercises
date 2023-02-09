from numpy import Infinity

A = 'A'
B = 'B'
C = 'C'
D = 'D'
E = 'E'
F = 'F'
G = 'G'
H = 'H'
I = 'I'
J = 'J'
K = 'K'
L = 'L'


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


'''
Search the tree for the goal state and return path from initial state to goal state
'''


def REMOVE_CHEAPEST_HEURISTIC(fringe): # heuristic function
    cheapest = fringe[0]
    for i in fringe:
        if heuristic(i.STATE) < heuristic(cheapest.STATE):
            cheapest = i
    fringe.remove(cheapest)
    return cheapest


def REMOVE_CHEAPEST_SUM(current_node, fringe):
    cheapest = fringe[0]
    for i in fringe:
        if evaluation_fn(i) < evaluation_fn(cheapest):
            cheapest = i
    fringe.remove(cheapest)
    return cheapest


def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    current_node = initial_node
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        #node = REMOVE_CHEAPEST_HEURISTIC(fringe) #greedy
        node = REMOVE_CHEAPEST_SUM(current_node, fringe) # a star
        current_node = node
        if node.STATE == GOAL_STATE[0] or node.STATE == GOAL_STATE[1]:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def EXPAND(node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''


def INSERT(node, queue):
    queue.append(node)
    # queue.insert(0, node)
    return queue


'''
Insert list of nodes into the fringe
'''


def INSERT_ALL(list, queue):
    for elem in list:
        queue.append(elem)  # breadth first
        # queue.insert(0, elem)  # depth first
    return queue


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


DICT = {
    'A': 6,
    'B': 5,
    'C': 5,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 5,
    'H': 2,
    'I': 2,
    'J': 1,
    'K': 0,
    'L': 0
}

COST = {
    (A, A): 0,
    (A, B): 1,
    (A, C): 2,
    (A, D): 4,
    (B, F): 5,
    (B, E): 4,
    (F, G): 1,
    (G, K): 6,
    (C, E): 1,
    (E, H): 3,
    (E, G): 2,
    (H, K): 6,
    (H, L): 5,
    (D, H): 3,
    (D, I): 4,
    (I, L): 4,
    (D, J): 2
}

INITIAL_STATE = (A)
GOAL_STATE = ['K', 'L']
STATE_SPACE = {
    A: [B, C, D],
    B: [F, E],
    C: [E],
    F: [G],
    E: [G, H],
    G: [K],
    H: [K, L],
    D: [H, I, J],
    I: [L],
    J: [],
    K: [],
    L: []
}


def heuristic(val):
    return DICT.get(val)


def cost(current, val):
    return COST.get((current, val))


def evaluation_fn(current_node):
    so_far = 0
    for i in range(0, len(current_node.path())-1): # calculate cost of its path
        so_far = so_far + cost(current_node.path()[i+1].STATE, current_node.path()[i].STATE)
    return so_far + heuristic(current_node.STATE) # add that to its value


'''
Run tree search and display the nodes in the path to goal node
'''


def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
