import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 1, 2, 3, 2, 2, 1]
    ] # dem der skal beregnes

    # Markov transition matrix
    # transitions[start, end]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state,  # gå til: [start, hot, cold, end]
                            [.0, .2, .6, .2],  # Hot state  # gå til: [start, hot, cold, end]
                            [.0, .3, .5, .2],  # Cold state # gå til: [start, hot, cold, end]
                            [.0, .0, .0, .0],  # Final state # gå til: [start, hot, cold, end]
                            ])

    # P(v|q)
    # emission[state, observation] DET ER TRANSITION PROBABILITIES
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .1, .15, .75],  # Hot state [NULL, 1, 2, 3] is givet det er varmt
                          [.0, .8, .1, .1],  # Cold state [NULL, 1, 2, 3] is givet det er koldt
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions) # forward = probability
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions) # viterbi = path
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions): # Transition matrix = a, emissions matrix = b
    # a indeholder transition probabilities
    # b indeholder the state observation likelihood of the observation symbol o_t given the current state j
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    f = big_n + 1

    # probability matrix - all values initialized to 5, as 0 has meaning in the matrix
    forward = np.ones((big_n + 2, big_t + 1)) * 5
    
    for i in inclusive_range(1, big_n):
        forward[i][1] = transitions[0][i]*emissions[i][observations[1]] # A0,S * b_s(o1)
    for t in inclusive_range(2, big_t):
        for s in inclusive_range(1, big_n):
            for s_mark in inclusive_range (1, big_n): # SUMMATION
                if forward[s,t] == 5:
                    forward[s,t] = 0
                forward[s,t] = forward[s][t] + forward[s_mark][t-1] * transitions[s_mark][s] * emissions[s][observations[t]]
    for s in inclusive_range(1, big_n): # SUMMATION
        if forward[f][big_t] == 5:
            forward[f][big_t] = 0
        forward[f][big_t] = forward[f][big_t] + forward[s][big_t]*transitions[s][f]
    return forward[f][big_t]


def compute_viterbi(states, observations, transitions, emissions):
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    f = big_n + 1

    # probability matrix - all values initialized to 5, as 0 is valid value in matrix
    viterbi = np.ones((big_n + 2, big_t + 1)) * 5

    # Must be of type int, otherwise it is tricky to use its elements to index
    # the states
    # all values initialized to 5, as 0 is valid value in matrix
    backpointers = np.ones((big_n + 2, big_t + 1), dtype=int) * 5

    for s in inclusive_range (1, big_n):
        viterbi[s][1] = transitions[0][s]*emissions[s][observations[1]]
        backpointers[s][1] = 0
    for t in inclusive_range(2, big_t):
        for s in inclusive_range(1, big_n):
            for s_mark in inclusive_range(1, big_n):
                if viterbi[s][t] == 5:
                    viterbi[s][t] = 0
                viterbi[s][t] = max(viterbi[s][t], viterbi[s_mark][t-1]*transitions[s_mark][s]*emissions[s][observations[t]])
            max_list = []
            for s_mark in inclusive_range(1, big_n):
                max_list.append(viterbi[s_mark][t-1]*transitions[s_mark][s])
            backpointers[s][t] = argmax(max_list)
    for s in inclusive_range(1, big_n):
        if viterbi[f, big_t] == 5:
            viterbi[f, big_t] = 0
        viterbi[f, big_t] = max(viterbi[f, big_t], viterbi[s][big_t]*transitions[s][f])
    max_list = []
    for s in inclusive_range(1, big_n):
        max_list.append(viterbi[s][big_t]*transitions[s][f])
    backpointers[f, big_t] = argmax(max_list)
    result = []
    result.append(backpointers[f, big_t])
    for i in range(big_t, 1, -1):
        result.append(backpointers[result[len(result)-1], i])

    result.reverse() # backtrace path by following backpointers to state back in time from backpointer[q_F, T]
    for i in range(len(result)):
        result[i] = states[result[i]]
    return result


    


def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))

    # Since we loop from 1 to big_n, the result of argmax is between
    # 0 and big_n - 1. However, 0 is the initial state, the actual
    # states start from 1, so we add 1.
    return 1 + max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()

# Implement the Forward Algorithm for the Hidden Markov Model (shown on the next slide) to compute the probability of the observation sequence 3 1 3.
# Implement the Viterbi Algorithm to compute the most likely weather sequence for the observation sequence 3 1 3.
