import pygame
import os

from game.game import Game
from color_settings import *
from settings import WIN_WIDTH, WIN_HEIGHT, FPS
from game.game import Game
from menu.menus import music_button_image, muse_button_image
from game.gameover import GameOver  # 8/9

known_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "COVER-button-gotit.png")), (182, 76))
class Demo:
    def __init__(self):
        self.demo_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "COVER-guide.png")),
                                         (WIN_WIDTH, WIN_HEIGHT))
        # button
        self.known_btn = Buttons(800, 500, 182, 76)
        self.sound_btn = Buttons(70, 525, 90, 70)
        self.buttons = [self.sound_btn,
                        self.known_btn,]

        # music and sound
        self.sound = pygame.mixer.Sound("./sound/sound.mp3")
        self.sound.set_volume(0.1)

    def play_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def demo_run(self, music):
        run = True
        if music == True:
            self.play_music()
        while run:
            self.demo_win.blit(self.bg, (0, 0))
            self.demo_win.blit(known_image, (800, 500))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound_btn.clicked(x, y):  # 如果按下聲音紐
                        music = not music
                    if self.known_btn.clicked(x, y):  # start
                        if music == True:
                            self.sound.play()
                        return music

            for button in self.buttons:  # 一一判斷每個button
                button.create_frame(x, y)  # 創造框框(滑鼠是否在按鈕上的判斷已在函式內了)
                button.draw_frame(self.demo_win)  # 印出框框

            if music == False:
                pygame.mixer.music.pause()
                self.demo_win.blit(muse_button_image, (70, 525))
            elif music == True:
                pygame.mixer.music.unpause()
                self.demo_win.blit(music_button_image, (70, 525))

            pygame.display.update()
        return music


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
