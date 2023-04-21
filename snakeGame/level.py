import pygame
import random
from snake import Snake, SnakeStatus
from enum import Enum


class LevelStatus(Enum):
    BUMPED = 1
    ATE_APPLE = 2


class GameStatus(Enum):
    PLAY_LEVEL = 1
    QUIT_LEVEL = 2
    SHOW_MENU = 3
    QUIT_GAME = 4


class Level():
    kFieldSize = 20
    kCellSize = 50
    kFPS = 30

    def __init__(self, wallCoords=set()):
        self.wallCoords = wallCoords
        self.freeCells = set((x, y) for x in range(self.kFieldSize)
                             for y in range(self.kFieldSize)) - self.wallCoords
        startPos = random.choice(list(self.freeCells))
        self.snake = Snake(startPos)
        self.freeCells.discard(startPos)
        self.placeApple()
        self.score = 0

    def placeApple(self):
        if len(self.freeCells) == 0:
            self.appleCoords = (self.kFieldSize, self.kFieldSize)
            return
        self.appleCoords = random.choice(list(self.freeCells))
        self.freeCells.discard(self.appleCoords)

    def tryCloseLevel(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameStatus.QUIT_GAME
        key = pygame.key.get_pressed()
        if key[pygame.K_b]:
            return GameStatus.QUIT_LEVEL
        return GameStatus.PLAY_LEVEL

    def updateSnakeMove(self, newSnakeHeadPos):
        if not (newSnakeHeadPos in self.freeCells) and\
              newSnakeHeadPos != self.appleCoords:
            return LevelStatus.BUMPED
        self.snake.moveHead(newSnakeHeadPos)
        if newSnakeHeadPos == self.appleCoords:
            self.placeApple()
            self.snake.speedUp()
            return LevelStatus.ATE_APPLE
        self.freeCells.add(self.snake.pullUpTail())
        self.freeCells.discard(newSnakeHeadPos)

    def getSquareParametrs(self, coord):
        return (coord[0] * self.kCellSize, coord[1] * self.kCellSize,
                self.kCellSize - 1, self.kCellSize - 1)

    def drawApple(self, surface, color):
        pygame.draw.rect(surface, pygame.Color(color),
                         self.getSquareParametrs(self.appleCoords))

    def drawSnake(self, surface, headColor, tailColor):
        for bodyCoord in self.snake.bodyCoords[:-1]:
            pygame.draw.rect(surface, pygame.Color(tailColor),
                             self.getSquareParametrs(bodyCoord))
        pygame.draw.rect(surface, pygame.Color(headColor),
                         self.getSquareParametrs(self.snake.bodyCoords[-1]))

    def drawWalls(self, surface, color):
        for wallCoord in self.wallCoords:
            pygame.draw.rect(surface, pygame.Color(color),
                             self.getSquareParametrs(wallCoord))

    def showFinalScore(self, surface, color):
        scoreFont = pygame.font.SysFont('Arial', 75, bold=True)
        scoreRender = scoreFont.render(f'Game Over! Your score: {self.score}',
                                       1, pygame.Color(color))
        surface.blit(scoreRender, (0, self.kFieldSize // 2 * self.kCellSize))
        pygame.display.flip()

    def play(self):
        surface = pygame.display.set_mode([self.kFieldSize * self.kCellSize,
                                           self.kFieldSize * self.kCellSize])
        clock = pygame.time.Clock()

        quitResult = GameStatus.PLAY_LEVEL
        while quitResult == GameStatus.PLAY_LEVEL:
            surface.fill(pygame.Color('blue'))
            self.drawApple(surface, 'red')
            self.drawSnake(surface, 'gold', 'green')
            self.drawWalls(surface, 'gray')
            pygame.display.flip()

            clock.tick(self.kFPS)

            if self.snake.updateCycle() == SnakeStatus.MOVE:
                newSnakeHeadPos = tuple(
                    [c % self.kFieldSize for c in self.snake.getNewHeadPos()])
                moveResult = self.updateSnakeMove(newSnakeHeadPos)
                if moveResult == LevelStatus.BUMPED:
                    self.showFinalScore(surface, 'cyan')
                    break
                if moveResult == LevelStatus.ATE_APPLE:
                    self.score += 1

            quitResult = self.tryCloseLevel()

        while quitResult == GameStatus.PLAY_LEVEL:
            clock.tick(self.kFPS)

            quitResult = self.tryCloseLevel()

        return (quitResult, self.score)
