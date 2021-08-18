import pygame  # 8/10
from settings import WIN_WIDTH, WIN_HEIGHT
from menu.menus import Button
GAMEOVER_IMAGE = pygame.transform.scale(pygame.image.load("images/gameover.png"), (WIN_WIDTH, WIN_HEIGHT))
RERUN_IMAGE = pygame.transform.scale(pygame.image.load("images/again.png"), (246, 100))

class GameOver:
    def run(self, quit, sound):
        self.rerun = Button(RERUN_IMAGE, "rerun", 503, 500)  # 8/17
        stop = False
        if sound == True:
            pygame.mixer.music.load("./sound/lose.mp3")    #8/18
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        while not stop:
            self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
            self.win.blit(GAMEOVER_IMAGE, (0, 0))
            self.win.blit(RERUN_IMAGE, (380, 450))
            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.QUIT:
                    quit = True
                    return quit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.rerun.clicked(x, y):
                        stop = True