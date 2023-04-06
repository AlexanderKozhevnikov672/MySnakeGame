import pygame
from level import Level


class Game():
    kLevelsCnt = 5
    kMenuLength = 500
    kMenuWidth = 300

    def __init__(self):
        file = open('levelsInfo/levelsRecords.txt', 'r')
        self.levelsRecords = [int(line) for line in file]
        file.close()

    def updateFileLevelsRecords(self):
        file = open('levelsInfo/levelsRecords.txt', 'w')
        for i in range(self.kLevelsCnt):
            file.write(str(self.levelsRecords[i]) + '\n')
        file.close()

    def getLevelNum(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            return 1
        if key[pygame.K_2]:
            return 2
        if key[pygame.K_3]:
            return 3
        if key[pygame.K_4]:
            return 4
        if key[pygame.K_5]:
            return 5
        if key[pygame.K_q]:
            return 'QuitGame'
        return 0

    def tryCloseGame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QuitGame'
        return 'StillInMenu'

    def printMenu(self):
        surface = pygame.display.set_mode([self.kMenuLength, self.kMenuWidth])
        surface.fill('yellow')
        color = 'black'
        menuFont = pygame.font.SysFont('Arial', 50, bold=True)
        menuRender = menuFont.render('Choose Level:', 1, pygame.Color(color))
        surface.blit(menuRender, (0, 0))
        kStringWidth = 50
        for i in range(self.kLevelsCnt):
            message = f'{i + 1} - Best Score: {self.levelsRecords[i]}'
            menuRender = menuFont.render(message, 1, pygame.Color(color))
            surface.blit(menuRender, (kStringWidth, (i + 1) * kStringWidth))
        pygame.display.flip()

    def getWallCoords(self, levelNum):
        file = open(f'levelsInfo/level{levelNum}wallsCoords.txt', 'r')
        wallsCoords = set([tuple(map(int, line.split())) for line in file])
        file.close()
        return wallsCoords

    def start(self):
        pygame.init()
        clock = pygame.time.Clock()

        quitResult = 'StillInMenu'
        while quitResult != 'QuitGame':
            self.printMenu()

            kFPS = 30
            clock.tick(kFPS)

            levelNum = self.getLevelNum()
            if levelNum == 'QuitGame':
                quitResult = 'QuitGame'
            elif levelNum != 0:
                quitResult, score = Level(self.getWallCoords(levelNum)).play()
                self.levelsRecords[levelNum - 1] = max(
                    self.levelsRecords[levelNum - 1], score)

            if quitResult != 'QuitGame':
                quitResult = self.tryCloseGame()

        self.updateFileLevelsRecords()
        pygame.quit()
