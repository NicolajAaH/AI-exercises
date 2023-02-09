A = 'A'
B = 'B'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}


def REFLEX_VACUUM_AGENT(loc_st):
    if loc_st[1] == 'Dirty':
        return 'Suck'
    if loc_st[0] == A:
        return 'Right'
    if loc_st[0] == B:
        return 'Left'

def Sensors(): #function to sense current location and status of environment (i.e., location of agent and status of square)
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action): #function to affect current environment location by some action (i.e., suck, left, right, NoOp)
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
    for i in range(1,n):
        (location, status) = Sensors() # get info
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_VACUUM_AGENT(Sensors()) # get action
        Actuators(action) #Handle
        (location, status) = Sensors() # get new status
        print("{:10s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(10)

# Only responds to current percept (location and status) ignoring percept history
# Brug if statements

# Should bogus actions be able to corrup the environment?
# change to return bogus action such as left when it should go right etc. Do the actuators allow bogus action?
#SVAR: Den crasher ikke, men den forsøger bare hele tiden. Altså så den vil prøve og gå til højre hele tiden hvis den er på B