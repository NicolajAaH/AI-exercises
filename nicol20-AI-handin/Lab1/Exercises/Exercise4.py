A = 'A'
B = 'B'
state = {}
action = None
model = {A: None, B: None} #Empty at start
RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'NoOp'
} # See exercise 3
rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 3,
    (A, B, 'Clean'): 4
}
# Ex. rule (if location == A && Dirty then rule 1

Environment = {
    A: 'Dirty',
    B: 'Dirty',
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
    if model[A] == model[B] == 'Clean': #Model only used to change state when A==B=='Clean'
        state = (A, B, 'Clean')
    model[location] = status
    return state

def REFLEX_AGENT_WITH_STATE(percept):
    global state, action
    state = UPDATE_STATE(state,action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action

def Sensors():
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Left' and location == B:
        Environment['Current'] = A


def run(n):
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
    run(10)
# Reflex agent with state
# Reflex agent only responded to current percepts; no history or knowledge
# Model-based reflex agents:
# - Maintain internal state that depends upon percept history
# - Agent has a model of how two types of information to update
# - THe model requires two types of information to update:
# -- How environment evvolves independent of the agent (e.g., Clean square stays clean)
# -- How agents action affect the environment (e.g., suck cleans square)