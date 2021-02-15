"""
Главный файл игры
В нем располагается MultiplexLayer и обработчик событий.
"""

import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import MultiplexLayer, pyglet
from cocos.layer import *
from game import session, city
from game import menu
from game.menu import *
from game.logic import *

from sys import platform
from PyQt5.QtCore import pyqtSignal, QObject
from threading import Timer

class CommunicateMain(QObject):
    sig = pyqtSignal()

class MouseDisplay(cocos.layer.Layer):
    """Класс реагирования на нажатия мыши"""
    is_event_handler = True
    waiting_other_players = True

    def __init__(self):
        super().__init__()
        # t = Timer(20, self.wait)
        # t.start()
        self.communicate = CommunicateMain()
        self.communicateCngMove = CommunicateMain()
        self.menu = False
        self.rules = False
        self.endgame = False
        self.communicate.sig.connect(self.unlock_game)
        self.communicateCngMove.sig.connect(self.change_move)
        self.logic = Logic(self.communicate.sig, self.communicateCngMove.sig)


    # def wait(self):
    #     self.on_key_press(104, '')
    #
    #     t = Timer(5, self.wait)
    #     t.start()

    def change_move(self):
        game_session.change_move()
        if game_session.endgame()[0]:
            self.endgame = True
            menu.Endgame.winner = game_session.endgame()[1]
            scene.children[2][1].switch_to(5)
        top_window.exit_animation()
        top_window.update_status(game_session.move_player)

    def unlock_game(self):
        self.waiting_other_players = False

    def on_mouse_motion(self, x, y, dx, dy):
        return
        # if self.waiting_other_players:
        #     # top_window.exit_animation()
        #     self.logic.wait_other_player()

    def on_key_press(self, key, _):
        print('key pressed: ', key)
        """Обработка нажатий на клавиатуру"""
        if self.waiting_other_players:
            # top_window.exit_animation()
            self.logic.wait_other_player()

        if not self.waiting_other_players:
            if key == pyglet.window.key.ENTER:
                self.waiting_other_players = True
                self.change_move()
                self.logic.end_move()

            if key == pyglet.window.key.MOD_WINDOWS:
                top_window.exit_animation()

    def on_mouse_press(self, x, y, buttons, _):
        """Обработка нажатий на мышь"""

        if not self.waiting_other_players:
            if top_window.mas_sprite:
                """закрытие окна с ифформацией об армии"""
                top_window.close_info_army()
            if self.endgame and menu.Endgame.button_exit[0] < x < menu.Endgame.button_exit[2] and\
               menu.Endgame.button_exit[1] < y < menu.Endgame.button_exit[3]:
                scene.children[2][1].switch_to(0)
            elif not self.menu and not self.rules:
                if menu.ButtonMap.button_end_move[0] < x < menu.ButtonMap.button_end_move[2] and \
                   menu.ButtonMap.button_end_move[1] < y < menu.ButtonMap.button_end_move[3]:
                    self.waiting_other_players = True
                    self.change_move()
                    self.logic.end_move()

                self.button_rule = [1200, 550, 1265, 615]
                if self.button_rule[0] < x < self.button_rule[2] and \
                        self.button_rule[1] < y < self.button_rule[3]:
                    self.rul = menu.GameRules(1)
                    self.rules = True

                if buttons == pyglet.window.mouse.LEFT:
                    if chart.Chart().get_at_pixel(x, y):
                        entered_cell = chart.Chart().get_at_pixel(x, y)

                        if entered_cell.army \
                                and entered_cell.army.player == game_session.move_player \
                                and not game_session.is_moving:
                            """добавление подсветки армии при нажатии на нее"""
                            self.logic.add_podsvet(entered_cell.i, entered_cell.j)
                            game_session.is_moving = True
                            game_session.last_entered_cell = entered_cell

                        elif game_session.is_moving:
                            i, j = game_session.last_entered_cell.i, game_session.last_entered_cell.j
                            i1, j1 = entered_cell.i, entered_cell.j

                            if not chart.Chart().get_cell(i, j).army.step(i, j, i1, j1):
                                """нажатие на неподсвеченную клетку, для которой работает подсветка"""
                                self.logic.delete_podsvet(i, j)
                                game_session.is_moving = False
                                game_session.last_entered_cell = None

                            else:
                                """передвижение армии (внутри передвижения удаляется подсветка)"""
                                self.logic.move_army(i, j, i1, j1)
                                game_session.is_moving = False
                                game_session.last_entered_cell = None

                        if entered_cell.army and entered_cell.properties['player'] == game_session.move_player:
                            """вывод информации об армии на которую нажали"""
                            top_window.draw_info_army(entered_cell)


                if buttons == pyglet.window.mouse.RIGHT and chart.Chart().get_at_pixel(x, y):
                    self.entered_cell = chart.Chart().get_at_pixel(x, y)
                    if self.entered_cell.town and self.entered_cell.properties['player'] == game_session.move_player:
                        self.menu = True
                        self.hiring = city.Hiring_window(x, y)

            elif self.menu:
                MINUS = [1, 2, 3, 4]
                PLUS = [5, 6, 7, 8]
                OK = 9
                if buttons == pyglet.window.mouse.LEFT and self.hiring.get_at_pixel(x, y):
                    button = self.hiring.get_at_pixel(x, y)
                    if button in MINUS:
                        self.hiring.enter_minus(button, self.entered_cell.town.type_city)
                    elif button in PLUS:
                        self.hiring.enter_plus(button, self.entered_cell.town.type_city)
                    elif button == OK:
                        self.logic.enter_ok(self.hiring, self.entered_cell)
                        self.hiring.close_window()
                        self.menu = False

            elif self.rules:
                self.button_exit = [1063, 74, 1117, 128]
                if self.button_exit[0] < x < self.button_exit[2] and \
                        self.button_exit[1] < y < self.button_exit[3]:
                    self.rul.close_window()
                    self.rules = False


window_w, window_h = 1300, 800
if platform == 'darwin':
    director.init(width=window_w, height=window_h, fullscreen=True)
else:
    director.init(width=window_w, height=window_h)

game_session = session.Session(2, ["Player 1", "Player 2"])

scene = Scene(MouseDisplay())
scene.add(MultiplexLayer(
        menu.MainMenu(),
        menu.SavedGames(),
        menu.Rules(),
        menu.Information(),
        menu.NewGame(game_session.move_player),
        menu.Endgame(),
    ),
        z=1)

top_window = menu.Top_Window(game_session.move_player)
scene.add(menu.BackgroundLayer(), z=0)
director.run(scene)

