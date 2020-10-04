from __future__ import division, print_function, unicode_literals

# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cocos
from pyglet.gl import *

from cocos.actions import *
from cocos.menu import Menu, MenuItem, zoom_in, zoom_out, fixedPositionMenuLayout
from cocos.layer import Layer, ColorLayer
from cocos.sprite import Sprite
from cocos.text import *

from game import chart
import pickle


class SavedGames(Layer):
    """Слой с открытием сохраненной карты"""
    is_event_handler = True

    def __init__(self):
        super().__init__()

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.button_exit = [1200, 650, 1265, 715]
        if self.button_exit[0] < x < self.button_exit[2] and \
                self.button_exit[1] < y < self.button_exit[3]:
            self.parent.switch_to(0)
            
        self.button_save = [1200, 450, 1265, 515]
        if self.button_save[0] < x < self.button_save[2] and \
                self.button_save[1] < y < self.button_save[3]:
            chart.save('saving', chart.Chart())

    def go(self):
        d = os.path.dirname(__file__)
        beginning = os.path.join(d, '../resources/saving.pickle')
        with open('resources/saving.pickle', 'rb') as f:
            data = pickle.load(f)

        SIZE = 62
        self.map_layer = chart.generate(data, SIZE, 1, 0)
            
        for i in range(len(chart.Chart().cells)):
            for j in range(len(chart.Chart().cells[0])):
                chart.Chart().get_cell(i, j).init_city(i, j, data[i][j])
        
        window_w, window_h = 1300, 800
        chart.Chart().set_view(0, 0, window_w, window_h)
        self.add(chart.BgLayer())
        self.add(chart.Chart())
        self.add(ButtonMap())
        Top_Window().reinit(1) 


class Rules(Layer):
    """Слой с правилами"""

    is_event_handler = True

    def __init__(self):
        super(Rules, self).__init__()
        items = []

        d = os.path.dirname(__file__)
        interface = os.path.join(d, '../resources')
        interface += '/' + 'rules.txt'
        f = open(interface, 'r', encoding='utf-8')
        x = 30
        y = 500
        for line in f:
            label = cocos.text.Label(line,
                                     font_name='Arial',
                                     font_size=18,
                                     anchor_x='left', anchor_y='center')
            label.position = x, y
            y -= 10
            self.add(label)

        self.sprite1 = pyglet.resource.image('exit.png')
        self.sprite2 = pyglet.resource.image('peasant0.png')
        self.sprite3 = pyglet.resource.image('soldier0.png')
        self.sprite4 = pyglet.resource.image('priest0.png')
        self.sprite5 = pyglet.resource.image('knight0.png')

    def draw(self):
        glPushMatrix()
        self.transform()
        self.sprite1.blit(1200, 50)
        self.sprite2.blit(730, 220) 
        self.sprite3.blit(770, 200)
        self.sprite4.blit(890, 175)
        self.sprite5.blit(680, 155)
        glPopMatrix()

    def on_mouse_press (self, x, y, buttons, modifiers):
        self.button_exit = [1200, 50, 1265, 115]
        if self.button_exit[0] < x < self.button_exit[2] and \
            self.button_exit[1] < y < self.button_exit[3]:
            self.parent.switch_to(0)


class Information(Layer):
    """Слой с информацией о разработчиках"""

    is_event_handler = True

    def __init__(self):
        super(Information, self).__init__()
        self.img = pyglet.resource.image('h_water.png')
        
        self.emblems = [0]*6      
        self.emblem(0, 'Crimea.png', [230, 480], 0.5)
        self.emblem(1, 'Moscow.png', [230, 180], 0.5)
        self.emblem(2, 'TG.png', [1050, 485], 0.5)
        self.emblem(3, 'Rostov.png', [230, 330], 0.5)
        self.emblem(4, 'Chelyabinsk.png', [1050, 330], 0.5)
        self.emblem(5, 'Georgia.png', [1050, 180], 0.4)
        
        d = os.path.dirname(__file__)
        interface = os.path.join(d, '../resources')
        interface += '/' + 'info.txt'
        f = open(interface, 'r', encoding='utf-8')
        x = 650
        y = 500
        for line in f:
            label = cocos.text.Label(line,
                                     font_name='Arial',
                                     font_size=20,
                                     anchor_x='center', anchor_y='center')
            label.position = x, y
            y -= 20
            self.add(label)

        self.sprite1 = pyglet.resource.image('exit.png')
        
    def emblem(self, i, img_name, position, scale):
        """Отображает спрайт по названию файла, координатам, размеру"""
        self.emblems[i] = Sprite(pyglet.resource.image(img_name))
        self.emblems[i].position = position
        self.emblems[i].scale = scale
        self.add(self.emblems[i])
            
    def draw(self):
        glPushMatrix()
        self.transform()
        self.sprite1.blit(1200, 50)
        glPopMatrix()

    def call(self):
        self.parent.switch_to(5)
        
    def on_mouse_press(self, x, y, buttons, modifiers):
        self.button_exit = [1200, 50, 1265, 115]
        if self.button_exit[0] < x < self.button_exit[2] and \
                self.button_exit[1] < y < self.button_exit[3]:
            self.parent.switch_to(0)


