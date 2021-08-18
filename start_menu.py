import pygame
import os
from game.game import Game
from color_settings import *
from settings import WIN_WIDTH, WIN_HEIGHT, FPS
from menu.menus import music_button_image,muse_button_image
from game.gameover import GameOver   #8/9
from demo import Demo

pygame.init()
pygame.mixer.init()


class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # background
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "start_menu.png")), (WIN_WIDTH, WIN_HEIGHT))
        self.v1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "trailer-01.png")),
                                         (WIN_WIDTH, WIN_HEIGHT))
        self.v2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "trailer-02.png")),
                                         (WIN_WIDTH, WIN_HEIGHT))
        self.v3 = pygame.transform.scale(pygame.image.load(os.path.join("images", "trailer-03.png")),
                                         (WIN_WIDTH, WIN_HEIGHT))
        self.v4 = pygame.transform.scale(pygame.image.load(os.path.join("images", "trailer-04.png")),
                                         (WIN_WIDTH, WIN_HEIGHT))

        # button
        self.start_btn = Buttons(232,375,206,104)
        self.sound_btn = Buttons(70, 525, 90, 70)
        self.mute_btn = Buttons(70, 525, 90, 70)#175
        self.buttons = [self.sound_btn,
                        self.mute_btn,
                        self.start_btn,]

        # music and sound
        self.sound = pygame.mixer.Sound("./sound/sound.mp3")
        self.sound.set_volume(0.1)
        self.video = True ###################################################################
        self.video_count = 0

    def play_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        
    def play_video(self):  #8/17
        self.video_count += 1
        if self.video_count < 120:
            self.menu_win.blit(self.v1, (0, 0))
        elif self.video_count < 320:
            self.menu_win.blit(self.v2, (0, 0))
        elif self.video_count < 520:
            self.menu_win.blit(self.v3, (0, 0))
        elif self.video_count < 720:
            self.menu_win.blit(self.v4, (0, 0))
        else:
            return not self.video

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("Finding Lover")
        self.play_music()
        music = True
        k = 1  # 8/17
        game = Game()  # 8/17

        while run:
            clock.tick(FPS)

            if k == 1:
                game.name()
                k += 1
                self.video_count = 0
            x, y = pygame.mouse.get_pos()

            if self.video != False:
                self.video = self.play_video()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.sound_btn.clicked(x,y):   #如果按下聲音紐
                            music = not music
            else:
                self.menu_win.blit(self.bg, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.sound_btn.clicked(x, y):  # 如果按下聲音紐
                            music = not music
                        if self.start_btn.clicked(x, y):  # start
                            if music == True:
                                self.sound.play()
                            demo = Demo()
                            music = demo.demo_run(music)  # 8/17
                            game.run(music)  #8/17
                            run = False

                for button in self.buttons:  # 一一判斷每個button
                    button.create_frame(x, y)  # 創造框框(滑鼠是否在按鈕上的判斷已在函式內了)
                    button.draw_frame(self.menu_win)  # 印出框框

            if music == False:
                pygame.mixer.music.pause()
                self.menu_win.blit(muse_button_image, (70, 525))
            elif music == True:
                pygame.mixer.music.unpause()
                self.menu_win.blit(music_button_image, (70, 525))

            pygame.display.update()
        pygame.quit()








class Buttons:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.frame = None

    def clicked(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True
        return False

    def create_frame(self, x: int, y: int):
        """if cursor position is on the button, create button frame"""
        if self.clicked(x, y):
            x, y, w, h = self.rect
            self.frame = pygame.Rect(x - 5, y - 5, w + 10, h + 10)
        else:
            self.frame = None

    def draw_frame(self, win):
        if self.frame is not None:
            pygame.draw.rect(win, (215, 155, 155), self.frame, 10)
