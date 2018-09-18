import util
import random
import copy
import pygame
import game as gm
import snake as sn
import sys

class NeuralNetwork(object):
    def __init__(self, inputSize, hiddenSize, outputSize):
        self.inputSize = inputSize
        self.hiddenSize = hiddenSize
        self.outputSize = outputSize

        self.ihBias = [[random.uniform(-1, 1) for _ in range(hiddenSize)]]
        self.hhBias = [[random.uniform(-1, 1) for _ in range(hiddenSize)]]
        self.hoBias = [[random.uniform(-1, 1) for _ in range(outputSize)]]
        self.ihWeights = [[random.uniform(-1, 1) for _ in range(hiddenSize)] for _ in range(inputSize)]
        self.hhWeights = [[random.uniform(-1, 1) for _ in range(hiddenSize)] for _ in range(hiddenSize)]
        self.hoWeights = [[random.uniform(-1, 1) for _ in range(outputSize)] for _ in range(hiddenSize)]

        self.fitness = -1 # -1 until updated by evaluation
        
    def getOutput(self, inputs):
        a_1 = [[util.sigmoid(x) for x in util.add(util.dot(inputs, self.ihWeights), self.ihBias)[0]]]
        #a_2 = [[util.sigmoid(x) for x in util.add(util.dot(a_1, self.hhWeights), self.hhBias)[0]]] # uncomment and fix a_3 for 2 hidden layers
        a_3 = [[util.sigmoid(x) for x in util.add(util.dot(a_1, self.hoWeights), self.hoBias)[0]]]
        return a_3[0]

    def getMutation(self):
        newNetwork = copy.deepcopy(self)
        newNetwork.ihBias = util.gaussianMutate(newNetwork.ihBias) 
        newNetwork.hhBias = util.gaussianMutate(newNetwork.hhBias)
        newNetwork.hoBias = util.gaussianMutate(newNetwork.hoBias)
        newNetwork.ihWeights = util.gaussianMutate(newNetwork.ihWeights)  
        newNetwork.hhWeights = util.gaussianMutate(newNetwork.hhWeights)
        newNetwork.hoWeights = util.gaussianMutate(newNetwork.hoWeights)
        newNetwork.fitness = -1
        return newNetwork
    
    def play(self, win=None, verbose=False):
        game = gm.Game()
        snake = sn.Snake(game, self)
        clock = pygame.time.Clock()
        while not game.over:
            if win:
                clock.tick(50)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            feedforward = self.getOutput(snake.getInputv2())
            movedirection = -1
            maximum = -1
            for i, val in enumerate(feedforward):
                if val > maximum:
                    maximum = val
                    movedirection = i
            #print(movedirection, maximum, max(feedforward), sum([x for x in snake.getInput()[0]]))
            finalDirection = snake.direction
            if movedirection == 0: # forward
                pass
            elif movedirection == 1: # left
                finalDirection = util.turnLeft[snake.direction]
            elif movedirection == 2: # right
                finalDirection = util.turnRight[snake.direction]

            if verbose and game.board[util.positionOnceTowardsDirection(snake.cells[0], game, finalDirection)] == 2:
                print("Snake's score is now {}, length {}".format(game.score+100, snake.length+3))
            snake.move(finalDirection)

            if game.score/10 + (snake.steps-snake.stepsAway) - 1.5*snake.stepsAway < -500:
                # the snake is moving indefinitely, cut off.
                #print(0)
                self.fitness = game.score/10 + (snake.steps-snake.stepsAway) - 1.5*snake.stepsAway
                return [self.fitness, game.score]

            if(win): # window
                win.fill((0,0,0))
                game.display(win)
                pygame.display.update()
        if verbose:
            print("Snake ended with a score of {}".format(game.score))

        self.fitness = game.score/2 + (snake.steps-snake.stepsAway) - 1.5*snake.stepsAway
        return [self.fitness, game.score]
    def display(self):
        print("ihBias")
        print(self.ihBias)
        print("ihWeights")
        print(self.ihWeights)
        print("hoBias")
        print(self.hoBias)
        print("hoWeights")
        print(self.hoWeights)