class MainMenu(Menu):
    """Страница главного меню"""
    def __init__(self):
        super(MainMenu, self).__init__('')

        self.font_item['font_name'] = 'Edit Undo Line BRK',
        self.font_item['font_size'] = 45

        item1 = MenuItem('Новая игра ', self.new_game)
        item2 = MenuItem('Загрузить сохраненнную игру', self.saved_game)
        item3 = MenuItem('Правила игры', self.rules)
        item4 = MenuItem('Информация', self.info)
        self.create_menu([item1, item2, item3, item4], zoom_in(), zoom_out(),
                         layout_strategy=fixedPositionMenuLayout(
                             [(650, 450), (650, 350), (650, 250), (650, 150)]))

    def new_game(self):
        self.parent.layers[4].go()
        self.parent.switch_to(4)

    def saved_game(self):
        self.parent.layers[1].go()
        self.parent.switch_to(1)

    def rules(self):
        self.parent.switch_to(2)

    def info(self):
        self.parent.switch_to(3)


class BackgroundLayer(ColorLayer):
    """Слой фона земли"""
    def __init__(self):
        super(BackgroundLayer, self).__init__(39, 174, 96, 255)
        try: 
            self.img = Sprite(pyglet.resource.image('earth_menu_head.png'))
            self.img.position = [650, 400]
            self.add(self.img)
        except GLException: # Если невозможно загрузить задний план, то вставляем только лого
            self.img = Sprite(pyglet.resource.image('logo.png'))
            self.img.position = [650, 650]
            self.add(self.img)
        

class NewGame(Layer):
    """Слой для меню для загрузки новой игры"""
    is_event_handler = True

    def __init__(self):
        super(NewGame, self).__init__()
        self.go(1)

    def on_mouse_press (self, x, y, buttons, modifiers):
        self.button_exit = [1200, 650, 1265, 715]
        if self.button_exit[0] < x < self.button_exit[2] and \
            self.button_exit[1] < y < self.button_exit[3]:
            self.parent.switch_to(0)
        '''self.button_rule = [1200, 550, 1265, 615]
        if self.button_rule[0] < x < self.button_rule[2] and \
            self.button_rule[1] < y < self.button_rule[3]:
            self.rul = GameRules(1)'''
        self.button_save = [1200, 450, 1265, 515]
        if self.button_save[0] < x < self.button_save[2] and \
                self.button_save[1] < y < self.button_save[3]:
            chart.save('saving', chart.Chart())

    def go(self, new=False):
        d = os.path.dirname(__file__)
        beginning = os.path.join(d, '../resources/begining.pickle')
        with open('resources/begining.pickle', 'rb') as f:
            data = pickle.load(f)

        SIZE = 62
        if new:
            # Сюда программа зайдет один раз при инициализации слоев MultiplexLayer
            self.map_layer = chart.generate(data, SIZE)
            Top_Window(1) # Инициализируем Top_Window впервые           
        else:
            self.map_layer = chart.generate(data, SIZE, 0, 0) # Делаем апдейт
            
        for i in range(len(chart.Chart().cells)):
            for j in range(len(chart.Chart().cells[0])):
                chart.Chart().get_cell(i, j).init_city(i, j)
        
        window_w, window_h = 1300, 800
        chart.Chart().set_view(0, 0, window_w, window_h)
        self.add(chart.BgLayer())
        self.add(chart.Chart())
        self.add(ButtonMap())
        Top_Window().reinit(1)


