#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import os
from tower.towers import Tower, Vacancy, BlockVacancy
from enemy.enemies3 import EnemyGroup,Enemy
from menu.menus import UpgradeMenu, BuildMenu, MainMenu, BlockMenu, LoveMenu
from game.user_request import RequestSubject, TowerFactory, TowerSeller, TowerDeveloper, EnemyGenerator, Music, HeartDeveloper, LoveletterDeveloper
from settings import WIN_WIDTH, WIN_HEIGHT, BACKGROUND_IMAGE_3
from menu.menus import UpgradeMenu, BuildMenu, MainMenu, LoveMenu


class GameModel3:
    def __init__(self):
        #self.wave = 0
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE_3, (WIN_WIDTH, WIN_HEIGHT))
        self.__towers = []   #改名字
        #self.__enemies = EnemyGroup(self.wave)
        self.__enemies = EnemyGroup()
        self.__menu = None
        self.__main_menu = MainMenu()
        self._love_menu = LoveMenu()  # love
        self.__plots = [Vacancy(262, 247), Vacancy(150, 114), Vacancy(147, 312), Vacancy(388, 369),
                        Vacancy(504, 253), Vacancy(594, 447), Vacancy(663, 322),   #final
                        Vacancy(314, 103), Vacancy(701, 495),
                        BlockVacancy(139, 70), BlockVacancy(134, 266), BlockVacancy(456, 316), BlockVacancy(727, 229),
                        BlockVacancy(638, 439)]  # 8/17
        self.selected_plot = None
        self.selected_tower = None
        self.selected_button = None
        
        self.subject = RequestSubject(self)
        self.seller = TowerSeller(self.subject)
        self.developer = TowerDeveloper(self.subject)

        self.loveletter_developer = LoveletterDeveloper(self.subject) #love
        self.heartdeveloper = HeartDeveloper(self.subject) #love

        self.factory = TowerFactory(self.subject)
        self.generator = EnemyGenerator(self.subject)
        # 8/17
        self.music = Music(self.subject)
        self.music_or_not = True

        self.wave = 0
        self.money = 500
        self.money = 500
        self.max_hp = 9
        self.hp = self.max_hp
        self.max_love_grade = 7  #戀愛指數滿分10 #更改
        self.love_grade = self.max_love_grade  #戀愛指數初始10
        self.loss_love_count = 0
        self.loss_max_count = 300

        self.hover = None  # 8/15
        self.lovehover = None  # 8/17
        self.sound = pygame.mixer.Sound(os.path.join("sound", "sound.mp3"))
        self.sound.set_volume(0.2)  #音量調小
        self.sound2 = pygame.mixer.Sound(os.path.join("sound", "virus-die.mp3"))  # virus-die
        self.sound2.set_volume(0.5)
        self.sound3 = pygame.mixer.Sound(os.path.join("sound", "sell.mp3"))  # sell
        self.sound3.set_volume(0.5)
        self.sound4 = pygame.mixer.Sound(os.path.join("sound", "build-and-upgrade.mp3"))  # build-and-upgrade
        self.sound4.set_volume(0.5)

    def user_request(self, user_request: str):
        """ add tower, sell tower, upgrade tower"""
        self.subject.notify(user_request)



    def get_request(self, events: dict) -> str:
        self.selected_button = None
       
        if events["keyboard key"] is not None:
            return "start wave"

        if events["mouse hover"] is not None:  # 8/15
            x, y = events["mouse hover"]
            if self.__menu is not None:
                for btn in self.__menu.buttons:
                    if btn.clicked(x, y):
                        self.hover = btn.response_hover
                        return "nothing"
            for btn in self._love_menu.buttons:  # 8/17
                if btn.clicked(x, y):
                    self.lovehover = btn.response_hover
                    return "nothing"
            self.lovehover = None
            return "nothing"

        if events["mouse position"] is not None:
            x, y = events["mouse position"]
            self.select(x, y)
            if self.selected_button is not None:
                return self.selected_button.response  # 回傳名字
            return "nothing"
        return "nothing"

    def select(self, mouse_x: int, mouse_y: int) -> None:
        
        
        for tw in self.__towers:
            if tw.clicked(mouse_x, mouse_y):
                self.selected_tower = tw
                self.selected_plot = None
                return

        for pt in self.__plots:
            if pt.clicked(mouse_x, mouse_y):
                self.selected_tower = None
                self.selected_plot = pt
                return

        
        if self.__menu is not None:
            for btn in self.__menu.buttons:
                if btn.clicked(mouse_x, mouse_y):
                    self.selected_button = btn
            if self.selected_button is None:
                self.selected_tower = None
                self.selected_plot = None
        
        for btn in self.__main_menu.buttons:
            if btn.clicked(mouse_x, mouse_y):
                self.selected_button = btn

        # lovemenu btn
        for btn in self._love_menu.buttons:
            if btn.clicked(mouse_x, mouse_y):
                self.selected_button = btn

    def call_menu(self):
        if self.selected_tower is not None:          #選擇秀出哪種menu
            x, y = self.selected_tower.rect.center
            if self.selected_tower.identify == 1:#8/8
                self.__menu = UpgradeMenu(x, y)
        elif self.selected_plot is not None:
            if self.selected_plot.identify==1:      #新增
                x, y = self.selected_plot.rect.center
                self.__menu = BuildMenu(x, y)
            elif self.selected_plot.identify==0:
                x, y = self.selected_plot.rect.center
                self.__menu = BlockMenu(x, y)
        else:
            self.__menu = None
    
    def loss_love(self):
        if self.loss_love_count < self.loss_max_count:
            self.loss_love_count += 1
        else:
            self.love_grade -= 1
            self.loss_love_count = 0
    
    def towers_attack(self):
        for tw in self.__towers:
            tw.attack(self.__enemies.get())
            
    def towers_collapse(self):                  #讓block種類的塔過n秒後自動倒塌
        for tw in self.__towers:
            if tw.hp==0:
                x, y = tw.rect.center
                self.__plots.append(BlockVacancy(x, y))
                self.__towers.remove(tw)
    
    def enemies_advance(self):
        self.__enemies.advance(self)

    def gameover(self):                #8/9
        if self.love_grade==0 or self.hp==0:
            return True
        else:
            return False
    
    def win(self):                     #8/10  #8/16
        if self.wave > 4 and self.__enemies.is_empty2():
            if self.love_grade > 0 and self.hp > 0:
                return True
    def cry(self):                     #8/11
        if self.love_grade <6:
            return True

    def get_attack_position(self):    #8/17
        position_list = []
        for tw in self.__towers:
            if tw.start_attack:
                position_list.append(tw.attack_position)
                return position_list

    def get_aoeattack_tower(self):   #8/18
        aoe_list = []
        for tw in self.__towers:
            if tw.start_aoe:
                if tw.aoe_count < 5:
                    tw.aoe_count += 1
                    aoe_list.append(tw)
                else:
                    tw.start_aoe = None
                    tw.aoe_count = 0
                return aoe_list

    @property
    def enemies(self):
        return self.__enemies

    @property
    def towers(self):
        return self.__towers

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, new_menu):
        self.__menu = new_menu

    @property
    def plots(self):
        return self.__plots











