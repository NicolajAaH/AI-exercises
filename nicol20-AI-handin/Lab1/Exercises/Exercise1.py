A = 'A'
B = 'B'
percepts = []
table = {
    ((A, 'Clean'),): 'Right',
    ((A, 'Dirty'),): 'Suck',
    ((B, 'Clean'),): 'Left',
    ((B, 'Dirty'),): 'Suck',
    ((A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Dirty')): 'Suck',
    # ...
    ((A, 'Clean'), (A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left'
    # ...

}


def LOOKUP(percepts, table):
    action = table.get(tuple(percepts))
    return action


def TABLE_DRIVEN_AGENT(percept):
    percepts.append(percept) # appending to percepts
    action = LOOKUP(percepts, table)
    return action


def run():
    print('Action\tPercepts')
    print(TABLE_DRIVEN_AGENT((A, 'Clean')), '\t', percepts) #Say a is clean
    print(TABLE_DRIVEN_AGENT((A, 'Dirty')), '\t', percepts) # say A is dirty
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts) # say b is clean


if __name__ == '__main__':
    run()

#Explain the results: It tries to go left, since a is now dirty, adds it to a list

#How many table entries would be required if only the current percept was used to select and action rather than the percept history?
## 4; (A, Clean): Right, (A, Dirty): Suck, (B, Clean): Left, (B, Dirty): Suck

# How many table entries are required for an agent lifetime of T steps?:
# P is possible percepts, T is the lifetime of the agent (the total number of percepts it will receive)
# The lookup table will contain sum from t=1 to T |P|^t
# Her er P=4