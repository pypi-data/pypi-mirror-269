import os

# CI
rpc = """
# client.py
import Pyro4 
uri = "PYRONAME:factorial.server" # Get the URI of the server object from the name  server 
factorial_server = Pyro4.Proxy(uri) 
number = int(input("Enter the number to calculate factorial: ")) 
result = factorial_server.factorial(number) 
print(f"The factorial  of {number} is {result}")
##############################################################

# clientA.py
import xmlrpc.client

def main():
    # Connect to the server
    server = xmlrpc.client.ServerProxy('http://localhost:8000')

    # User input for factorial calculation
    number = int(input("Enter a number to calculate its factorial: "))
    result = server.factorial(number)
    print(f"The factorial of {number} is {result}")

if __name__ == "__main__":
    main()
##############################################################

# server.py 
import Pyro4 
@Pyro4.expose 
class FactorialServer: 
    def factorial(self, n): 
        result = 1 
        for i in range(1, n + 1): 
            result *= i 
        return result 
daemon = Pyro4.Daemon() # Make a Pyro daemon 
ns = Pyro4.locateNS() # Find the name server 
uri = daemon.register(FactorialServer) # Register the server object with a name in the  name server 
ns.register("factorial.server", uri) # Register the object with a name in the name server
print("Factorial server ready.") 
daemon.requestLoop() # Start the event loop of the server to wait for calls 
##############################################################

# serverA.py
import xmlrpc.server
import math

class MathServices:
    def factorial(self, n):
        return math.factorial(n)

# Set up the server
server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")

# Register MathServices instance to handle requests
server.register_instance(MathServices())

# Run the server's main loop
server.serve_forever()
##############################################################
    
# To run use commands
# pyro4-ns
# python server.py
# python client.py
"""

rmi = """
# client2.py
import Pyro4

def main():
    uri = input("Enter the URI of the server: ")
    str1 = input("Enter the first string: ")
    str2 = input("Enter the second string: ")

    concat_server = Pyro4.Proxy(uri)
    concatenated_str = concat_server.concatenate_strings(str1, str2)
    
    print("Concatenated String:", concatenated_str)

if __name__ == "__main__":
    main()
##############################################################

# server2.py
import Pyro4

@Pyro4.expose
class StringConcatenator(object):
    def concatenate_strings(self, str1, str2):
        return str1 + str2

def main():
    daemon = Pyro4.Daemon()
    uri = daemon.register(StringConcatenator)
    
    print("Server URI:", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
##############################################################
    
# To run use commands
pyro4-ns
python server2.py
python client2.py
"""

mapreduce_character_count = """
# character_count.py
from mrjob.job import MRJob
import sys

class CharacterCount(MRJob):
    
    def mapper(self, _, line):
        # Emit each character with count 1
        for char in line:
            yield char, 1
    
    def reducer(self, key, values):
        # Sum up the counts for each character
        yield key, sum(values)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python character_count.py <input_file>")
        sys.exit(1)
    CharacterCount.run()

##############################################################
    
# word_count.py
from mrjob.job import MRJob
import re
import sys

WORD_RE = re.compile(r"[\w']+")

class WordCount(MRJob):
    
    def mapper(self, _, line):
        # Emit each word with count 1
        for word in WORD_RE.findall(line):
            yield word.lower(), 1
    
    def reducer(self, key, values):
        # Sum up the counts for each word
        yield key, sum(values)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python word_count.py <input_file>")
        sys.exit(1)
    WordCount.run()
##############################################################

# x.txt    
Dr D y Patil Institute Of Engineering Management And Research , Akurdi

##############################################################
"""

fuzzy_sets_u_n = """
A = dict()
B = dict()
Y = dict()

A = {"a": 0.2, "b": 0.3, "c": 0.6, "d": 0.6}
B = {"a": 0.9, "b": 0.9, "c": 0.4, "d": 0.5}

print('The First Fuzzy Set is :', A)
print('The Second Fuzzy Set is :', B)


for A_key, B_key in zip(A, B):
	A_value = A[A_key]
	B_value = B[B_key]

	if A_value > B_value:
		Y[A_key] = A_value
	else:
		Y[B_key] = B_value
		
print('Fuzzy Set Union is :', Y)



for A_key, B_key in zip(A, B):
	A_value = A[A_key]
	B_value = B[B_key]

	if A_value < B_value:
		Y[A_key] = A_value
	else:
		Y[B_key] = B_value
print('Fuzzy Set Intersection is :', Y)

A = dict()
Y = dict()
 
A = {"a": 0.2, "b": 0.3, "c": 0.6, "d": 0.6}
 
print('The Fuzzy Set is :', A)
 
 
for A_key in A:
   Y[A_key]= 1-A[A_key]
         
print('Fuzzy Set Complement is :', Y)

for A_key, B_key in zip(A, B):
    A_value = A[A_key]
    B_value = B[B_key]
    B_value = 1 - B_value
 
    if A_value < B_value:
        Y[A_key] = A_value
    else:
        Y[B_key] = B_value
         
print('Fuzzy Set Difference is :', Y)
"""

