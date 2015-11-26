import random

from deap import base
from deap import creator
from deap import tools
from evaluator import Evaluater

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

e = Evaluater("data.tsv", k = 10, dist = 0.02, capacity = 200000)
def randrange(Min, Max):
    return random.random() * (Max - Min) + Min

def randCoord(xmin, xmax, ymin, ymax):
    return (randrange(xmin, xmax), randrange(ymin, ymax))

def mutCoord(ind):
    i = random.randint(0, e.k - 1)
    ind[i] = (randrange(e.xmin, e.xmax), randrange(e.ymin, e.ymax))
    return ind

toolbox.register("coord", randCoord, e.xmin, e.xmax, e.ymin, e.ymax)

toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.coord, 10)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", e.evaluate)

toolbox.register("mate", tools.cxTwoPoint)

toolbox.register("mutate", mutCoord)

toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(128)

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
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

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
        fitnesses = map(toolbox.evaluate, invalid_ind)
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
    e.draw_result()

if __name__ == "__main__":
    main()
