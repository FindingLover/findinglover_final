import pygame
from game.controller import GameControl
from game.model import GameModel
from game.model_2 import GameModel2
from game.model_3 import GameModel3
from game.view import GameView
from game.view_2 import GameView2
from game.view_3 import GameView3
from settings import FPS, WIN_WIDTH, WIN_HEIGHT
from game.gameover import GameOver  # 8/9
from game.gameend import GameEnd
from menu.menus import music_button_image, muse_button_image


class Game:
    def __init__(self): #8/17
        self.text = ' '
    def name(self):    #8/17
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        name_bg = pygame.Rect(0, 0, WIN_WIDTH, WIN_HEIGHT)
        #font = pygame.font.Font(None, 50)
        font = pygame.font.SysFont("arial", 50)
        text = 'Please enter your name here:'
        text2 = '(press \'Enter\' to continue)'
        input_box = pygame.Rect(350, 300, 524, 80)
        color = (128, 0, 0)   #8/18
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
            # Render the current text.
            name_surface = font.render(text, True, (128, 0, 0))
            name_surface2 = font.render(text2, True, (128, 0, 0))
            txt_surface = font.render(self.text, True, color)
            # Resize the box if the text is too long.
            width = max(324, txt_surface.get_width()+20)
            input_box.w = width
            pygame.draw.rect(self.win, (215, 155, 155), name_bg)
            # Blit the input_box rect.
            pygame.draw.rect(self.win, color, input_box, 2)
            # Blit the text.
            self.win.blit(name_surface, (input_box.x-90, input_box.y-120))
            self.win.blit(name_surface2, (input_box.x-60, input_box.y-70))
            self.win.blit(txt_surface, (input_box.x+15, input_box.y+20))
            pygame.display.flip()

    def run(self, sound): #8/17
        pygame.init()
        game_model = GameModel()
        # 8/17
        if sound == True:
            game_model.music_or_not = True
        else:
            game_model.music_or_not = False
        game_view = GameView()
        game_control = GameControl(game_model, game_view)
        win_game = False
        quit_game = False
        level = 1
        while not quit_game:
            pygame.time.Clock().tick(FPS)
            game_control.receive_user_input()
            game_control.update_model()
            game_control.update_view(self.text)     #8/17
            pygame.display.update()
            win_game = game_model.win()  # 8/10
            quit_game = game_control.quit_game
            if win_game:  # 8/11
                game_end = GameEnd()
                quit_game, level = game_end.run(quit_game, level, game_model.music_or_not)
                if level == 1:
                    pygame.init()
                    if game_model.music_or_not:
                        game_model = GameModel()
                        game_model.music_or_not = True
                    else:
                        game_model = GameModel()
                        game_model.music_or_not = False
                    game_view = GameView()
                    game_control = GameControl(game_model, game_view)
                    pygame.mixer.music.load("./sound/menu.wav")

                elif level == 2:
                    pygame.init()
                    if game_model.music_or_not:
                        game_model = GameModel2()
                        game_model.music_or_not = True
                    else:
                        game_model = GameModel2()
                        game_model.music_or_not = False
                    game_view = GameView2()
                    game_control = GameControl(game_model, game_view)
                    pygame.mixer.music.load("./sound/level02.mp3")  #8/18
                elif level == 3:
                    pygame.init()
                    if game_model.music_or_not:
                        game_model = GameModel3()
                        game_model.music_or_not = True
                    else:
                        game_model = GameModel3()
                        game_model.music_or_not = False
                    game_view = GameView3()
                    game_control = GameControl(game_model, game_view)
                    pygame.mixer.music.load("./sound/level03.mp3")  #8/18
                win_game = False
                
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                if game_model.music_or_not:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

            if game_model.gameover():  # 8/9
                gameover = GameOver()
                quit_game = gameover.run(quit_game, game_model.music_or_not)
                if level == 1:
                    pygame.init()
                    if game_model.music_or_not:
                        game_model = GameModel()
                        game_model.music_or_not = True
                    else:
                        game_model = GameModel()
                        game_model.music_or_not = False
                    game_view = GameView()
                    game_control = GameControl(game_model, game_view)
                    pygame.mixer.music.load("./sound/menu.wav")

                elif level == 2:
                    pygame.init()
                    if game_model.music_or_not:
                        game_model = GameModel2()
                        game_model.music_or_not = True
                    else:
                        game_model = GameModel2()
                        game_model.music_or_not = False
                    game_view = GameView2()
                    game_control = GameControl(game_model, game_view)
                    pygame.mixer.music.load("./sound/level02.mp3")  #8/18
                elif level == 3:
                    pygame.init()
                    if game_model.music_or_not:
                        game_model = GameModel3()
                        game_model.music_or_not = True
                    else:
                        game_model = GameModel3()
                        game_model.music_or_not = False
                    game_view = GameView3()
                    game_control = GameControl(game_model, game_view)
                    pygame.mixer.music.load("./sound/level03.mp3")  #8/18
                win_game = False
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                if game_model.music_or_not:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()












