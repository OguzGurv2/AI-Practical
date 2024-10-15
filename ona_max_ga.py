import random as rd
import numpy as np
import math

size = 4
chromosome = 8

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

    print('normalized fitness')
    print('__________________')
    print_fpop(normalized)
    print('__________________')
    f_cumulative = []
    index = 0
    for n_value in normalized:
        index += n_value
        f_cumulative.append(index)

    pop_size = len(pop)
    print('cumulative fitness')
    print('__________________')
    print_fpop(f_cumulative)
    print('__________________')
    for index2 in range(pop_size):
        rand_n = rd.uniform(0, 1)
        individual_n = 0
        for fitvalue in f_cumulative:
            if(rand_n <= fitvalue):
                parents.append(pop[individual_n])
                break
            individual_n += 1
    return parents

def mutate(chromo):
    for idx in range(len(chromo)):
        if rd.random() < 0.3:
            chromo = chromo[:idx] + [1 - chromo[idx]] + [chromo[idx + 1:]]
        return chromo
    
def mating_crossover(parent_a, parent_b):
    offspring = []
    cut_point = rd.randint(1, len(parent_a) - 1)

    offspring.append(parent_a[:cut_point] + parent_b[cut_point:])
    offspring.append(parent_b[:cut_point] + parent_a[cut_point:])
    return offspring

def init():
    pop = i_pop(size, chromosome)
    fitness = fitness_f(pop)
    selected_pop = Roulette_wheel(pop, fitness)
    selected_fitness = fitness_f(selected_pop)


init()