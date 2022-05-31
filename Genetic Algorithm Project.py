import numpy as np
import random

# this one is working and converging

# returns population as list of lists
def makePopulation(size):
    # This creates an array with values under 2 so 0 and 1's at random.
    # Size represents the population size and length represents the genome length in the 2D array.
    rng = np.random.default_rng()
    population = rng.integers(2, size=(size, LENGTH))   # makes the population as ndarray
    population = np.ndarray.tolist(population)   # convert ndarray to list
    # returns list of lists
    return population

# find the fitness of each genome
def fitness(genome):
    total, nums = 0, [] #makes a new list of numbers and says our total is starting at 0.
    for g in genome: #we are now saying that if an integer in genome is equal to one it needs to be added to our new list called total
        if g == 1:total += 1
    return total

# find the average fitness of the population and return the most fit genome
def fitnessAvg(population):
    total, most_fit = 0, 0 #says the total and most fit scores start at 0
    for genome in population: #says for each genome in the population
        total += fitness(genome)  #we add fitness score found in the fitness function of each genome to our total
        if fitness(genome) > most_fit: #if the fitness of the genome is greater than our most fit,
            most_fit = fitness(genome) #then that fitness score becomes our new most fit genome
    avg = total / len(population) #the total of all fitness scores is then divided by the total number of genomes in the population to get our average
    return avg, most_fit

# Select a random pair of genomes using roulette wheel selection
def selectPair(population):
   population_fitness = sum((fitness(i) for i in population)) #we are getting the total population fitness
   string_probabilities = [fitness(i)/population_fitness for i in population] #formula given on powerpoint to select
   randomGenome1 = np.random.randint(0, (len(string_probabilities) - 1)) #picking a random intiger(genome)
   randomGenome2 = np.random.randint(0, (len(string_probabilities) - 1)) #picking a second random integer(genome)
   return population[randomGenome1], population[randomGenome2]

# Performs crossover based on the crossover rate we give it.
def crossover(genome1, genome2, crossoverRate):
   if random.random() < crossoverRate: #if a random number under the crossover rate is selected then crossover happens
       CrossoverHappens = True  #if crossover is true then the follwoing happens:
       recombinedpopulation = [] #a new list with the two crossed genomes or unchanged genomes is formed
       splice = random.randint(0, len(genome1) - 1)  # we slice the two genomes at random points
       GenomeOne = genome1[:splice] + genome2[splice:] #we are attaching the front half of genome one to the other half of genome 2
       GenomeTwo = genome2[:splice] + genome1[splice:] #we are attaching the front half of genome two to the other half of genome 1
       recombinedpopulation.append(GenomeOne) # adds genome 1 to our new recombinedpopulation list
       recombinedpopulation.append(GenomeTwo) # adds genome 2 to our new recombinedpopulation list
       return recombinedpopulation, CrossoverHappens #identifies what we want out of the function
   else:
       CrossoverHappens = False #if crossover is false then the following happens
       recombinedpopulation = [genome1, genome2] #the original genomes are the recombined population list
   return recombinedpopulation, CrossoverHappens #identifies what we want out of the function

# Performs mutation based on the mutation rate given.
def mutate(children, mutationRate):
    for genome in children:
        for i in range(len(genome)): #says for a random genome, if an assigned random number is less than the mutation rate then it mutates
            m = random.random()
            if m < mutationRate:
                genome[i] = 1 - genome[i]
    return children

# Performs replacement based off whether or not crossover happens. If crossover does happen both of our lowest scoring genomes are replaced with crossed over ones.
#If crossover does not happen then only the lowest scoring genome is replaced.
def replace(population, children, CrossoverHappens):
   temp = []
   c1, c2 = children[0], children[1]
   C1 = []
   C2 = []
   FIT1 = fitness(c1)
   FIT2 = fitness(c2)
   C1.append(FIT1)
   C1.append(children[0])
   C2.append(FIT2)
   C2.append(children[1]) #The above code assigns the two children a fitness score to get them into the same format as the fitness list.
   for i in population:
       fitness_list = [] #creating a new list of fitness variable to then be attached to our new "temp" list that will now hav population ranked by fitness.
       fitness_list.append(fitness(i))
       fitness_list.append(i)
       temp.append(fitness_list)
   temp.sort(reverse=False) #this lists the fitness with their corresponding genome in order of least fit to most.
   if (CrossoverHappens == True):
       del temp[0], temp[1] #these are the two genomes from original population with lowest fitness score and deletes them
           # could do temp.sort(reverse=True), this would then append the
           # following two in the same spot rather than at the back of the population, would then need to flip again after.. is this necessary or does this automatically happen?
       temp.append(C1), #since Crossover happened, we are replacing the lowest fitness genomes with the new children from the crossover,
       temp.append(C2) #this add both to our temp list
   else:
       del temp[0],
       temp.append(C1)
   l = temp
   flatten_list = [item for subl in l for item in subl] #this gets rid of a layer of nesting in my code which needed to happen to more easily remove fitness scores
   for i,x in enumerate(flatten_list):  #this allowed me to remove all values (all fitness scores) >-1 in my string without effecting the genome strings (removed fitness scores)
       if x > -1:
           flatten_list.pop(i)
   return flatten_list

LENGTH = 20 #the lenght of our genome

# Calls on the other functions to simulate population loops until a fitness score (20) matching the length of the genome is achieved, and creates a .txt file with the generations and fitness scores.
def runGA(generations, size, crossoverRate, mutationRate, logFile="nickLog.txt"):
    logGA = open(logFile, "w") #opens the log file to write the following results
    population = makePopulation(size) #this generates the first population
    for i in range(generations): #specifies how many generations I will let the code run till, and tells when to terminate when the most_fit equals 20, the lenght of the genome.
        avg, most_fit = fitnessAvg(population)
        if most_fit == LENGTH: #breaks the loop and prints goal if the length is met by a genome.
                print("goal!")
                break
        genome1, genome2 = selectPair(population) #performs selectPair function given the population
        children, CrossoverHappens = crossover(genome1, genome2, crossoverRate) #performs crossover function on the selected pair
        mutated = mutate(children, mutationRate) #performs the mutation function on the children
        population = replace(population, children, CrossoverHappens) #calls replacement function and replaces the population with the new one and the cycle will repeat until the break condition above is met
        print("Generation", i, ": average fitness", round(avg,2), ", best fitness", most_fit) #prints each generation with the corresponding information into the .txt file
        logGA.write(' '.join([str(i), str(round(avg,2)), str(most_fit), "\n"]))
    logGA.close() #closes the .txt file
    return
runGA(1000, 100, 0.7, 0.001) #this is where I adjust my values