optimize_gen_algo_spray_dry = """
import random

from deap import base, creator, tools, algorithms

def evaluate(individual):
    return random.random(),

# Define genetic algorithm parameters

POPULATION_SIZE = 10

GENERATIONS = 5

# Create types for fitness and individuals in the genetic algorithm

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)

# Initialize toolbox

toolbox = base.Toolbox()

# Define attributes and individuals

toolbox.register("attr_neurons", random.randint, 1, 100)  # Example: number of neurons

toolbox.register("attr_layers", random.randint, 1, 5)  # Example: number of layers

toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_neurons,

                                                                      toolbox.attr_layers), n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Genetic operators

toolbox.register("evaluate", evaluate)

toolbox.register("mate", tools.cxTwoPoint)

toolbox.register("mutate", tools.mutUniformInt, low=1, up=100, indpb=0.2)

toolbox.register("select", tools.selTournament, tournsize=3)

# Create initial population

population = toolbox.population(n=POPULATION_SIZE)

# Run the genetic algorithm

for gen in range(GENERATIONS):

    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    fitnesses = toolbox.map(toolbox.evaluate, offspring)

    for ind, fit in zip(offspring, fitnesses):

        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))

# Get the best individual from the final population

best_individual = tools.selBest(population, k=1)[0]

best_params = best_individual

# Print the best parameters found

print("Best Parameters:", best_params)

###################################################### next cell

import matplotlib.pyplot as plt

# Extract the number of neurons and number of layers for each individual in the final population
neurons = [ind[0] for ind in population]
layers = [ind[1] for ind in population]

# Plot the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(neurons, layers, c='b', label='Population')
plt.scatter(best_params[0], best_params[1], c='r', label='Best Individual', marker='x', s=100)
plt.xlabel('Number of Neurons')
plt.ylabel('Number of Layers')
plt.title('Best Parameters Found by Genetic Algorithm')
plt.legend()
plt.grid(True)
plt.show()
"""

clonal_select_algo = """
# The Clonal Selection Algorithm (CSA) is a computational optimization algorithm inspired by the immune system's clonal selection process, where it clones and mutates high-affinity immune cells to improve their antigen recognition, effectively mimicking an adaptive search process for optimization problems.

import random
import numpy as np

# Define the objective function
def objective_function(x):
# Example: Sphere function
    return sum([i**2 for i in x])

# Initialize population
def initialize_population(pop_size, dimensions, lower_bound, upper_bound):
    population = []
    for _ in range(pop_size):
        individual = np.random.uniform(lower_bound, upper_bound, dimensions)
        population.append(individual)
    return population

# Clone an individual
def clone_individual(individual, clone_factor):
    clones = []
    for _ in range(clone_factor):
        clone = np.array(individual)
        for i in range(len(clone)):
          mutation_rate = random.uniform(0, 1)
          if mutation_rate < 0.5:
            clone[i] += random.uniform(-1, 1)
    clones.append(clone)
    return clones

# Select the best individuals
def select_best(population, num_selected, num_clones, clone_factor):
    population.sort(key=lambda x: objective_function(x))
    selected = []
    for i in range(min(len(population), num_selected)):
        clones = clone_individual(population[i], clone_factor)
        selected.extend(clones)
    return selected[:num_clones]

# Main function for clonal selection algorithm
def clonal_selection_algorithm(pop_size, dimensions, lower_bound, upper_bound,num_generations, num_selected, num_clones, clone_factor):
    population = initialize_population(pop_size, dimensions, lower_bound, upper_bound)
    for _ in range(num_generations):
        selected = select_best(population, num_selected, num_clones, clone_factor)
        population = selected
    best_solution = min(population, key=lambda x: objective_function(x))
    return best_solution, objective_function(best_solution)

if __name__ == "__main__":
    pop_size = 100
    dimensions = 2
    lower_bound = -5.0
    upper_bound = 5.0
    num_generations = 100
    num_selected = 10
    num_clones = 5
    clone_factor = 3

best_solution, best_fitness = clonal_selection_algorithm(pop_size,dimensions, lower_bound,upper_bound, 
                                                        num_generations, num_selected, num_clones, clone_factor)
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
"""

# DC
Deap = """
import random
from deap import base, creator, tools, algorithms

def evaluate(individual):
    return sum(individual),

# Create the DEAP types for the individuals and fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Initialize the DEAP toolbox
toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

population_size = 100
num_generations = 50

# Create initial population
population = toolbox.population(n=population_size)

# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

    
# Evolutionary loop
for generation in range(num_generations):
    # Select the next generation individuals
    offspring = toolbox.select(population, len(population))

    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

            
invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
fitnesses = map(toolbox.evaluate, invalid_ind)
for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

# Replace the current population with the offspring
population[:] = offspring

# Print the best individual
best_individual = tools.selBest(population, 1)[0]
print("Best individual:", best_individual)
print("Fitness:", best_individual.fitness.values[0])
"""

