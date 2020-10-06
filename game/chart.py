"""
Данный файл включает в себя класс клетки;
Функцию генерации и сохранения карты;
Задний слой с водой;
Синглтон для карты.
"""

from cocos.tiles import Tile, HexCell, HexMapLayer
from cocos.layer import ColorLayer
from cocos.sprite import Sprite
from pyglet.gl import *
from pyglet.resource import image
import pickle
from random import randint

from game import city
from game import army

class Singleton(type):
    _instances = {}
 
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyCell(HexCell): 
    """
    Класс ячейки, включает в себя ее координаты, 
    рельеф, вместимость, наличие в ней города или армии
    """
    WATER = 0
    SOIL = 1
    CITY = 2
    BASE = 3
    start_capacity = 99    
    def __init__(self, i, j, pix_size, info):
        if info['relief'] == self.WATER:
            self.tile = Tile('water', info, image('h_water.png'))
        elif info['relief'] == self.SOIL:
            a = randint(-10, 7)
            a = '' if (a <= 0) else a
            self.tile = Tile('soil', info, image('h_earth'+str(a)+'.png'))
        elif info['relief'] == self.CITY:
            self.tile = Tile('sity', info, image('h_town1.png'))
        elif info['relief'] == self.BASE:
            a = info['player']
            self.tile = Tile('base', {}, image('h_castle'+str(a)+'.png'))
        
        self.army = None
        HexCell.__init__(self, i, j, None, pix_size, info, self.tile)
        self.properties['capacity'] = self.start_capacity 

    def init_city(self, i, j, data=False):
        """Инициализирует города и армии"""
        self.town = None
        self.army = None
        
        if not data:
            if self.properties['relief'] == self.CITY: 
                self.town = city.City(self.properties['relief'], randint(1, 4), i, j)
                self.town.spawn()
            elif self.properties['relief'] == self.BASE:
                self.town = city.City(self.properties['relief'], 1, i, j)
                self.town.spawn()
        else:
            if data['town']:
                self.town = city.City(self.properties['relief'], data['town']['type_unit'], i, j)
                self.town.gold = data['town']['gold']
                self.town.stats = data['town']['stats']
            if data['army']:
                unit = army.Unit(data['army'][0]['count'], data['army'][0]['type_unit'], data['army'][0]['stats'])
                self.army = army.Army(unit, i, j)
                for i in range(1, len(data['army'])):
                    self.army.merge_unit(army.Unit(data['army'][i]['count'],
                                              data['army'][i]['type_unit'], data['army'][i]['stats']))
                            
    def enter_cell(self, army):
        """Позволяет объекту класса армия войти в клетку"""
        self.army = army
        self.properties['player'] = army.player
        
    def leave_cell(self):
        """Позволяет армии выйти из клетки"""
        self.army = None


class Chart(HexMapLayer, metaclass=Singleton):
    def _init(self, name, info, size, cells):
        HexMapLayer.__init__(self, name, info, size, cells)
    def update(self, name, info, size, cells):
        HexMapLayer.__init__(self, name, info, size, cells)


    
class BgLayer(ColorLayer):
    """
    Задний фон воды для карты. 
    """
    def __init__(self):
        super(BgLayer, self).__init__(176, 233, 252, 255)
        try:
            self.img = Sprite(image('water.png'))
            self.img.position = [650, 400]
            self.add(self.img)
        except GLException:
            # Если невозможно загрузить задний план, то оставляем цветной фон
            pass
        
def generate(data, size, load=False, new=True):
    """
    Функция генерации Chart на основе массива
    с типами плиток. 
    """
    r = []
    for i in range(len(data)):
        c = []
        for j in range(len(data[i])):
            if load:
                c.append(MyCell(i, j, size, data[i][j]['properties']))
            else:
                c.append(MyCell(i, j, size, data[i][j]))
        r.append(c)
    if new:
        return Chart('LetTheBattleBegin', None, size, r)
    else:
        return Chart().update('LetTheBattleBegin', None, size, r)


def save(filename, chart):
    """
    Сохраняет карту в файл, для последующей загрузки.
    """
    data = []
    for i in range(len(chart.cells)):
        row = []
        data.append(row)
        for j in range(len(chart.cells[0])):
            cell = chart.cells[i][j]
            info = {}
            info['properties'] = cell.properties
            if cell.town:
                info['town'] = {'gold': cell.town.gold, 'type_unit': cell.town.type_unit,
                                'stats': cell.town.stats}
            else: info['town'] = None
            if cell.army:
                army = []
                for unit in cell.army.army:
                    unit_stat = {'type_unit': unit.type_unit, 'count': unit.count,
                            'stats':[unit.one_unit_hp, unit.one_unit_attack,
                                     unit.one_unit_defense]}
                    army.append(unit_stat)
                info['army'] = army
            else: info['army'] = None
            row.append(info)
    with open('resources/'+filename+'.pickle', 'wb') as f:
        pickle.dump(data, f)

