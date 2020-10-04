"""
Главный файл игры
В нем располагается MultiplexLayer и обработчик событий.
"""

import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import MultiplexLayer
from game import *

from sys import platform

class MouseDisplay(cocos.layer.Layer):
    """Класс реагирования на нажатия мыши"""
    is_event_handler = True
    
    def __init__(self):
        super().__init__()
        self.menu = False
        self.rules = False
        self.endgame = False
        
    def on_key_press(self, key, modifiers):
        """Обработка нажатий на клавиатуру"""
        if key == pyglet.window.key.ENTER:
            game_session.change_move()
            if game_session.endgame()[0]:
                self.endgame = True
                menu.Endgame.winner = game_session.endgame()[1]
                scene.children[2][1].switch_to(5)
            top_window.exit_animation()
            top_window.update_status(game_session.move_player)

        if key == pyglet.window.key.MOD_WINDOWS:
            top_window.exit_animation()

    def on_mouse_press (self, x, y, buttons, modifiers):
        """Обработка нажатий на мышь"""

        if top_window.mas_sprite:
            """закрытие окна с ифформацией об армии"""
            top_window.close_info_army()
        if self.endgame and menu.Endgame.button_exit[0] < x < menu.Endgame.button_exit[2] and\
           menu.Endgame.button_exit[1] < y < menu.Endgame.button_exit[3]:
            scene.children[2][1].switch_to(0)
        elif not self.menu and not self.rules:
            if menu.ButtonMap.button_end_move[0] < x < menu.ButtonMap.button_end_move[2] and \
               menu.ButtonMap.button_end_move[1] < y < menu.ButtonMap.button_end_move[3]:
                """смена хода"""
                game_session.change_move()
                if game_session.endgame()[0]:
                    self.endgame = True
                    menu.Endgame.winner = game_session.endgame()[1]
#                    print(menu.Endgame.winner)
                    scene.children[2][1].switch_to(5)
                """Пропуск анимации"""
                top_window.exit_animation()
                """Отображает переход хода"""
                top_window.update_status(game_session.move_player)
            self.button_rule = [1200, 550, 1265, 615]
            if self.button_rule[0] < x < self.button_rule[2] and \
                    self.button_rule[1] < y < self.button_rule[3]:
                self.rul = menu.GameRules(1)
                self.rules = True

            if buttons == pyglet.window.mouse.LEFT:
                if chart.Chart().get_at_pixel(x, y):
                    entered_cell = chart.Chart().get_at_pixel(x, y)

                    if entered_cell.army and entered_cell.army.player == game_session.move_player and not game_session.is_moving:
                        """добавление подсветки армии при нажатии на нее"""
                        entered_cell.army.add_podsvet()
                        game_session.is_moving = True
                        game_session.last_entered_cell = entered_cell

                    elif game_session.is_moving:
                        i, j = game_session.last_entered_cell.i, game_session.last_entered_cell.j
                        i1, j1 = entered_cell.i, entered_cell.j
                        
                        if not chart.Chart().get_cell(i, j).army.step(i, j, i1, j1):
                            """нажатие на неподсвеченную клетку, для которой работает подсветка"""
                            chart.Chart().get_cell(i, j).army.delete_podsvet()
                            game_session.is_moving = False
                            game_session.last_entered_cell = None

                        else:
                            """передвижение армии (внутри передвижения удаляется подсветка)"""
                            chart.Chart().get_cell(i, j).army.move_army(i1, j1)
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
                    self.hiring.enter_ok(self.entered_cell.town.type_city)
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

game_session = session.Session(4, ["Player 1", "Player 2", "Player 3", "Player 4"])

scene = Scene(MouseDisplay())
scene.add(MultiplexLayer(
        menu.MainMenu(),
        menu.SavedGames(),
        menu.Rules(),
        menu.Information(),
        menu.NewGame(),
        menu.Endgame(),
    ),
        z=1)

top_window = menu.Top_Window(game_session.move_player)
scene.add(menu.BackgroundLayer(), z=0)
director.run(scene)

