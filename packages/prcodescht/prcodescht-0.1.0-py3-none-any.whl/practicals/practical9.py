import numpy as np

# Define the objective function (fitness function)
def objective_function(x):
    return np.sum(x**2)

# Clonal Selection Algorithm
def clonal_selection_algorithm(num_antibodies, num_dimensions, search_space, num_generations, num_clones, clone_factor, mutation_rate):
    antibodies = np.random.uniform(search_space[:, 0], search_space[:, 1], size=(num_antibodies, num_dimensions))

    for generation in range(num_generations):
        fitness = np.array([objective_function(antibody) for antibody in antibodies])
        clones = np.repeat(antibodies, np.round(num_clones * (1 / (1 + fitness * clone_factor))).astype(int), axis=0)
        mutation_mask = np.random.rand(*clones.shape) < mutation_rate
        mutation_amounts = np.random.uniform(-0.5, 0.5, size=clones.shape) * (search_space[:, 1] - search_space[:, 0])
        mutated_clones = np.clip(clones + mutation_mask * mutation_amounts, search_space[:, 0], search_space[:, 1])
        combined_population = np.vstack((antibodies, mutated_clones))
        fitness_combined = np.array([objective_function(antibody) for antibody in combined_population])
        antibodies = combined_population[np.argsort(fitness_combined)][:num_antibodies]

    return antibodies[0]

best_solution = clonal_selection_algorithm(50, 3, np.array([[-5,5]]* 3), 100, 10,0.1, 0.1)
print("Best Solution:", best_solution)
print("Objective Value:", objective_function(best_solution))

