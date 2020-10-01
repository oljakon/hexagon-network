import cocos
import pyglet
from cocos.director import director
from cocos.scene import Scene
from game import *
from cocos.layer import *                
from cocos.sprite import Sprite

class Session():
    '''
    Класс сессия. Хранит информацию о текущем состоянии игры
    '''
    
    def __init__(self, num, names_of_players):
        self.names = names_of_players
        self.num = num
        self.move_player = 1
        self.is_moving = False
        self.last_entered_cell = None
        
    '''
    Конец игры
    '''
    def endgame(self):
        array_players = []
        for i in range(len(chart.Chart().cells)):
            for j in range(len(chart.Chart().cells[0])):
                if chart.Chart().get_cell(i, j) and\
                  chart.Chart().get_cell(i, j).properties['relief'] == chart.MyCell.BASE:
                      if chart.Chart().get_cell(i, j).properties['player'] not in array_players:
                          array_players.append(chart.Chart().get_cell(i, j).properties['player'])
        if len(array_players) == 1:
            return True, self.names[array_players[0] - 1]
        return False, 0
    '''
    Текущий ход
    '''
    def show_move(self):
        return self.move_player
    '''
    Окончание текущего хода и подготовка к следующему
    '''
    def change_move(self):
#        print(len(chart.Chart().cells))
        for i in range(len(chart.Chart().cells)):
            for j in range(len(chart.Chart().cells[0])):
#                print(i,j,chart.Chart().get_cell(i, j))
                
                if chart.Chart().get_cell(i, j) and chart.Chart().get_cell(i, j).army:
                    chart.Chart().get_cell(i, j).army.move = True
                    chart.Chart().get_cell(i, j).army.delete_podsvet()
                    chart.Chart().get_cell(i, j).army.sprite.kill()
                    army = chart.Chart().get_cell(i, j).army
                    army.mas_sprite = ['peasant' + str(army.player) + '.png',   \
                           'priest' + str(army.player) + '.png',    \
                           'soldier' + str(army.player) + '.png',   \
                           'knight' + str(army.player) + '.png']
        
                    army.type_army_global = army.army[0].type_unit
                    army.xy = [army.x + army.deviation_x, army.y + army.deviation_y]
                    
                    army.sprite = Sprite(army.mas_sprite[army.type_army_global-1])
                    army.sprite.position = army.xy
                    army.sprite.scale = 1.4
                    chart.Chart().get_cell(i, j).army = army
                    chart.Chart().add(army.sprite)
                
                if chart.Chart().get_cell(i, j) and\
                   chart.Chart().get_cell(i, j).properties['relief'] == chart.MyCell.BASE\
                   and chart.Chart().get_cell(i, j).properties['player'] ==\
                   self.move_player:
                    chart.Chart().get_cell(i, j).town.spawn()
                if chart.Chart().get_cell(i, j) and chart.Chart().get_cell(i, j).properties['relief'] == chart.MyCell.CITY \
                   and chart.Chart().get_cell(i, j).properties['player'] ==\
                   self.move_player:
                    chart.Chart().get_cell(i, j).town.spawn()
        self.move_player = self.move_player % self.num  + 1
        flag_isplaying = False
        for i in range(len(chart.Chart().cells)):
            for j in range(len(chart.Chart().cells[0])):
                if chart.Chart().get_cell(i, j) and\
                   chart.Chart().get_cell(i, j).properties['relief'] == chart.MyCell.BASE\
                   and chart.Chart().get_cell(i, j).properties['player'] ==\
                   self.move_player:
                    flag_isplaying = True
        if not flag_isplaying:
            for i in range(len(chart.Chart().cells)):
                for j in range(len(chart.Chart().cells[0])):
                    if chart.Chart().get_cell(i, j) and\
                       chart.Chart().get_cell(i, j).army and \
                       chart.Chart().get_cell(i, j).army.player == self.move_player:
                        chart.Chart().get_cell(i, j).army.change_player(0)
                        
            self.change_move()
        self.move_name = self.names[self.move_player - 1]
        self.is_moving = False
        self.last_entered_cell = None

