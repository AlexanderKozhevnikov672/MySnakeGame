import pygame
from enum import Enum


class SnakeDirection(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5


class SnakeStatus(Enum):
    MOVE = 1
    STAY = 2


class Snake():
    kStartSpeed = 10
    kMaxSpeed = 5

    def __init__(self, startPos):
        self.bodyCoords = [startPos]
        self.nowSpeed = self.kStartSpeed
        self.cycleCnt = 0
        self.nowDirection = SnakeDirection.NONE
        self.directionIsSwitched = False

    def updateCycle(self):
        self.trySwitchDirection()
        self.cycleCnt += 1
        if self.cycleCnt == self.nowSpeed:
            self.cycleCnt = 0
            self.directionIsSwitched = False
            if self.nowDirection != SnakeDirection.NONE:
                return SnakeStatus.MOVE
        return SnakeStatus.STAY

    def trySwitchDirection(self):
        if self.directionIsSwitched:
            return
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and not (self.nowDirection in
                                    {SnakeDirection.UP, SnakeDirection.DOWN}):
            self.nowDirection = SnakeDirection.UP
            self.directionIsSwitched = True
            return
        if key[pygame.K_s] and not (self.nowDirection in
                                    {SnakeDirection.UP, SnakeDirection.DOWN}):
            self.nowDirection = SnakeDirection.DOWN
            self.directionIsSwitched = True
            return
        if key[pygame.K_a] and not (self.nowDirection in
                                    {SnakeDirection.LEFT,
                                     SnakeDirection.RIGHT}):
            self.nowDirection = SnakeDirection.LEFT
            self.directionIsSwitched = True
            return
        if key[pygame.K_d] and not (self.nowDirection in
                                    {SnakeDirection.LEFT,
                                     SnakeDirection.RIGHT}):
            self.nowDirection = SnakeDirection.RIGHT
            self.directionIsSwitched = True
            return

    def getNewHeadPos(self):
        if self.nowDirection == SnakeDirection.NONE:
            return self.bodyCoords[0]
        dx, dy = 0, 0
        if self.nowDirection == SnakeDirection.UP:
            dy = -1
        if self.nowDirection == SnakeDirection.DOWN:
            dy = 1
        if self.nowDirection == SnakeDirection.LEFT:
            dx = -1
        if self.nowDirection == SnakeDirection.RIGHT:
            dx = 1
        return (self.bodyCoords[-1][0] + dx, self.bodyCoords[-1][1] + dy)

    def speedUp(self):
        self.nowSpeed = max(self.kMaxSpeed, self.nowSpeed - 1)

    def moveHead(self, newHeadPos):
        self.bodyCoords.append(newHeadPos)

    def pullUpTail(self):
        return self.bodyCoords.pop(0)
