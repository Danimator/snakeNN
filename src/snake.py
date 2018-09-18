from collections import deque
from neural_network import NeuralNetwork
import game as Game
import random
import math
import util

class Snake(object):
    def __init__(self, game, brain=NeuralNetwork(util.DEFAULT_INPUT_SIZE,util.DEFAULT_HIDDEN_SIZE,util.DEFAULT_OUTPUT_SIZE)):
        self.cells = deque((-1 for x in range(game.width*game.height)), game.width*game.height)
        self.cells[0] = int((game.height/2)*game.width + game.width/2)
        self.length = 1
        self.game = game # store reference to game info
        self.deferGrow = 0
        self.direction = 26
        self.steps = 0
        self.stepsAway = 0

        self.stepsSinceApple = 0

        # input layer of 21 nodes, hidden layer of 12 nodes, output layer of 4 nodes
        self.brain = brain

    def move(self, direction):
        self.steps += 1
        self.stepsSinceApple += 1

        oldManhattanDistance = util.manhattan(self.cells[0], self.game.applePos, self.game.width)
        nextPos = self.cells[0] # get head
        if direction == 24 and (self.length == 1 or self.direction != 25): #up
            nextPos -= self.game.width
            self.direction = 24
            if nextPos < 0:
                self.game.over = True
                return -1
        elif direction == 25 and (self.length == 1 or self.direction != 24): #down
            nextPos += self.game.width
            self.direction = 25
            if nextPos//self.game.width >= self.game.height:
                self.game.over = True
                return -1
        elif direction == 26 and (self.length == 1 or self.direction != 27): #right
            nextPos += 1
            self.direction = 26
            if nextPos%self.game.width == 0:
                self.game.over = True
                return -1
        elif direction == 27 and (self.length == 1 or self.direction != 26): #left
            nextPos -= 1
            self.direction = 27
            if nextPos%self.game.width == self.game.width-1:
                self.game.over = True
                return -1
        else:
            return self.move(self.direction)
        if self.game.board[nextPos] == Game.SNAKE:
            self.game.over = True
            return -1

        self.cells.appendleft(nextPos)
        newManhattanDistance = util.manhattan(self.cells[0], self.game.applePos, self.game.width)
        if newManhattanDistance > oldManhattanDistance:
            self.stepsAway += 1
        
        if self.deferGrow >= 1:
            self.deferGrow -= 1
            self.length += 1

        # check if we ate apple
        if self.game.board[nextPos] == Game.APPLE:
            self.grow()
            newApple = random.randint(0, self.game.width*self.game.height-1)
            while(self.game.board[newApple] != Game.EMPTY):
                newApple = random.randint(0, self.game.width*self.game.height-1)
            self.game.applePos = newApple
            self.game.score += 100
            self.stepsSinceApple = 0

        # update board
        self.game.board = [Game.EMPTY for _ in range(self.game.width*self.game.height)]
        for i in range(self.length):
            self.game.board[self.cells[i]] = Game.SNAKE
        self.game.board[self.game.applePos] = Game.APPLE

        return 0

    def grow(self):
        if self.length+3 > 300:
            self.length = 300
        if self.cells[self.length] == -1:
            self.deferGrow += 1
        if self.cells[self.length+1] == -1:
            self.deferGrow += 1

        if self.cells[self.length+2] == -1:
            self.deferGrow += 1
        self.length += max(3-self.deferGrow, 0)

    def getInputv2(self):
        result = [0 for _ in range(util.DEFAULT_INPUT_SIZE)]
        #result[0] = util.manhattan(self.cells[0], self.game.applePos, self.game.width)
        result[0] = int(util.isSquareInDirection(self, self.game.applePos, self.direction))
        result[1] = int(util.isSquareInDirection(self, self.game.applePos, util.turnLeft[self.direction]))
        result[2] = int(util.isSquareInDirection(self, self.game.applePos, util.turnRight[self.direction]))
        onceAhead = util.positionOnceTowardsDirection(self.cells[0], self.game, self.direction)
        onceRight = util.positionOnceTowardsDirection(self.cells[0], self.game, util.turnRight[self.direction])
        onceLeft = util.positionOnceTowardsDirection(self.cells[0], self.game, util.turnLeft[self.direction])
        result[3] = 0 if (onceAhead == -1 or self.game.board[onceAhead] == Game.SNAKE) else 1
        result[4] = 0 if (onceLeft == -1 or self.game.board[onceLeft] == Game.SNAKE) else 1
        result[5] = 0 if (onceRight == -1 or self.game.board[onceRight] == Game.SNAKE) else 1
        return [result]

    def getInput(self): 
        result = [0 for _ in range(21)]
        headSquare = self.cells[0]
        appleSquare = self.game.applePos
        result[0] = 2*(abs((headSquare//self.game.width) - (appleSquare//self.game.width)) + abs((headSquare%self.game.width) - (appleSquare%self.game.width)))/(self.game.width+self.game.height) - 1
        result[1] = int((headSquare//self.game.width) < (appleSquare//self.game.width))
        result[2] = int((headSquare//self.game.width) > (appleSquare//self.game.width))
        result[3] = int((headSquare%self.game.width) < (appleSquare%self.game.width))
        result[4] = int((headSquare%self.game.width) > (appleSquare%self.game.width))
        result[5] = 2*(headSquare//self.game.width) / self.game.height - 1
        result[6] = 2*(self.game.height-(headSquare//self.game.width)-1)/ self.game.height - 1
        result[7] = 2*(headSquare%self.game.width)/ self.game.width - 1 
        result[8] = 2*(self.game.width-(headSquare%self.game.width)-1)/self.game.width - 1
        
        # scan up
        i = headSquare-self.game.width
        while(i >= 0):
            if(self.game.board[i] == Game.SNAKE):
                break
            i -= self.game.width
            result[9] += 1
        result[9] = 2*(result[9]/self.game.height) - 1
        # scan down
        i = headSquare+self.game.width
        while(i < self.game.width*self.game.height):
            if(self.game.board[i] == Game.SNAKE):
                break
            i += self.game.width
            result[10] += 1
        result[10] = 2*(result[10]/self.game.height) - 1
        # scan right
        i = headSquare+1
        while(i % self.game.width != 0):
            if(self.game.board[i] == Game.SNAKE):
                break
            i += 1
            result[11] += 1
        result[11] = 2*(result[11]/self.game.width) - 1
        # scan left
        i = headSquare-1
        while(i % self.game.width != self.game.width-1):
            if(self.game.board[i] == Game.SNAKE):
                break
            i -= 1
            result[12] += 1
        result[12] = 2*(result[12]/self.game.width) - 1
        # scan top left
        i = (headSquare-1)-self.game.width
        while(i % self.game.width != self.game.width-1 and i >= 0):
            if(self.game.board[i] == Game.SNAKE):
                break
            i -= (1+self.game.width)
            result[13] += 1
        result[13] = 2*(result[13]/self.game.width) - 1
        # scan top right
        i = (headSquare+1)-self.game.width
        while(i % self.game.width != 0 and i >= 0):
            if(self.game.board[i] == Game.SNAKE):
                break
            i -= (self.game.width - 1)
            result[14] += 1
        result[14] = 2*(result[14]/self.game.height) - 1
        # scan bottom left
        i = (headSquare-1)+self.game.width
        while(i % self.game.width != self.game.width-1 and i < self.game.width*self.game.height):
            if(self.game.board[i] == Game.SNAKE):
                break
            i += (self.game.width - 1)
            result[15] += 1
        result[15] = 2*(result[15]/self.game.height) - 1
        # scan bottom right
        i = (headSquare+1)+self.game.width
        while(i % self.game.width != 0 and i < self.game.width*self.game.height):
            if(self.game.board[i] == Game.SNAKE):
                break
            i += (1+ self.game.width)
            result[16] += 1
        result[16] = 2*(result[16]/self.game.width) - 1

        result[17] = int(self.direction == 24)
        result[18] = int(self.direction == 25)
        result[19] = int(self.direction == 26)
        result[20] = int(self.direction == 27)
        return [result] # represent as a matrix