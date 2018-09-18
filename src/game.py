import pygame
import random
import snake

EMPTY = 0
SNAKE = 1
APPLE = 2
X = 0
Y = 1

# Stores 'board' representation
class Game(object):
    def __init__(self):
        self.width = 60
        self.height = 40
        self.board = [EMPTY for _ in range(0, self.width*self.height)]
        self.applePos = random.randint(0, self.width*self.height-1)
        self.over = False
        # ensure apple does not start at snake pos
        while self.applePos == int((self.height/2)*self.width + self.width/2):
            self.applePos = random.randint(0, self.width*self.height-1)
        self.board[self.applePos] = APPLE
        self.score = 0

    def display(self, win):
        for rowNum in range(self.height):
            for colNum in range(self.width):
                if self.board[rowNum*self.width + colNum] == SNAKE:
                    pygame.draw.rect(win, (255, 255, 255), (colNum*12+1, rowNum*12+1, 10, 10))
                elif self.board[rowNum*self.width + colNum] == APPLE:
                    pygame.draw.rect(win, (255, 0, 0), (colNum*12+1, rowNum*12+1, 10, 10))
        pygame.draw.rect(win, (255,255,255), (self.width*12, 0, 300, self.height*12))
        pygame.draw.rect(win, (255,255,255), (0, self.height*12, self.width*12, 2))