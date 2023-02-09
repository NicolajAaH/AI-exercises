A = 'A'
B = 'B'
C = 'C'
D = 'D'
state = {}
action = None
model = {A: None, B: None, C: None, D: None} #empty at start
RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'NoOp',
    5: 'Up',
    6: 'Down'
}
rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 5,
    (C, 'Clean'): 3,
    (D, 'Clean'): 6,
    (A, B, C, D, 'Clean'): 4
}
# Ex. rule (if location == A && Dirty then rule 1

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def INTERPRET_INPUT(input):
    return input


def RULE_MATCH(state, rules):
    rule = rules.get(tuple(state))
    return rule


def UPDATE_STATE(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == 'Clean': # see exercise 4
        state = (A, B, C, D, 'Clean')
    model[location] = status
    return state


def REFLEX_AGENT_WITH_STATE(percept):
    global state, action
    state = UPDATE_STATE(state, action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


def Sensors():
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):
    location = Environment['Current']
    if action == 'Suck': # see homework1
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Up' and location == B:
        Environment['Current'] = C
    elif action == 'Left' and location == C:
        Environment['Current'] = D
    elif action == 'Down' and location == D:
        Environment['Current'] = A


def run(n, start=A):
    Environment['Current'] = start
    print('Current                       New')
    print('location    status  action    location    status')
    for i in range(1, n):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_AGENT_WITH_STATE(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:10s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20, C)
