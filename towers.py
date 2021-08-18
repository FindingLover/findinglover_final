from tower.attack_strategy import AOE, SingleAttack, Snipe, Slow, Stop  # 加上Stop8/8
import os
import pygame
import math
# 8/14
PLOT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "icon-build-blue.png")), (20, 20))
BLOCKPLOT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "icon-build-red.png")), (20, 20))
ALCOHOL_IMAGE01 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-alcohol-01.png")), (81, 80))
ALCOHOL_IMAGE02 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-alcohol-02.png")), (81, 80))
ALCOHOL_IMAGE03 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-alcohol-03.png")), (81, 80))
ALCOHOL_IMAGE04 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-alcohol-04.png")), (81, 80))
VACCINE_IMAGE01 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-inject-01.png")), (81, 80))
VACCINE_IMAGE02 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-inject-02.png")), (81, 80))
VACCINE_IMAGE03 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-inject-03.png")), (81, 80))
VACCINE_IMAGE04 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-inject-04.png")), (81, 80))
ISOLATE_IMAGE01 = pygame.transform.scale(pygame.image.load(os.path.join("images", "isolate.png")), (54, 50))
HEALTHCARE_IMAGE01 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-healthcare-01.png")),
                                            (81, 80))
HEALTHCARE_IMAGE02 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-healthcare-02.png")),
                                            (81, 80))
HEALTHCARE_IMAGE03 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-healthcare-03.png")),
                                            (81, 80))
HEALTHCARE_IMAGE04 = pygame.transform.scale(pygame.image.load(os.path.join("images", "tower-healthcare-04.png")),
                                            (81, 80))
MASK_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "mask.png")), (54, 50))

ALCOHOL_IMAGE_list = [ALCOHOL_IMAGE01, ALCOHOL_IMAGE02, ALCOHOL_IMAGE03, ALCOHOL_IMAGE04]  # 8/11
VACCINE_IMAGE_list = [VACCINE_IMAGE01, VACCINE_IMAGE02, VACCINE_IMAGE03, VACCINE_IMAGE04]
ISOLATE_IMAGE_list = [ISOLATE_IMAGE01, ISOLATE_IMAGE01, ISOLATE_IMAGE01, ISOLATE_IMAGE01]
HEALTHCARE_IMAGE_list = [HEALTHCARE_IMAGE01, HEALTHCARE_IMAGE02, HEALTHCARE_IMAGE03, HEALTHCARE_IMAGE04]
MASK_IMAGE_list = [MASK_IMAGE, MASK_IMAGE, MASK_IMAGE, MASK_IMAGE, MASK_IMAGE]


class Vacancy:
    def __init__(self, x, y):
        self.image = PLOT_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.identify = 1

    def clicked(self, x: int, y: int) -> bool:
        return True if self.rect.collidepoint(x, y) else False


class BlockVacancy:  # 新增
    def __init__(self, x, y):
        self.image = BLOCKPLOT_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.identify = 0

    def clicked(self, x: int, y: int) -> bool:
        return True if self.rect.collidepoint(x, y) else False


class Tower:
    """ super class of towers """

    def __init__(self, x: int, y: int, attack_strategy, image):
        self.level = 0
        self.image_list = image  # 8/11
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._range = [100, 110, 120, 130]
        self._damage = [2.0, 2.5, 3.0, 3.5]
        self.cd_count = 0
        self.cd_max_count = 60
        self.attack_strategy = attack_strategy
        self.value = [100, 140, 200, 250]
        self.hp = 350  # 8/15
        self.identify = 1  # 用來辨識地面和高台塔的
        self._attack_position = (x, y)  #8/17
        self._start_attack = None #8/17
        self.attack_count = 0 #8/17
        self.start_aoe = None #8/18
        self.aoe_count = 0#8/18

    @classmethod
    def HealthFood(cls, x, y):  # 範圍傷害
        healthfood = cls(x, y, AOE(), HEALTHCARE_IMAGE_list)  # 8/15
        healthfood._range = [120, 130, 150, 160]
        healthfood._damage = [1.5, 2.0, 2.5, 3.0]
        healthfood.value = [80, 120, 180, 260]
        return healthfood

    @classmethod
    def Alcohol(cls, x, y):  # 單體攻擊
        alcohol = cls(x, y, SingleAttack(), ALCOHOL_IMAGE_list)  # 8/15
        alcohol._range = [150, 160, 170, 180]
        alcohol._damage = [2.0, 3.0, 4.0, 5.0]
        alcohol.value = [80, 120, 180, 260]
        return alcohol

    @classmethod
    def Vaccine(cls, x, y):  # 狙擊
        vaccine = cls(x, y, Snipe(), VACCINE_IMAGE_list)  # 8/15
        vaccine._range = [110, 130, 150, 180]
        vaccine.cd_max_count = 120
        vaccine.value = [110, 150, 210, 290]
        return vaccine

    @classmethod
    def Isolate(cls, x, y):  # 全部緩速
        isolate = cls(x, y, Slow(), ISOLATE_IMAGE_list)  # 8/15
        isolate._range = [0]
        isolate.cd_max_count = 1
        isolate.identify = 0
        return isolate

    @classmethod
    def Mask(cls, x, y):  # 8/8 加上新塔(Block)，擋人+傷害
        mask = cls(x, y, Stop(), MASK_IMAGE_list)  # 8/15
        mask._range = [15]
        mask.cd_max_count = 1
        mask.identify = 0
        return mask

    def attack(self, enemy_group: list):
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return

        self.cd_count = self.attack_strategy.attack(enemy_group, self, self.cd_count)

    def get_upgrade_cost(self):
        return self.value[self.level + 1] - self.value[self.level]

    def get_cost(self):
        return self.value[self.level]

    @property
    def range(self):
        return self._range[self.level]

    @property
    def damage(self):
        return self._damage[self.level]

    @property  # 8/15
    def image(self):
        return self.image_list[self.level]

    @property  # 8/15
    def upgrade_range(self):
        return self._range[self.level + 1] - self._range[self.level]

    @property  # 8/15
    def upgrade_damage(self):
        return self._damage[self.level + 1] - self._damage[self.level]

    def clicked(self, x: int, y: int) -> bool:
        return True if self.rect.collidepoint(x, y) else False

    #8/17
    def hit(self, enemy):
        x1, y1 = self.rect.center
        x2, y2 = enemy.rect.center
        stride = 10
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        step = int(distance / stride)

        unit_vector_x = (x2 - x1) / distance
        unit_vector_y = (y2 - y1) / distance

        delta_x = unit_vector_x * step * self.attack_count
        delta_y = unit_vector_y * step * self.attack_count

        if self.attack_count <= stride:
            self._attack_position = (x1 + delta_x, y1 + delta_y)
            self.attack_count += 1
            self._start_attack = True
            return False
        else:
            self.attack_count = 0
            self._start_attack = False
            return True

    @property  # 8/17
    def attack_position(self):
        return self._attack_position

    @property  # 8/17
    def start_attack(self):
        return self._start_attack