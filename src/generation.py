from neural_network import NeuralNetwork
import random
import copy
import util
import cPickle as pickle
import os

bestFitness = 0
bestScore = 0
bestID = ""
bestGenome = None

class Generation(object):
    def __init__(self, size=50, networkInputSize=util.DEFAULT_INPUT_SIZE, networkHiddenSize=util.DEFAULT_HIDDEN_SIZE, networkOutputSize = util.DEFAULT_OUTPUT_SIZE):
        self.genNumber = 0
        self.size = size
        self.networkInputSize = networkInputSize
        self.networkHiddenSize = networkHiddenSize
        self.networkOutputSize = networkOutputSize
        self.genomes = [NeuralNetwork(networkInputSize, networkHiddenSize, networkOutputSize) for _ in range(0, size)]
        self.bestGenomes = []
    
    def train(self, name, win=None):
        i = 0
        global bestFitness
        global bestID
        global bestGenome
        global bestScore
        for genome in self.genomes:
            fitness, score = genome.play(win)
            if fitness > bestFitness:
                bestID = "G"+str(self.genNumber)+"I"+str(i)
                bestFitness = fitness
                bestScore = score
                bestGenome = copy.deepcopy(genome)
                try:
                    os.mkdir("./trained_model/"+name)
                except:
                    pass
                pickle.dump(genome.ihBias, open("trained_model/"+name+"/ihBias.pb", 'wb'))
                pickle.dump(genome.hhBias, open("trained_model/"+name+"/hhBias.pb", 'wb'))
                pickle.dump(genome.hoBias, open("trained_model/"+name+"/hoBias.pb", 'wb'))
                pickle.dump(genome.ihWeights, open("trained_model/"+name+"/ihWeights.pb", 'wb'))
                pickle.dump(genome.hhWeights, open("trained_model/"+name+"/hhWeights.pb", 'wb'))
                pickle.dump(genome.hoWeights, open("trained_model/"+name+"/hoWeights.pb", 'wb'))
            print("Generation " + str(self.genNumber) + " genome " + str(i) + " fitness: " + str(fitness) + " score: " + str(score) + " bestFitness: " + str(bestFitness) + " bestScore: " + str(bestScore) + " " + bestID)
            i += 1

    def saveBestGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.bestGenomes = copy.deepcopy(self.genomes[0:max(self.size//10, 4)])

    def getParent(self):
        totalScore = sum([x.fitness for x in self.genomes])
        select = random.randint(0,totalScore-1)
        runningSum = 0
        for genome in self.genomes:
            runningSum += genome.fitness
            if runningSum >= select:
                return genome
        return self.genomes[0]

    def mutate(self):
        newGenomes = copy.deepcopy(self.bestGenomes)
        while len(newGenomes) < self.size-20:
            genomeMutation1 = random.choice(self.bestGenomes)
            genomeMutation2 = random.choice(self.bestGenomes)
            newGenomes.append(self.crossover(genomeMutation1, genomeMutation2))
            newGenomes.append(self.crossover(genomeMutation2, genomeMutation1))
            newGenomes.append(self.crossover(genomeMutation1, genomeMutation2).getMutation())
            newGenomes.append(self.crossover(genomeMutation2, genomeMutation1).getMutation())
        while len(newGenomes) < self.size-8:
            genomeMutation = random.choice(self.bestGenomes)
            newGenomes.append(self.crossover(random.choice(self.bestGenomes), NeuralNetwork(self.networkInputSize, self.networkHiddenSize, self.networkOutputSize)).getMutation())
            newGenomes.append(self.crossover(NeuralNetwork(self.networkInputSize, self.networkHiddenSize, self.networkOutputSize), random.choice(self.bestGenomes)).getMutation())
        while len(newGenomes) < self.size:
            newGenomes.append(self.bestGenomes[0].getMutation())
            newGenomes.append(self.bestGenomes[1].getMutation())
            newGenomes.append(self.bestGenomes[2].getMutation())
            newGenomes.append(self.bestGenomes[3].getMutation())
        newGenomes = newGenomes[:self.size] # guarantee correct pop size
        self.genNumber += 1
        self.genomes = newGenomes
        
            
    def crossover(self, genome1, genome2):
        newGenome = copy.deepcopy(genome1)
        newGenome.ihBias = util.crossover(genome1.ihBias, genome2.ihBias)
        newGenome.hoBias = util.crossover(genome1.hhBias, genome2.hhBias)
        newGenome.hoBias = util.crossover(genome1.hoBias, genome2.hoBias)
        newGenome.ihWeights = util.crossover(genome1.ihWeights, genome2.ihWeights)
        newGenome.hhWeights = util.crossover(genome1.hhWeights, genome2.hhWeights)
        newGenome.hoWeights = util.crossover(genome1.hoWeights, genome2.hoWeights)
        newGenome.fitness = -1
        return newGenome