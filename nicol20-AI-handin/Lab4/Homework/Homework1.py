"""
Chessboard module

"""
import array
import copy
import random

p_mutation = 0.2  # probability of mutation, so we dont mutate everytime, 20%
num_of_generations = 70  # iterations


def fitness_fn_negative(individual):
    '''
    Compute the number of conflicting pairs, negated.
    For a solution with 5 conflicting pairs the return value is -5, so it can
    be maximized to 0.
    '''

    n = len(individual)
    fitness = 0
    for column, row in enumerate(individual):
        contribution = 0

        # Horizontal
        for other_column in range(column + 1, n):
            if individual[other_column] == row:
                contribution += 1

        # Diagonals
        for other_column in range(column + 1, n):
            row_a = row + (column - other_column)
            row_b = row - (column - other_column)
            if 0 <= row_a < n and individual[other_column] == row_a:
                contribution += 1
            if 0 <= row_b < n and individual[other_column] == row_b:
                contribution += 1

        fitness += contribution

    return - fitness


def fitness_fn_positive(state):
    '''
    Compute the number of non-conflicting pairs.
    '''

    def conflicted(state, row, col):
        for c in range(col):
            if conflict(row, col, state[c], c):
                return True

        return False

    def conflict(row1, col1, row2, col2):
        return (
                row1 == row2 or
                col1 == col2 or
                row1 - col1 == row2 - col2 or
                row1 + col1 == row2 + col2
        )

    fitness = 0
    for col in range(len(state)):
        for pair in range(1, col + 1):
            if not conflicted(state, state[pair], pair):
                fitness = fitness + 1
    return fitness


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child, child2 = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            if random.uniform(0, 1) < p_mutation:
                child2 = mutate(child2)

            new_population.add(child)
            new_population.add(child2)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        m = 15 # Keep only m fittest individuals
        ordered_population = sorted(population, key=fitness_fn, reverse=True) # sorter population ud fra fitness function og gør det med højeste først
        population = set(ordered_population[:m])

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    n = len(mother)
    crossoverpoint = random.randint(1, n-1)
    child = mother[:crossoverpoint] + father[crossoverpoint:]
    child2 = father[:crossoverpoint] + mother[crossoverpoint:]
    return child, child2


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    temparray = list(individual)
    flipindex = random.randint(0, 7)
    value = random.randint(1, 8)
    temparray[flipindex] = value
    return tuple(temparray)


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    # mother and father can be the same
    population = list(population)
    total = 0
    mother = None
    father = None
    percentages = []
    previous = 0
    for individual in population:
        total = fitness_fn(individual) + total
    for individual in population:
        percentage = fitness_fn(individual) / total
        percentages.append(percentage + previous)
        previous = previous + percentage
    rand = random.uniform(0, 1)
    for i in range(len(percentages)):
        if rand < percentages[i]:
            mother = population[i]
            break
    rand = random.uniform(0, 1)
    for i in range(len(percentages)):
        if rand < percentages[i]:
            father = population[i]
            break
    return mother, father


def fitness_function(individual):
    return fitness_fn_positive(individual)


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def main():
    minimal_fitness = (8 * (8 - 1)) / 2  # this is the maximum, thereby we are sure to get the right answer, 28

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (2, 4, 7, 4, 8, 5, 5, 2),
        (3, 2, 7, 5, 2, 4, 1, 1),
        (2, 4, 4, 1, 5, 1, 2, 4),
        (3, 2, 5, 4, 3, 2, 1, 3),
    }

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    # pass
    main()

# Modify your GA program given the following problem and code (queens_fitness.py):
# Place n-queens on a chess board in non-conflicting positions.
# Representation: A solution is represented by a list of integers, the rows of each queen. Each queen has its own column.
# (3,4,2,6,1,7,8,5) represents a queen in a3, one in b4, etc.Remember in Python list indices start from 0.
# Fitness function: returns the integer value of the number of non-conflicting queen pairs; the maximum for n queens is (n(n-1))/2.
# Fitness function(alternative): returns the integer value of the number of conflicting queen pairs.
# Minimize instead of maximizing.
# Selection: Roulette selection.
# Reproduce: Randomly select a crossover point to combine the two parents. Two new children are produced from the crossover.
# The effect is to maintain the fitness of each parent in the new population;
# keeping only one child occasionally loses fitness.
# SÆT EVT ITERAITONS OP