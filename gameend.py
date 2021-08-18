import pygame  # 8/10
from settings import WIN_WIDTH, WIN_HEIGHT
from menu.menus import Button

NEXT2_IMAGE = pygame.transform.scale(pygame.image.load("images/LEVEL02-loading.png"), (WIN_WIDTH, WIN_HEIGHT))
NEXT3_IMAGE = pygame.transform.scale(pygame.image.load("images/LEVEL03-loading.png"), (WIN_WIDTH, WIN_HEIGHT))
GAMEWIN_IMAGE = pygame.transform.scale(pygame.image.load("images/WIN.png"), (WIN_WIDTH, WIN_HEIGHT))
RERUN_IMAGE = pygame.transform.scale(pygame.image.load("images/button-replay.png"), (200, 80))
NEXT_IMAGE = pygame.transform.scale(pygame.image.load("images/button-next.png"), (200, 80))


class GameEnd:
    def run(self, quit, level, sound):
        self.rerun = Button(RERUN_IMAGE, "rerun", 200, 540)
        if level < 3:  # 之後要改成 3
            self.next = Button(NEXT_IMAGE, "next", 200, 460)
        if sound == True:
            pygame.mixer.music.load("./sound/win.mp3")  #8/18
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        while 1:
            self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
            if level == 1:
                self.win.blit(NEXT2_IMAGE, (0, 0))
                self.win.blit(NEXT_IMAGE, (100, 420))
            elif level == 2:
                self.win.blit(NEXT3_IMAGE, (0, 0))
                self.win.blit(NEXT_IMAGE, (100, 420))
            else:
                self.win.blit(GAMEWIN_IMAGE, (0, 0))
            self.win.blit(RERUN_IMAGE, (100, 500))

            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.QUIT:
                    quit = True
                    return quit, level
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.rerun.clicked(x, y):
                        if level == 3:
                            level =1
                        return quit, level
                    if level < 3:  # 之後要改成 3
                        if self.next.clicked(x, y):
                            level += 1
                            return quit, level