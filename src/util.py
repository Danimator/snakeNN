import math
import numpy
import random
import copy

UP = 24
DOWN = 25
RIGHT = 26
LEFT = 27

turnRight = {
    UP: RIGHT,
    DOWN: LEFT,
    RIGHT: DOWN,
    LEFT: UP
}

turnLeft = {
    UP: LEFT,
    DOWN: RIGHT,
    RIGHT: UP,
    LEFT: DOWN
}

def isSquareInDirection(snake, sq, direction):
    assert turnRight[direction] is not None
    headSq = snake.cells[0]
    
    if direction == UP:
        return sq//(snake.game.width) < headSq//snake.game.width
    elif direction == DOWN:
        return sq//(snake.game.width) > headSq//snake.game.width
    elif direction == RIGHT:
        return sq%snake.game.width > headSq%snake.game.width
    return sq%snake.game.width < headSq%snake.game.width

def positionOnceTowardsDirection(sq, game, direction):
    if direction == UP and (sq-game.width) >= 0:
        return sq - game.width
    elif direction == DOWN and (sq+game.width) < game.width*game.height:
        return sq + game.width
    elif direction == RIGHT and (sq+1)%game.width != 0:
        return sq + 1
    elif direction == LEFT and (sq-1)%game.width != game.width-1:
        return sq - 1
    else:
        return -1

DEFAULT_INPUT_SIZE = 6
DEFAULT_HIDDEN_SIZE = 9
DEFAULT_OUTPUT_SIZE = 3


def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# Utility function to calculate dot product
def dot(m1, m2):
    result_rows = len(m1)
    result_cols = len(m2[0])
    m1cols = len(m1[0])
    m2rows = len(m2)
    assert m1cols == m2rows

    result = [
        [0 for _ in range(result_cols)] for _ in range(result_rows)
    ]
    for row in range(result_rows):
        for col in range(result_cols):
            for i in range(m1cols):
                result[row][col]  += m1[row][i] * m2[i][col]

    return result

# Utility function to add matrices
def add(m1, m2):
    result_rows = len(m1)
    result_cols = len(m1[0])
    assert result_rows == len(m2)
    assert result_cols == len(m1[0])
    return [[m1[i][j] + m2[i][j] for j in range(result_cols)] for i in range(result_rows)]


def gaussianMutate(m1):
    return [[(max(min(m1[j][i] + numpy.random.normal()/5, 1), -1) if (random.uniform(0, 1) < 0.2) else m1[j][i]) for i in range(len(m1[0]))] for j in range(len(m1))]

def crossover(m1, m2):
    rows = len(m1)
    cols = len(m1[0])
    assert rows == len(m2)
    assert cols == len(m2[0])
    length = rows*cols
    x = random.randint(0, length)
    return [
        [(m1[j][i] if (j*cols+i < x) else m2[j][i]) for i in range(cols)] for j in range(rows)
    ]

def manhattan(sq1, sq2, boardWidth):
    return (abs((sq1//boardWidth) - (sq2//boardWidth)) + abs((sq1%boardWidth) - (sq2%boardWidth)))

def decipherInput(result):
    print("Manhattan distance:", result[0])
    print("Above apple?:", result[1])
    print("Below apple?:", result[2])
    print("Left of apple?:", result[3])
    print("Right of apple?:", result[4])
    print("Distance from top wall:", result[5])
    print("Distance from bottom wall:", result[6])
    print("Distance from left wall:", result[7])
    print("Distance from right wall:", result[8])
    print("Distance above self from bad square:", result[9])
    print("Distance below self from bad square:", result[10])
    print("Distance left of self from bad square:", result[11])
    print("Distance right of self from bad square:", result[12])
    print("Distance top left of self from bad square:", result[13])
    print("Distance top right of self from bad square:", result[14])
    print("Distance bottom left of self from bad square:", result[15])
    print("Distance bottom right of self from bad square:", result[16])
    print("Moving up?:", result[17])
    print("Moving down?:", result[18])
    print("Moving right?:", result[19])
    print("Moving left?:", result[20])
    