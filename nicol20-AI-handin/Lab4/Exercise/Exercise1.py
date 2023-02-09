import array
import copy
import random


p_mutation = 0.2 # probability of mutation, so we dont mutate everytime, 20%
num_of_generations = 70 # iterations


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

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
    crossoverpoint = random.randint(0,1) # only between those
    moth = mother[:crossoverpoint]
    fath = father[crossoverpoint:]
    child = moth + fath
    return child


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    temparray = list(individual)
    if random.random() < p_mutation:
        flipindex = random.randint(0, 2)
        if individual[flipindex] == 0:
            temparray[flipindex] = 1
        else:
            temparray[flipindex] = 0
        return tuple(temparray)
    return individual


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
    ordered_population = list(population)
    total = 0
    mother = None
    father = None
    percentages = []
    previous = 0
    for individual in ordered_population:
        total = fitness_fn(individual) + total
    for individual in ordered_population:
        percentage = fitness_fn(individual) / total
        percentages.append(percentage + previous)
        previous = previous + percentage
    rand = random.random()
    for i in range(len(percentages)):
        if rand < percentages[i]:
            mother = ordered_population[i]
            break
    rand = random.random()
    for i in range(len(percentages)):
        if rand < percentages[i]:
            father = ordered_population[i]
            break
    return mother, father


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''
    fitness = individual[0] * 4 + individual[1] * 2 + individual[2] * 1
    return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7 # this is the maximum, thereby we are sure to get the right answer

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    #initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    #pass
    main()
