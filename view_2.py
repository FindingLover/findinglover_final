#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import random
import enemy.enemies
from settings import WIN_WIDTH, WIN_HEIGHT, HP_IMAGE, HP_GRAY_IMAGE, BACKGROUND_IMAGE_2
from color_settings import *
from menu.menus import music_button_image, muse_button_image, boy_cry_image, girl_cry_image
from enemy.enemies import EnemyGroup

#love
LOVE_GRAY_IMAGE = pygame.transform.scale(pygame.image.load("images/love_gray.png"), (28, 26))
LOVE_IMAGE = pygame.transform.scale(pygame.image.load("images/love.png"), (28, 26))
ATTACK_IMAGE = pygame.transform.scale(pygame.image.load("images/attack-02.png"), (20, 20))
class GameView2:
    def __init__(self):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.font = pygame.font.SysFont("arial",24)

        self.text_cd = 0
        self.r = random.randint(0, 7)
    def draw_bg(self):
        self.win.blit(BACKGROUND_IMAGE_2, (0, 0))
    #8/11
    def draw_cry(self):
        self.win.blit(boy_cry_image, (810, 155))
        self.win.blit(girl_cry_image, (480, 30))

        # 8/17

    def draw_text(self, text):
        if text == ' ':
            text = 'honey'
        self.text_cd += 1
        if self.text_cd == 120:
            self.r = random.randint(0, 7)
            self.text_cd = 0
        pygame.draw.rect(self.win, (205, 175, 149), [495, 130, 480, 55])
        if self.r == 0:
            message = 'Click \'+\' to build the tower that can against viruses !!'
        if self.r == 1:
            message = 'The  mask  can  make  a  virus  stop  walking.'
        if self.r == 2:
            message = 'All towers with blue circle can be upgraded till 4 level.'
        if self.r == 3:
            message = 'Click  \'love  buttons\'  to  get  hearts.'
        if self.r == 4:
            message = 'Fighting  ~  <3  <3'
        if self.r == 5:
            message = 'Please  be  careful  and  be  healthy ! !'
        if self.r == 6:
            message = 'I  miss  you  so  much  <3'
        if self.r == 7:
            message = 'Go  Go  Go  ~  ~  <3'

        name = self.font.render(f"Dear   my   {text}    :  )", True, (139, 69, 19))
        m = self.font.render(message, True, (139, 69, 19))
        self.win.blit(name, (515, 130))
        self.win.blit(m, (515, 155))

    def draw_sound(self):  # 8/17
        self.win.blit(music_button_image, (815, 525))

    def draw_muse(self):
        self.win.blit(muse_button_image, (815, 525))

    def draw_towers(self, towers):
        # draw tower
        for tw in towers:
            self.win.blit(tw.image, tw.rect)

    def draw_enemies(self, enemies):
        for en in enemies.get():
            self.win.blit(en.image, en.rect)
            # draw health bar
            bar_width = en.rect.w * (en.health / en.max_health) *0.77
            max_bar_width = en.rect.w *0.77
            bar_height = 5
            pygame.draw.rect(self.win, RED, [en.rect.x+3, en.rect.y - 10, max_bar_width, bar_height])
            pygame.draw.rect(self.win, GREEN, [en.rect.x+3, en.rect.y - 10, bar_width, bar_height])

    def draw_range(self, selected_tower):
        # draw tower range
        if selected_tower is not None:
            tw = selected_tower
            # create a special surface that is able to render semi-transparent image
            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            transparency = 120
            pygame.draw.circle(surface, (128, 128, 128, transparency), tw.rect.center, tw.range)
            self.win.blit(surface, (0, 0))

    def draw_menu(self, menu):
        self.win.blit(menu.image, menu.rect)
        for btn in menu.buttons:
            self.win.blit(btn.image, btn.rect)

    def draw_lovemenu(self, lovemenu): #love
        for btn in lovemenu.buttons:
            self.win.blit(btn.image, btn.rect)

    def draw_plots(self, plots):
        for pt in plots:
            self.win.blit(pt.image, pt.rect)

    def draw_money(self, money: int):
        """ (Q2.1)render the money"""
        pygame.draw.rect(self.win, (205,175 ,149), [1024-220, 520, 220,80])
        text = self.font.render(f"Money: {money}", True, (139,69 ,19))
        self.win.blit(text, (1024-115, 565))

    def draw_wave(self, wave: int):
        """(Q2.2)render the wave"""
        text = self.font.render(f"Wave: {wave}/4", True, (139,69 ,19))
        self.win.blit(text, (1024-115, 535))


    def draw_hp(self, lives):
        # draw_lives
        hp_rect = HP_IMAGE.get_rect()
        for i in range(9):
            self.win.blit(HP_GRAY_IMAGE, (619+39 * ( i % 9 ),45))

        for i in range(lives):
            self.win.blit(HP_IMAGE,(619+39 * ( i % 9 ),45))



    def draw_love_grade(self, love_grade): #love
        love_rect = LOVE_IMAGE.get_rect()
        for i in range(7):
            self.win.blit(LOVE_GRAY_IMAGE, (632.5+ 50.7* ( i % 7), 90))
        for i in range(love_grade):
            self.win.blit(LOVE_IMAGE, (632.5+ 50.7* ( i % 7), 90))

    # 8/17
    def draw_love_information(self, hoverbutton):
        informationfont = pygame.font.SysFont("arial", 20)
        x, y = (830, 485)
        if hoverbutton is not None:
            pygame.draw.rect(self.win, (98, 91, 87), [x + 20, y - 60, 160, 90])
            if hoverbutton == "hearthover":
                text = informationfont.render(f"get one heart", True, WHITE)
                text2 = informationfont.render(f"FREE", True, WHITE)
                text3 = informationfont.render(f"4 seconds preparing", True, WHITE)
                self.win.blit(text, (x + 48, y - 58))
                self.win.blit(text2, (x + 80, y - 28))
                self.win.blit(text3, (x + 26, y + 2))
            elif hoverbutton == "loveletterhover":
                text = informationfont.render(f"get three hearts", True, WHITE)
                text2 = informationfont.render(f"$150", True, WHITE)
                text3 = informationfont.render(f"10 seconds preparing", True, WHITE)
                self.win.blit(text, (x + 42, y - 58))
                self.win.blit(text2, (x + 82, y - 28))
                self.win.blit(text3, (x + 24, y + 2))

    # 8/17
    def draw_tower_information(self, hoverbutton, hovertower, hoverplot):
        informationfont = pygame.font.SysFont("arial", 20)

        if hovertower is not None:
            x, y = hovertower.rect.center
            if hoverbutton is not None:
                pygame.draw.rect(self.win, (98, 91, 87), [x + 20, y - 60, 120, 120])
                pygame.draw.rect(self.win, (255, 255, 255), [x + 23, y - 57, 114, 114])
                if hoverbutton == "sellhover":
                    text = informationfont.render(f"money : +{hovertower.get_cost()}", True, (98, 91, 87))
                    self.win.blit(text, (x + 26, y - 58))
                elif hoverbutton == "upgradehover":
                    if hovertower.level < 3:
                        text1 = informationfont.render(f"money : -{hovertower.get_upgrade_cost()}", True, (98, 91, 87))
                        self.win.blit(text1, (x + 26, y - 58))
                        text2 = informationfont.render(f"damage : +{hovertower.upgrade_damage}", True, (98, 91, 87))
                        self.win.blit(text2, (x + 26, y - 28))
                        text3 = informationfont.render(f"range : +{hovertower.upgrade_range}", True, (98, 91, 87))
                        self.win.blit(text3, (x + 26, y + 2))
                    else:
                        text1 = informationfont.render(f"Max Level", True, (98, 91, 87))
                        self.win.blit(text1, (x + 26, y - 58))

        elif hoverplot is not None:
            x, y = hoverplot.rect.center
            if hoverbutton is not None:
                pygame.draw.rect(self.win, (98, 91, 87), [x + 20, y - 60, 120, 120])
                pygame.draw.rect(self.win, (255, 255, 255), [x + 23, y - 57, 114, 114])
                if hoverbutton == "health foodhover":
                    text1 = informationfont.render(f"AOE attack", True, (98, 91, 87))
                    self.win.blit(text1, (x + 26, y - 58))
                    text2 = informationfont.render(f"damage : 1.5", True, (98, 91, 87))
                    self.win.blit(text2, (x + 26, y - 28))
                    text3 = informationfont.render(f"range : 120", True, (98, 91, 87))
                    self.win.blit(text3, (x + 26, y + 2))
                    text4 = informationfont.render(f"money : -80", True, (98, 91, 87))
                    self.win.blit(text4, (x + 26, y + 32))
                elif hoverbutton == "alcoholhover":
                    text1 = informationfont.render(f"Single attack", True, (98, 91, 87))
                    self.win.blit(text1, (x + 26, y - 58))
                    text2 = informationfont.render(f"damage : 2.0", True, (98, 91, 87))
                    self.win.blit(text2, (x + 26, y - 28))
                    text3 = informationfont.render(f"range : 150", True, (98, 91, 87))
                    self.win.blit(text3, (x + 26, y + 2))
                    text4 = informationfont.render(f"money : -80", True, (98, 91, 87))
                    self.win.blit(text4, (x + 26, y + 32))
                elif hoverbutton == "vaccinehover":
                    text1 = informationfont.render(f"Snipe attack", True, (98, 91, 87))
                    self.win.blit(text1, (x + 26, y - 58))
                    text2 = informationfont.render(f"damage : kill 1", True, (98, 91, 87))
                    self.win.blit(text2, (x + 26, y - 28))
                    text3 = informationfont.render(f"range : 110", True, (98, 91, 87))
                    self.win.blit(text3, (x + 26, y + 2))
                    text4 = informationfont.render(f"money : -110", True, (98, 91, 87))
                    self.win.blit(text4, (x + 26, y + 32))
                elif hoverbutton == "maskhover":
                    text1 = informationfont.render(f"Stop 1 enemy", True, (98, 91, 87))
                    self.win.blit(text1, (x + 26, y - 58))
                    text2 = informationfont.render(f"money : -110", True, (98, 91, 87))
                    self.win.blit(text2, (x + 26, y - 28))
                    text3 = informationfont.render(f"last 7 second", True, (98, 91, 87))
                    self.win.blit(text3, (x + 26, y + 2))
                elif hoverbutton == "isolatehover":
                    text1 = informationfont.render(f"Slow all enemy", True, (98, 91, 87))
                    self.win.blit(text1, (x + 26, y - 58))
                    text2 = informationfont.render(f"money : -110", True, (98, 91, 87))
                    self.win.blit(text2, (x + 26, y - 28))
                    text3 = informationfont.render(f"last 7 second", True, (98, 91, 87))
                    self.win.blit(text3, (x + 26, y + 2))

    def draw_attack(self, position):  # 8/17
        if position:
            for pt in position:
                self.win.blit(ATTACK_IMAGE, pt)
    def draw_aoe(self, towers):
        if towers:
            for tw in towers:
                x, y = tw.rect.center
                surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
                transparency = 100
                pygame.draw.circle(surface, (255, 255, 255, transparency), (x, y), tw.range)
                pygame.draw.rect(surface, (255, 0, 0, transparency), [x - 20, y - 100, 40, 200])
                pygame.draw.rect(surface, (255, 0, 0, transparency), [x - 100, y - 20, 200, 40])
                self.win.blit(surface, (0, 0))