class GameRules():
    X_WINDOW = 630
    Y_WINDOW = 370
    X_BTN = 1090
    Y_BTN = 100
    def __init__(self, flag):
        super(GameRules, self).__init__()
        self.flag = flag
        self.draw(flag)

    def draw(self, flag):
        if flag == 1:
            '''Рисует окно'''
            N = 3
            window = Sprite("game_rule.png")
            window.position = [self.X_WINDOW, self.Y_WINDOW]
            window.scale = 0.8
            self.mas_sprite = [window]
            exit = Sprite("exit.png")
            exit.position = [self.X_BTN, self.Y_BTN]
            self.mas_sprite.append(exit)
            self.mas_text = []
            self.mas_test_pos = []
            d = os.path.dirname(__file__)
            interface = os.path.join(d, '../resources')
            interface += '/' + 'rules.txt'
            f = open(interface, 'r', encoding='utf-8')
            x = 130
            y = 650
            for line in f:
                label = cocos.text.Label(line,
                                         font_name='Arial',
                                         font_size=14,
                                         anchor_x='left', anchor_y='center')
                label.position = x, y
                y -= 13
                self.mas_sprite.append(label)
            for object in self.mas_sprite:
                chart.Chart().add(object)

    def close_window(self):
        '''Стирает окно'''
        for i in range(len(self.mas_sprite)):
            self.mas_sprite[i].kill()
        self.mas_sprite = []


class ButtonMap(Layer):
    """Слой с кнопками"""
    button_end_move = [1175, 50, 1300, 150]

    def __init__(self):
        super(ButtonMap, self).__init__()
        self.s_exit = pyglet.resource.image('exit.png')
        self.s_rule = pyglet.resource.image('rule.png')
        self.s_save = pyglet.resource.image('save.png')
        self.s_end = pyglet.resource.image('end_turn.png')

    def draw(self):
        glPushMatrix()
        self.transform()
        self.s_exit.blit(1200, 650)
        self.s_rule.blit(1200, 550)
        self.s_save.blit(1200, 450)
        self.s_end.blit(self.button_end_move[0], self.button_end_move[1])
        glPopMatrix()