ant_colony = """
import numpy as np

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        shortest_path_length = np.inf
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path, shortest_path_length)
            shortest_path, shortest_path_length = self.get_shortest(all_paths)
            self.pheromone *= self.decay

        return shortest_path, shortest_path_length

    def spread_pheronome(self, all_paths, n_best, shortest_path, shortest_path_length):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move

    def get_shortest(self, all_paths):
        best_path = None
        best_path_length = np.inf
        for path, dist in all_paths:
            if dist < best_path_length:
                best_path_length = dist
                best_path = path
        return best_path, best_path_length

if __name__ == '__main__':
    # Define the distance matrix
    distances = np.array([[np.inf, 10, 15, 20],
                          [10, np.inf, 35, 25],
                          [15, 35, np.inf, 30],
                          [20, 25, 30, np.inf]])

    # Initialize the Ant Colony Optimization algorithm
    ant_colony = AntColony(distances, n_ants=3, n_best=2, n_iterations=100, decay=0.95)

    # Run the algorithm
    shortest_path, shortest_path_length = ant_colony.run()

    print("Shortest Path:", shortest_path)
    print("Shortest Path Length:", shortest_path_length)
"""

arti_immune_pr_damage_class = """
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score , classification_report

# Generate synthetic dataset
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


print("Classification Report:")
print(classification_report(y_test, y_pred))
"""

art_neural_style_transfer = """
!pip install tensorflow

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import vgg19
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras import backend as K
import numpy as np
import matplotlib.pyplot as plt

# Function to load and preprocess an image
def load_and_preprocess_image(image_path, img_height, img_width):
    img = keras_image.load_img(image_path, target_size=(img_height, img_width))
    img = keras_image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img

# Function to convert a tensor into a valid image
def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.clip(tensor, 0, 255).astype('uint8')
    return tensor[0]

# Define paths to style and content images using raw string (r-prefix) or escaped backslashes
style_image_path =  r'style1.jpg'
content_image_path = r'content1.jpg'
# Constants for image dimensions
img_height = 400
img_width = 400

# Load style and content images
style_image = load_and_preprocess_image(style_image_path, img_height, img_width)
content_image = load_and_preprocess_image(content_image_path, img_height, img_width)

#### New cell
import tensorflow as tf

def style_loss(style_targets, style_outputs):
    loss = tf.zeros(shape=())  # Initialize loss tensor
    num_layers = len(style_targets)  # Number of style layers

    for i in range(num_layers):
        target_features = style_targets[i]
        output_features = style_outputs[i]

        # Compute Gram matrices for target and output features
        target_gram_matrix = gram_matrix(target_features)
        output_gram_matrix = gram_matrix(output_features)

        # Compute mean squared difference between Gram matrices
        layer_loss = tf.reduce_mean(tf.square(target_gram_matrix - output_gram_matrix))
        
        # Accumulate layer loss
        loss += layer_loss
    
    # Average loss across all style layers
    total_loss = loss / float(num_layers)
    
    return total_loss

def gram_matrix(tensor):
    # Get shape of the tensor (batch_size, height, width, channels)
    batch_size, height, width, channels = tensor.get_shape().as_list()
    
    # Reshape tensor to combine batch_size and spatial dimensions
    reshaped_tensor = tf.reshape(tensor, [batch_size * height * width, channels])
    
    # Compute Gram matrix: A^T * A where A is the reshaped tensor
    gram = tf.matmul(reshaped_tensor, reshaped_tensor, transpose_a=True)
    
    # Normalize Gram matrix by the number of elements
    num_elements = tf.cast(batch_size * height * width * channels, tf.float32)
    gram /= num_elements
    
    return gram
# Use tf.Variable to create a trainable image (initialized with content image)
generated_image = tf.Variable(content_image, dtype=tf.float32)

# Optimizer and training loop
optimizer = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

### New cell
# Convert the final generated image tensor to a valid image
final_image = tensor_to_image(generated_image.numpy())

# Display the final stylized image
plt.imshow(final_image)
plt.axis('off')
plt.show()
"""

masterDict = {
    "rpc": rpc,
    "rmi": rmi,
    "mapreduce_character_count": mapreduce_character_count,
    "fuzzy_sets_u_n": fuzzy_sets_u_n,
    "optimize_gen_algo_spray_dry": optimize_gen_algo_spray_dry,
    "clonal_select_algo": clonal_select_algo,
    "Deap": Deap,
    "ant_colony": ant_colony,
    "arti_immune_pr_damage_class": arti_immune_pr_damage_class,
    "arti_immune_pr_damage_class": arti_immune_pr_damage_class,
}


class Writer:
    def __init__(self, filename):
        self.filename = os.path.join(os.getcwd(), filename)
        self.masterDict = masterDict
        self.questions = list(masterDict.keys())

    def getCode(self, input_string):
        input_string = self.masterDict[input_string]
        with open(self.filename, "w") as file:
            file.write(input_string)
        print(f"##############################################")


if __name__ == "__main__":
    write = Writer("output.txt")
    print(write.questions)
    # write.getCode("rpc")
