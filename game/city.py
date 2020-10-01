import cocos
from game import army
from game import chart
from cocos.sprite import Sprite

class City():
    '''Класс города, генерируются отряды'''
    
    COST = [2, 4, 4, 8]
    GOLD = 2
    BASE_STATS = [
        [6, 2, 0],
        [6, 8, 2],
        [8, 5, 3],
        [15, 7, 10]
    ]
    
    SPAWN = [4, 2, 2, 1]
    
    def __init__(self, type_city, type_unit, i, j):
        self.i = i
        self.j = j
        self.gold = 0
        self.building = type_city - 1
        self.type_unit = type_unit
        self.type_city = type_city
        self.stats = self.BASE_STATS
        self.cell = chart.Chart().get_cell(i, j)
        
    def spawn(self):
        '''Генерация отрядов'''
        self.gold += self.building*self.GOLD
        self.unit = army.Unit(self.building * self.SPAWN[self.type_unit - 1],
                              self.type_unit, self.stats[self.type_unit - 1])
        if self.cell.army:
            self.cell.army.merge_unit(self.unit)
        else:
            self.cell.enter_cell(army.Army(self.unit, self.i, self.j))

    def hire(self, count, type_unit):
        '''Найм войск'''
        if self.COST[type_unit]*count <= self.gold:
            self.gold -= self.COST[type_unit]*count
            self.unit = army.Unit(count, type_unit+1, self.stats[type_unit])
            if self.cell.army:
                self.cell.army.merge_unit(self.unit)
            else:
                self.cell.enter_cell(army.Army(self.unit, self.i, self.j))

