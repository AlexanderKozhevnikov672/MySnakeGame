import pygame


class Snake():
    kStartSpeed = 10
    kMaxSpeed = 5

    def __init__(self, startPos):
        self.bodyCoords = [startPos]
        self.nowSpeed = self.kStartSpeed
        self.cycleCnt = 0
        self.nowDirection = 'NS'
        self.directionIsSwitched = False

    def updateCycle(self):
        self.trySwitchDirection()
        self.cycleCnt += 1
        if self.cycleCnt == self.nowSpeed:
            self.cycleCnt = 0
            self.directionIsSwitched = False
            if self.nowDirection != 'NS':
                return 'Move'
        return 'Stay'

    def trySwitchDirection(self):
        if self.directionIsSwitched:
            return
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and not (self.nowDirection in {'W', 'S'}):
            self.nowDirection = 'W'
            self.directionIsSwitched = True
            return
        if key[pygame.K_s] and not (self.nowDirection in {'W', 'S'}):
            self.nowDirection = 'S'
            self.directionIsSwitched = True
            return
        if key[pygame.K_a] and not (self.nowDirection in {'A', 'D'}):
            self.nowDirection = 'A'
            self.directionIsSwitched = True
            return
        if key[pygame.K_d] and not (self.nowDirection in {'A', 'D'}):
            self.nowDirection = 'D'
            self.directionIsSwitched = True
            return

    def getNewHeadPos(self):
        if self.nowDirection == 'NS':
            return self.bodyCoords[0]
        dx, dy = 0, 0
        if self.nowDirection == 'W':
            dy = -1
        if self.nowDirection == 'S':
            dy = 1
        if self.nowDirection == 'A':
            dx = -1
        if self.nowDirection == 'D':
            dx = 1
        return (self.bodyCoords[-1][0] + dx, self.bodyCoords[-1][1] + dy)

    def speedUp(self):
        self.nowSpeed = max(self.kMaxSpeed, self.nowSpeed - 1)

    def moveHead(self, newHeadPos):
        self.bodyCoords.append(newHeadPos)

    def pullUpTail(self):
        return self.bodyCoords.pop(0)
