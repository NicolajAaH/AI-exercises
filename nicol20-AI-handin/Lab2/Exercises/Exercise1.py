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
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE:
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
    #queue.append(node)
    queue.insert(0, node)
    return queue


'''
Insert list of nodes into the fringe
'''
def INSERT_ALL(list, queue):
    for elem in list:
        #queue.append(elem)  # breadth first
        queue.insert(0, elem)  # depth first
    return queue



'''
Removes and returns the first element from fringe
'''
def REMOVE_FIRST(queue):
    if len(queue) != 0:
        return queue.pop(0)
    return []


'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


INITIAL_STATE = 'A'
GOAL_STATE = 'J'
#STATE_SPACE = {'A': ['B', 'C'],
#               'B': ['D', 'E'], 'C': ['F', 'G'],
#               'D': [], 'E': [], 'F': [], 'G': ['H', 'I', 'J'],
#               'H': [], 'I': [], 'J': [], }
STATE_SPACE = {'A': ['B', 'C'],
               'B': ['D', 'E'], 'C': ['F', 'G'],
               'D': ['H', 'I'], 'E': ['J'], 'F': [], 'G': [],
               'H': [], 'I': [], 'J': [], }

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

#Successor nodes are inserted at fron of the fringe (successor list) as a node is expanded.
# is this a breadth (FIFO) or depth-first search (LIFO)? SVAR: LIFO

# For a goal J, give the fringe (successor list) after expanding each node
# svar: A --> B,C --> D, E, C --> H, I, E, C --> I, E, C --> E, C --> J, K, C

#What is the effect of inserting successor nodes at the end of the fringe as a node ie expanded? A depth or breadth-first search?
# FIFO = breath
# svar: A --> B, C --> C, D, E --> D, E, F, G --> E, F, G, H, I --> F, G, H, I, J, K, stopper da den ser J