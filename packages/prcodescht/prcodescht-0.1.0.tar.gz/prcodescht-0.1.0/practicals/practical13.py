import numpy as np

# Parameters
num_cities = 10
num_ants = 100
num_iterations = 1000
alpha = 1
beta = 2
evaporation_rate = 0.1

# Initialize pheromone matrix with small positive values
pheromone_matrix = np.ones((num_cities, num_cities))

# Initialize distance matrix (example with random distances)
distance_matrix = np.random.randint(1, 100, size=(num_cities, num_cities))
np.fill_diagonal(distance_matrix, 0)  # No distance from a city to itself

# ACO algorithm
for iteration in range(num_iterations):
    # Ant movement and pheromone update
    for ant in range(num_ants):
        tour = []
        visited = set()
        current_city = np.random.randint(0, num_cities)
        tour.append(current_city)
        visited.add(current_city)
        
        for _ in range(num_cities - 1):
            next_city_probabilities = [(pheromone_matrix[current_city][city] ** alpha) * ((1 / distance_matrix[current_city][city]) ** beta) if city not in visited else 0 for city in range(num_cities)]
            next_city_probabilities /= np.sum(next_city_probabilities)
            next_city = np.random.choice(num_cities, p=next_city_probabilities)
            tour.append(next_city)
            visited.add(next_city)
            current_city = next_city
        
        # Update pheromone matrix
        tour_length = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))
        pheromone_matrix += (1 / tour_length)

    # Evaporation
    pheromone_matrix *= (1 - evaporation_rate)

# Find the best solution
best_tour_length = np.inf
for ant in range(num_ants):
    tour_length = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))
    if tour_length < best_tour_length:
        best_tour_length = tour_length

print("Best tour length:", best_tour_length)
