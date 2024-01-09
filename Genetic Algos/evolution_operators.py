import random


def generate_offspring(elite,population_size,mutation_rate):
    new_population = []
    elite_size = len(elite)
    
    # Create new individuals by performing uniform crossover and mutation
    while len(new_population) < population_size:
        parent1 = random.choice(elite)
        parent2 = random.choice(elite)
        
        # Perform uniform crossover
        child = uniform_crossover(parent1, parent2)
        
        # Apply mutation
        if random.random() < mutation_rate:
            child = mutate(child)
        
        new_population.append(child)
    
    return new_population

def uniform_crossover(parent1, parent2):
    child = []
    for gene1, gene2 in zip(parent1, parent2):
        # Randomly select genes from parents for the child
        if random.choice([True, False]):
            child.append(gene1)
        else:
            child.append(gene2)
    return child

def mutate(individual):
    # Implement mutation logic here
    # ...
    return individual