class Top_Window(metaclass=chart.Singleton):
    """Класс отображения того, кто ходит и окна информации армии"""
    X_POS = 30
    Y_POS = 745
    X_POS_ARMY = 250
    SHIFT = 40
    IMAGE_NAME = ["peasant", "priest", "soldier", "knight"]
    POS_CENTER_BASE = [[87, 124],
                       [87, 620],
                       [1075, 589],
                       [1075, 93]]
    BG_ANIMATION_POS = [[155, 185],
                        [155, 557],
                        [990, 557],
                        [990, 185]]
    CENTER_POS = [570, 370]

    def __init__(self, move):
        super(Top_Window, self).__init__()
        self.reinit(move)
        
    def reinit(self, move):
        """Происходит реинициализация класса по заданному ходу"""
        self.bg = Sprite("light95.png")
        self.bg.scale_x = 0.09
        self.bg.scale_y = 0.115
        self.bg.position = [self.X_POS, self.Y_POS]
        chart.Chart().add(self.bg)
        self.castle = Sprite('castle' + str(move) + '.png')
        self.castle.scale = 0.8
        self.castle.position = [self.X_POS, self.Y_POS]
        chart.Chart().add(self.castle)
        self.mas_sprite = []
        
        self.move = [(move-1) if move > 1 else 1, move]
        self.castle_last_turn = Sprite("castle" + str(self.move[0]) + ".png")
        self.castle_next_turn = Sprite("castle" + str(self.move[1]) + ".png")

        self.bg_animation = Sprite("light95.png")
        self.bg_animation.scale_x = 0.09
        self.bg_animation.scale_y = 0.115

        chart.Chart().add(self.bg_animation)
        chart.Chart().add(self.castle_last_turn)
        chart.Chart().add(self.castle_next_turn)
        self.bg_animation.opacity = 0
        self.castle_next_turn.opacity = 0
        self.castle_last_turn.opacity = 0
        
    def draw_info_army(self, cell):
        """Прорисовка окна информации армии"""
        bg = Sprite("light95.png")
        bg.scale_x = 0.5
        bg.scale_y = 0.115
        bg.position = [self.X_POS_ARMY, self.Y_POS]

        self.mas_sprite.append(bg)
        mas_shift = [-3, -1, 1, 3]
        mas_count = [0]*4
        for unit in cell.army.army:
            for i in range(len(mas_count)):
                if unit.type_unit == i+1:

                    mas_count[i] += unit.count

        for i, g in enumerate(mas_shift):
            unit = Sprite(self.IMAGE_NAME[i] + str(cell.army.player) + ".png")
            unit.scale = 1.5
            unit.position = [self.X_POS_ARMY + self.SHIFT*g - 20, self.Y_POS]
            count = cocos.text.Label(str(mas_count[i]),
                                          font_name='Times New Roman',
                                          font_size=32,
                                          anchor_x='left', anchor_y='center')
            count.position = [self.X_POS_ARMY + self.SHIFT*g - 5, self.Y_POS]
            self.mas_sprite.append(count)
            self.mas_sprite.append(unit)

        for object in self.mas_sprite:
            chart.Chart().add(object)

    def close_info_army(self):
        """Закрывает окно информации о количестве армии"""
        for object in self.mas_sprite:
            object.kill()
        self.mas_sprite = []

    def update_status(self, move):
        """Отображает переход хода"""
        self.move = [self.move[1], move]
        self.castle.image = pyglet.resource.image('castle' + str(move) + '.png')
        self.castle_last_turn.image = pyglet.resource.image("castle" + str(self.move[0]) + ".png")
        self.castle_next_turn.image = pyglet.resource.image('castle' + str(move) + '.png')
        self.animation()

    def animation(self):
        """Анимация перехода хода"""
        self.castle_next_turn.opacity = 0
        self.castle_next_turn.position = self.CENTER_POS
        self.castle_last_turn.position = self.POS_CENTER_BASE[self.move[0]-1]
        self.bg_animation.position = self.BG_ANIMATION_POS[self.move[0]-1]
        self.castle_last_turn.opacity = 255
        self.bg_animation.do((Show()
                                + FadeIn(0.35)
                                + (ScaleTo(3,1.15)|MoveTo((self.CENTER_POS), 1.15))

                                + Delay(0.5)

                                + (ScaleTo(1, 1.15)|MoveTo((self.BG_ANIMATION_POS[self.move[1]-1]),1.15))

                                + FadeOut(0.85)))
        self.castle_last_turn.do((Show()
                                + MoveTo((self.BG_ANIMATION_POS[self.move[0]-1]), 0.35) | ScaleTo(0.8, 0.35)
                                + (ScaleTo(2.5,1.15)|MoveTo((self.CENTER_POS), 1.15))

                                + FadeOut(0.5)

                                + ScaleTo(1, 0.85)))
        self.castle_next_turn.do((Show()
                                + ScaleTo(2.5, 1.5)

                                + FadeIn(0.5)

                                + (ScaleTo(1, 1.15)|MoveTo((self.BG_ANIMATION_POS[self.move[1]-1]),1.15))

                                + (ScaleTo(1, 0.35)|MoveTo(self.POS_CENTER_BASE[self.move[1]-1], 0.35))
                                + FadeOut(0.5)))
                                
    def exit_animation(self):
        """Пропуск анимации"""
        if self.castle_next_turn:
            self.castle_next_turn.kill()
            self.castle_next_turn = 0
        if self.castle_last_turn:
            self.castle_last_turn.kill()
            self.castle_last_turn = 0
        if self.bg_animation:
            self.bg_animation.kill()
            self.bg_animation = 0

        self.bg_animation = Sprite("light95.png")
        self.bg_animation.scale_x = 0.09
        self.bg_animation.scale_y = 0.115
        self.bg_animation.opacity = 0
        self.bg_animation.position = self.BG_ANIMATION_POS[self.move[1] - 1]
        chart.Chart().add(self.bg_animation)

        self.castle_last_turn = Sprite("castle" + str(self.move[0]) + ".png")
        self.castle_last_turn.scale = 1
        self.castle_last_turn.opacity = 0
        self.castle_last_turn.position = self.CENTER_POS
        chart.Chart().add(self.castle_last_turn)

        self.castle_next_turn = Sprite("castle" + str(self.move[1]) + ".png")
        self.castle_next_turn.scale = 1
        self.castle_next_turn.opacity = 0
        self.castle_next_turn.position = self.POS_CENTER_BASE[self.move[1]-1]
        chart.Chart().add(self.castle_next_turn)


class Endgame (Layer):
    """Слой конца игры"""
    is_event_handler = True

    button_exit = [1200, 50, 1265, 115]
    winner = ''
    
    def __init__(self):
        super(Endgame, self).__init__()

        d = os.path.dirname(__file__)
        interface = os.path.join(d, '../resources')
        pyglet.resource.path = [interface]
        pyglet.resource.reindex()
        self.sprite1 = pyglet.resource.image('exit.png')
        label = cocos.text.Label('That`s all, folks!',
                                     font_name='Arial',
                                     font_size= 70,
                                     anchor_x='left', anchor_y='center')
        label.position = 310, 350
        self.add(label)
        
    def draw(self):
        glPushMatrix()
        self.transform()
        self.sprite1.blit(1200, 50)
        glPopMatrix()


