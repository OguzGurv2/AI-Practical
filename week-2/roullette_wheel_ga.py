import random as rd

size = 100
chromosome = 50
generations = 400
mutationRate = 0.02

def i_pop(size, chromosome):
    pop = []
    for inx in range(size):
        pop.append(rd.choices(range(2), k = chromosome))
    return pop

def fitness_f(pop):
    list = []
    for i in range(len(pop)):
        list.append(sum(pop[i]))
    return list

def print_fpop(f_pop):
    for indexp in f_pop:
        print(indexp)

def Roulette_wheel(pop, fitness):
    parents = []
    fitotal = sum(fitness)
    normalized = [x/fitotal for x in fitness]

    f_cumulative = []
    index = 0
    for n_value in normalized:
        index += n_value
        f_cumulative.append(index)

    pop_size = len(pop)
    for index2 in range(pop_size):
        rand_n = rd.uniform(0, 1)
        individual_n = 0
        for fitvalue in f_cumulative:
            if(rand_n <= fitvalue):
                parents.append(pop[individual_n])
                break
            individual_n += 1
    return parents
    
def mating_crossover(parent_a, parent_b):
    offspring = []
    
    cut_point = rd.randint(1, len(parent_a) - 1)
    
    offspring.append(parent_a[:cut_point] + parent_b[cut_point:])
    offspring.append(parent_b[:cut_point] + parent_a[cut_point:])
    
    return offspring

def mutate(chromo):
    for idx in range(len(chromo)):
        if rd.random() < mutationRate:
            chromo[idx] = 1 - chromo[idx] 
    return chromo

def init():
    pop = i_pop(size, chromosome)

    for generation in range(generations):
        fitness = fitness_f(pop)
        best_fitness = max(fitness)
        best_individual = pop[fitness.index(best_fitness)]

        if best_fitness != 50:
            selected_pop = Roulette_wheel(pop, fitness)
            crossoverList = []

            for individual_n in range(0, len(selected_pop) - 1, 2):
                crossover = mating_crossover(selected_pop[individual_n], selected_pop[individual_n + 1])
                
                crossoverList.append(crossover[0])
                crossoverList.append(crossover[1])

            mutated_offspring = []
            for individual_n2 in range(len(crossoverList)):
                mutated_offspring.append(mutate(crossoverList[individual_n2]))

            pop = mutated_offspring
            pop[0] = best_individual
            generation += 1
            
            print(f'Generation {generation}: Best Fitness = {best_fitness}')
        else:
            print(f'Generation {generation}: Best Fitness = {best_fitness}')
            print('Best fitness is reached')
            break

init()