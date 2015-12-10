import random
from random import randint
from deap import base
from deap import creator
from deap import tools
from evaluator import Evaluater
from multiprocessing import Pool

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

e = Evaluater("sorted.tsv", dist = 0.02, total_capacity = 800, date_range = 3)

def randToTotalCapacity(l):
    sum_l = sum(l)
    while sum_l > e.total_capacity:
        r = randint(0, e.k_hospitals - 1)
        if l[r] > 0:
            l[r] -= 1
            sum_l -= 1
    while sum_l < e.total_capacity:
        r = randint(0, e.k_hospitals - 1)
        if l[r] < e.hospital[r].max_capacity:
            l[r] += 1
            sum_l += 1
    return l

def randCapacity(ind):
    h = e.hospital
    l = [randint(0, h[i].max_capacity) for i in range(e.k_hospitals)]
    l = randToTotalCapacity(l)
    return ind(l)

def mutCapacity(ind):
    i1 = randint(0, e.k_hospitals - 1)
    i2 = randint(0, e.k_hospitals - 1)
    diff = randint(0, min(ind[i1], e.hospital[i2].max_capacity - ind[i2]))
    ind[i1], ind[i2] = ind[i1] - diff, ind[i2] + diff
    return ind

def cxCapacity(ind1, ind2):
    for i in range(len(ind1)):
        r = random.random()
        if r < 0.5:
            ind1[i], ind2[i] = ind2[i], ind1[i]
    ind1 = randToTotalCapacity(ind1)
    ind2 = randToTotalCapacity(ind2)
    return ind1, ind2
toolbox.register("individual", randCapacity, creator.Individual)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", e.eval)

toolbox.register("mate", cxCapacity)

toolbox.register("mutate", mutCapacity)

toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(128)
    # multiprocesssing pool
    p = Pool(4)
    pop = toolbox.population(n=100)
    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    #
    # NGEN  is the number of generations for which the
    #       evolution runs
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(p.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(p.map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = p.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    e.calc_labels(best_ind)
    # e.save_result()
    e.draw_result()
if __name__ == "__main__":
    main()