class Hiring_window():
    '''Класс окна для найма'''

    CITY = 2
    BASE = 3
    X_WINDOW = 550
    Y_WINDOW = 350
    X_UNIT = 410
    Y_UNIT = 265
    X_SHIFT = 55
    Y_SHIFT = 60
    IMAGE_NAME = ["peasant", "priest", "soldier", "knight"]
    MAS_COST = [8, 4, 4, 2]

    def __init__(self, x, y):
        super(Hiring_window, self).__init__()
        self.x = x
        self.y = y
        self.mas_sprite = []
        self.mas_label = ["0", "0", "0", "0"]
        self.mas_true_minus = [0, 0, 0, 0]
        self.mas_true_plus = [0, 0, 0, 0]
        self.cell = chart.Chart().get_at_pixel(x, y)
        self.type_cell = self.cell.properties['relief']
        self.player = self.cell.properties['player']
        self.type_unit = self.cell.town.type_unit - 1
        self.draw()

    def draw(self):
        '''Рисует окно'''
        N = 3
        window = Sprite("light95.png")
        window.position = [self.X_WINDOW, self.Y_WINDOW]
        window.scale = 0.6
        self.mas_sprite = [window]
        gold = Sprite("gold.png")
        gold.scale = 0.25
        shift_pos = 5
        gold.position = [self.X_UNIT + self.X_SHIFT * 4 + shift_pos,
                         self.Y_UNIT + self.Y_SHIFT * N]
        self.mas_sprite.append(gold)
        gold2 = Sprite("gold.png")
        gold2.scale = 0.25
        gold2.position = [self.X_UNIT + self.X_SHIFT * 4 + shift_pos,
                          self.Y_UNIT + self.Y_SHIFT * (N - 1)]
        self.mas_sprite.append(gold2)
        shift_gold_pos = 30
        gold_label = cocos.text.Label(str(self.cell.town.gold),
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='left', anchor_y='center')
        gold_label.position = [self.X_UNIT + self.X_SHIFT * 4 + shift_gold_pos,
                               self.Y_UNIT + self.Y_SHIFT * N]
        self.mas_sprite.append(gold_label)
        ok = Sprite("ok.png")
        ok.position = [self.X_UNIT + self.X_SHIFT * 4.5, self.Y_UNIT]
        self.mas_sprite.append(ok)
        if self.type_cell == self.CITY:
            unit = Sprite(self.IMAGE_NAME[self.type_unit] + str(self.player) + ".png")
            unit.scale = 2
            unit.position = [self.X_UNIT, self.Y_UNIT + self.Y_SHIFT*3]
            self.mas_sprite.append(unit)
            self.mas_true_minus[0] = bool(int(self.mas_label[0]))
            if self.mas_true_minus[0]:
                minus = Sprite("minus.png")
                minus.scale = 0.7
                minus.position = [self.X_UNIT + self.X_SHIFT, self.Y_UNIT + self.Y_SHIFT*3]
                self.mas_sprite.append(minus)

            label = cocos.text.Label(self.mas_label[0],
                                     font_name='Times New Roman',
                                     font_size=32,
                                     anchor_x='center', anchor_y='center')
            label.position = [self.X_UNIT + self.X_SHIFT*2, self.Y_UNIT + self.Y_SHIFT*3]
            self.mas_sprite.append(label)
            all_costs = int(self.mas_label[0]) * self.MAS_COST[N - self.type_unit]
            self.mas_true_plus[0] = all_costs + self.MAS_COST[N - self.type_unit] <= self.cell.town.gold
            if self.mas_true_plus[0]:
                plus = Sprite("plus.png")
                plus.scale = 0.7
                plus.position = [self.X_UNIT + self.X_SHIFT*3, self.Y_UNIT + self.Y_SHIFT*3]
                self.mas_sprite.append(plus)

        elif self.type_cell == self.BASE:

            all_costs = 0
            for i in range(len(self.mas_label)):
                all_costs += (int(self.mas_label[i]) * self.MAS_COST[N - i])
            for i in range(len(self.IMAGE_NAME)):
                self.mas_true_plus[i] = all_costs + self.MAS_COST[N - i] <= self.cell.town.gold

            for i in range(len(self.IMAGE_NAME)):
                unit = Sprite(self.IMAGE_NAME[i] + str(self.player) + ".png")
                unit.scale = 2
                unit.position = [self.X_UNIT, self.Y_UNIT + self.Y_SHIFT*i]
                self.mas_sprite.append(unit)

                label = cocos.text.Label(self.mas_label[i],
                                         font_name = 'Times New Roman',
                                         font_size = 32,
                                         anchor_x = 'center', anchor_y = 'center')
                label.position = [self.X_UNIT + self.X_SHIFT * 2,
                                  self.Y_UNIT + self.Y_SHIFT * i]
                self.mas_sprite.append(label)
                self.mas_true_minus[i] = bool(int(self.mas_label[i]))
                if self.mas_true_minus[i]:
                    minus = Sprite("minus.png")
                    minus.scale = 0.7
                    minus.position = [self.X_UNIT + self.X_SHIFT,
                                    self.Y_UNIT + self.Y_SHIFT * i]
                    self.mas_sprite.append(minus)

                if self.mas_true_plus[N - i]:
                    plus = Sprite("plus.png")
                    plus.scale = 0.7
                    plus.position = [self.X_UNIT + self.X_SHIFT * 3,
                                  self.Y_UNIT + self.Y_SHIFT * (N - i)]
                    self.mas_sprite.append(plus)
                    
        gold2_label = cocos.text.Label(str(all_costs),
                                      font_name='Times New Roman',
                                      font_size=32,
                                      anchor_x='left', anchor_y='center')
        gold2_label.position = [self.X_UNIT + self.X_SHIFT * 4 + shift_gold_pos,
                               self.Y_UNIT + self.Y_SHIFT * (N-1)]
        self.mas_sprite.append(gold2_label)

        for object in self.mas_sprite:
            chart.Chart().add(object)

    def enter_plus(self, button, typ):
        if typ == self.BASE:
            for i, bool_plus in enumerate(self.mas_true_plus):
                if bool_plus and i == button%(len(self.mas_true_plus) + 1):
                    self.mas_label[i] = str(int(self.mas_label[i]) + 1)
                    self.close_window()
                    self.draw()
        elif typ == self.CITY:
            BUTTON_PLUS = 8
            if self.mas_true_plus[0] and button == BUTTON_PLUS:
                self.mas_label[0] = str(int(self.mas_label[0]) + 1)
                self.close_window()
                self.draw()

    def enter_minus(self, button, typ):
        if typ == self.BASE:
            for i, bool_minus in enumerate(self.mas_true_minus):
                if bool_minus and i == button-1:
                    self.mas_label[i] = str(int(self.mas_label[i]) - 1)
                    self.close_window()
                    self.draw()
        elif typ == self.CITY:
            BUTTON_MINUS = 4
            if self.mas_true_minus[0] and button == BUTTON_MINUS:
                self.mas_label[0] = str(int(self.mas_label[0]) - 1)
                self.close_window()
                self.draw()

    def enter_ok(self, typ):
        if typ == self.BASE:
            for i in range(len(self.mas_label)):
                count = int(self.mas_label[i])
                if count:
                    self.cell.town.hire(count, i)
        elif typ == self.CITY:
            if int(self.mas_label[0]):
                self.cell.town.hire(int(self.mas_label[0]), self.type_unit)
                
    @staticmethod
    def get_at_pixel(x, y):
        '''Находит кнопку по координатам'''
        X1_MINUS = 442
        X2_MINUS = 487
        X1_PLUS = 552
        X2_PLUS = 596
        X1_OK = 626
        X2_OK = 688
        Y_POS = 243
        Y_SHIFT = 42
        Y0_SHIFT = 22
        button = 0
        if x > X1_MINUS and x < X2_MINUS:
            start = 1
            stop = 5
            for i in range(start, stop):
                if y > (Y_POS + Y0_SHIFT*(i-start) + Y_SHIFT*(i-start)) \
                        and y < (Y_POS + Y0_SHIFT*(i-start) + Y_SHIFT*i):
                    button = i
                    break

        elif x > X1_PLUS and x < X2_PLUS:
            start = 5
            stop = 9
            for i in range(start, stop):
                if y > (Y_POS + Y0_SHIFT*(i-start) + Y_SHIFT*(i-start))\
                        and y < (Y_POS + Y0_SHIFT*(i-start) + Y_SHIFT*(i-start+1)):
                    button = i
                    break

        elif x > X1_OK and x < X2_OK and y > Y_POS and y < (Y_POS + Y_SHIFT):
            button = 9

        return button
        
    def close_window(self):
        '''Стирает окно'''
        for i in range(len(self.mas_sprite)):
            self.mas_sprite[i].kill()
        self.mas_sprite = []
        
