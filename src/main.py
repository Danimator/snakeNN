import pygame
from argparse import ArgumentParser
import sys
from game import Game
from snake import Snake
import generation
import neural_network
import util
import pickle
import time
import datetime

def main():
    game = Game()
    snake = Snake(game)
    if len(sys.argv) == 1:
        print "Running in regular mode"

    else:
        if sys.argv[1] == "watch":
            args = {}
            for arg in sys.argv[2:]:
                split = arg.split('=')
                args[split[0]] = split[1]
            if "name" not in args:
                args["name"] = "."

            snake.brain.ihBias = pickle.load(open("trained_model/"+args["name"]+"/ihBias.pb", "rb"))
            snake.brain.hhBias = pickle.load(open("trained_model/"+args["name"]+"/hhBias.pb", "rb"))
            snake.brain.hoBias = pickle.load(open("trained_model/"+args["name"]+"/hoBias.pb", "rb"))
            snake.brain.ihWeights = pickle.load(open("trained_model/"+args["name"]+"/ihWeights.pb", "rb"))
            snake.brain.hhWeights = pickle.load(open("trained_model/"+args["name"]+"/hhWeights.pb", "rb"))
            snake.brain.hoWeights = pickle.load(open("trained_model/"+args["name"]+"/hoWeights.pb", "rb"))
            pygame.init()
            win = pygame.display.set_mode((720, 480))
            pygame.display.set_caption("Snake Neural Network - Watching")
            clock = pygame.time.Clock()

            snake.brain.play(win, True)
            pygame.quit()
            return
            
        elif sys.argv[1] == "train":
            args = {}
            for arg in sys.argv[2:]:
                split = arg.split('=')
                args[split[0]] = split[1]
            if "name" not in args:
                args["name"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            if "pop" not in args:
                args["pop"] = 80
            else:
                args["pop"] = int(args["pop"])
            if "gen" not in args:
                args["gen"] = 1000
            else:
                args["gen"] = max(int(args["gen"]), 4)
            if "display" not in args:
                args["display"] = 0
            else:
                args["display"] = int(args["display"])

            gen = generation.Generation(args["pop"], util.DEFAULT_INPUT_SIZE, util.DEFAULT_HIDDEN_SIZE , util.DEFAULT_OUTPUT_SIZE)
            for _ in range(args["gen"]):
                gen.train(args["name"], None)
                gen.saveBestGenomes()
                gen.mutate()
            print("Training completed")
            return




    pygame.init()
    win = pygame.display.set_mode((980, 480))
    pygame.display.set_caption("Snake Neural Network - Regular")
    clock = pygame.time.Clock()

    while not game.over:
        clock.tick(20)
        movedirection = snake.direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movedirection = 27
                elif event.key == pygame.K_RIGHT:
                    movedirection = 26
                elif event.key == pygame.K_UP:
                    movedirection = 24
                elif event.key == pygame.K_DOWN:
                    movedirection = 25
            if game.board[util.positionOnceTowardsDirection(snake.cells[0], game, finalDirection)] == 2:
                print("Snake's score is now {}, length {}".format(game.score+100, snake.length+3))
        snake.move(movedirection)

        win.fill((0,0,0))
        game.display(win)
        pygame.display.update()
    print("You ended with a score of {}".format(score))
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()