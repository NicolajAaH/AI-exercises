A = 'A'
B = 'B'
C = 'C'
D = 'D'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A
}


def REFLEX_VACUUM_AGENT(loc_st):
    if loc_st[1] == 'Dirty': # if current is dirty
        return 'Suck'
    if loc_st[0] == A: # else move
        return 'Right'
    if loc_st[0] == B:
        return 'Up'
    if loc_st[0] == C:
        return 'Left'
    if loc_st[0] == D:
        return 'Down'

def Sensors():
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Up' and location == B:
        Environment['Current'] = C
    elif action == 'Left' and location == C:
        Environment['Current'] = D
    elif action == 'Down' and location == D:
        Environment['Current'] = A

def run(n, start=A): # Start
    Environment['Current'] = start
    print('Current                       New')
    print('location    status  action    location    status')
    for i in range(1,n):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_VACUUM_AGENT(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:10s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20, C) # C is start

# Four squares instead of 2
#Only sense and act on the square where it is located
# Any starting square is allowed