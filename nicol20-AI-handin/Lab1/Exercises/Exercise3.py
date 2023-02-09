A = 'A'
B = 'B'
RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'NoOp'
} #Defines action for each rule such as: rule 1 procudes action Suck
rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 3,
    (A, B, 'Clean'): 4
} # Defines rule for each condition
# Ex. rule (if location == A && Dirty) then rule 1

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}


def INTERPRET_INPUT(input):
    return input


def RULE_MATCH(state, rules): # matches the rule
    rule = rules.get(tuple(state))
    return rule


def SIMPLE_REFLEX_AGENT(percept):
    state = INTERPRET_INPUT(percept)
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
        action = SIMPLE_REFLEX_AGENT(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:10s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(10)

#Condition-action rules

# change to return bogus action such as left when it should go right etc. Do the actuators allow bogus action?
# den sidder stuck, den vil ikke bevæge sig