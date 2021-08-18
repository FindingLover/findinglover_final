import pygame


# controller
class GameControl:
    def __init__(self, game_model, game_view):
        self.model = game_model
        self.view = game_view
        self.events = {"game quit": False,
                       "mouse position": [0, 0],
                       "keyboard key": 0
                       }
        self.request = None
        #self.__enemies = EnemyGroup()

    def update_model(self):
        """update the model and the view here"""
        self.request = self.model.get_request(self.events)
        self.model.user_request(self.request)
        self.model.call_menu()
        self.model.towers_attack()
        self.model.towers_collapse()   #新增
        self.model.enemies_advance()
        self.model.loss_love()   #love

    def receive_user_input(self):  # 8/15
        self.events = {"game quit": False,
                       "mouse position": None,
                       "keyboard key": None,
                       "mouse hover": None
                       }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events["game quit"] = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.events["keyboard key"] = pygame.K_n

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.events["mouse position"] = [x, y]

            if event.type == pygame.MOUSEMOTION:  # 8/15
                x, y = pygame.mouse.get_pos()
                self.events["mouse hover"] = [x, y]

    def update_view(self, text):
        self.view.draw_bg()
        self.view.draw_aoe(self.model.get_aoeattack_tower())
        if self.model.cry():     #8/11
            self.view.draw_cry()
        self.view.draw_text(text)
        self.view.draw_hp(self.model.hp)
        self.view.draw_love_grade(self.model.love_grade)
        self.view.draw_towers(self.model.towers)
        self.view.draw_enemies(self.model.enemies)

        self.view.draw_range(self.model.selected_tower)
        self.view.draw_plots(self.model.plots)
        self.view.draw_money(self.model.money)  #畫出money
        self.view.draw_wave(self.model.wave)    #畫出wave

        if self.model.music_or_not == True:          #8/17
            self.view.draw_sound()
        else:
            self.view.draw_muse()
        self.view.draw_lovemenu(self.model._love_menu) #love

        if self.model.menu is not None:
            self.view.draw_menu(self.model.menu)
        self.view.draw_attack(self.model.get_attack_position())  # 8/17
        self.view.draw_tower_information(self.model.hover, self.model.selected_tower, self.model.selected_plot)  # 8/15
        self.view.draw_love_information(self.model.lovehover)  # 8/17

    @property
    def quit_game(self):
        return self.events["game quit"]


