import pygame
import math
import os
from settings import  BASE2,PATH21,PATH22,PATH23,PATH24,PATH25
from color_settings import *
import game
import random
import time


pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))
VIRUS_IMAGE = pygame.image.load(os.path.join("images", "virus.png")) #virus
VIRUS2_IMAGE = pygame.image.load(os.path.join("images", "virus2.png")) #virus#第二關再出現

class Enemy:
    def __init__(self):
        self.path = PATH21
        self.path_index = 0
        self.move_count = 0
        self.stride = 1.3
        self.image = pygame.transform.scale(ENEMY_IMAGE, (85, 80))
        self.rect = self.image.get_rect()
        self.rect.center = self.path[self.path_index]
        self.path_index = 0
        self.move_count = 0
        self.health = 10
        self.max_health = 10
        self.wavecount = 0


    def move(self):
        x1, y1 = self.path[self.path_index]
        x2, y2 = self.path[self.path_index + 1]
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        max_count = int(distance / self.stride)
        # compute the unit vector
        unit_vector_x = (x2 - x1) / distance
        unit_vector_y = (y2 - y1) / distance
        # compute the movement
        delta_x = unit_vector_x * self.stride * self.move_count
        delta_y = unit_vector_y * self.stride * self.move_count
        # update the position and counter
        if self.move_count <= max_count:
            self.rect.center = (x1 + delta_x, y1 + delta_y)
            self.move_count += 1
        else:
            self.move_count = 0
            self.path_index += 1
            self.rect.center = self.path[self.path_index]

    @classmethod
    def people(cls):
        people = cls()
        return people

    @classmethod
    def virus(cls):
        virus = cls()
        virus.image = pygame.transform.scale(VIRUS_IMAGE, (71, 60))
        return virus

    @classmethod
    def virus2(cls): #第二關再出現
        virus2 = cls()
        virus2.image = pygame.transform.scale(VIRUS2_IMAGE, (54, 50))
        return virus2


class EnemyGroup:
    #def __init__(self, wave_count):
    def __init__(self):
        self.campaign_count = 0
        self.campaign_max_count = 60   # (unit: frame)
        self.__reserved_members = []
        self.__expedition = []

    def advance(self, model):
        """Bonus.2"""
        # use model.hp and model.money to access the hp and money information
        self.campaign()
        for i in range(4):  # 814
            if i == 2 and self.is_empty2() and self.is_empty() == True:
                p = random.randint(0, 4)
                model.wave += 1
                for i in range(6):  # final
                    e = random.randint(0, 2)
                    if e == 0:
                        new = Enemy.people()
                    if e == 1:
                        new = Enemy.virus()
                    if e == 2:
                        new = Enemy.virus2()
                        new.stride = 2
                    if p == 0:
                        new.path = PATH21
                    if p == 1:
                        new.path = PATH22
                    if p == 2:
                        new.path = PATH23
                    if p == 3:
                        new.path = PATH24
                    if p == 4:
                        new.path = PATH25
                    self.__reserved_members.append(new)



        for en in self.__expedition:
            en.move()
            if en.health <= 0:
                self.retreat(en)
                model.money+=15  #消滅敵人後錢+15
                if model.music_or_not == True:
                    model.sound2.play()
            # delete the object when it reach the base2
            if BASE2.collidepoint(en.rect.centerx, en.rect.centery):
                self.retreat(en)
                model.hp -= 1   #撞上主塔後血量-1
                if model.music_or_not == True:
                    model.sound2.play()

    def update(self):
        self.campaign()

        for en in self.__expedition:
            en.move()
            if en.health <= 0:
                self.retreat(en)
            # delete the object when it reach the base
            if BASE2.collidepoint(en.rect.centerx, en.rect.centery):
                self.retreat(en)

    def draw(self, win):
        for en in self.__expedition:
            win.blit(en.image, en.rect)
            # draw health bar
            bar_width = en.rect.w * (en.health / en.max_health)
            max_bar_width = en.rect.w
            bar_height = 5
            pygame.draw.rect(win, RED, [en.rect.x, en.rect.y - 10, max_bar_width , bar_height])
            pygame.draw.rect(win, GREEN, [en.rect.x, en.rect.y - 10, bar_width, bar_height])

    def campaign(self):
        """Enemy go on an expedition."""
        if self.campaign_count > self.campaign_max_count and self.__reserved_members:
            self.__expedition.append(self.__reserved_members.pop())
            self.campaign_count = 0
        else:
            self.campaign_count += 1


    def add(self, num):
        """Generate the enemies for next wave"""

    def get(self):
        """Get the enemy list"""
        return self.__expedition

    def is_empty(self):  #8/10
        """Return whether the enemy is empty (so that we can move on to next wave)"""
        return False if self.__reserved_members else True
    def is_empty2(self):  #8/10
        """Return whether the enemy is empty (so that we can move on to next wave)"""
        return False if self.__expedition else True

    def retreat(self, enemy):
        """Remove the enemy from the expedition"""
        self.__expedition.remove(enemy)




