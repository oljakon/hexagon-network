import pyglet
from cocos.actions import *
from cocos.sprite import Sprite
from game import chart


class Unit:
    """В классе хранится информация о количестве воинов в одном отряде и
    их характеристики"""

    def __init__(self, count, type_unit, stats):
        self.type_unit = type_unit
        self.count = count
        self.one_unit_attack = stats[1]
        self.one_unit_defense = stats[2]
        self.one_unit_hp = stats[0]
        self.update_all()

    def update_all(self):
        """Перерасчет общих характеристик"""
        self.attack = self.one_unit_attack * self.count
        self.defense = self.one_unit_defense * self.count
        self.hp = self.one_unit_hp * self.count

class Army:
    """Хранит массив объектов юнита и отвечает за перемещения и сражения"""
    deviation_x = 10
    deviation_y = -5
    move_time = 0.5
    scale_time = 0.5
    scale_size = 1.5
    rotation_degree = 20
    rotation_time = 0.2
    blink_times = 5

    def __init__(self, one_unit, i, j):
        self.i = i
        self.j = j
        self.move = True
        self.player = chart.Chart().get_cell(self.i, self.j).properties['player']

        self.x = chart.Chart().get_cell(self.i, self.j).center[0]
        self.y = chart.Chart().get_cell(self.i, self.j).center[1]
        self.mas_sprite = ['peasant' + str(self.player) + '.png',
                           'priest' + str(self.player) + '.png',
                           'soldier' + str(self.player) + '.png',
                           'knight' + str(self.player) + '.png']

        self.army = [one_unit]
        self.type_army_global = self.army[0].type_unit
        self.xy = [self.x + self.deviation_x, self.y + self.deviation_y]

        self.sprite = Sprite(self.mas_sprite[self.type_army_global-1])
        self.sprite.position = self.xy
        self.sprite.scale = 1.4
        chart.Chart().add(self.sprite)

        self.sprite_kletka = []


    def step(self, i1, j1, i2, j2):
        """
        Проверка дальних клеток на возможность хода в них,
        если их предшественники отсутствуют
        """
        def check(i1, j1, i2, j2):
            """Проверка области и рельефа куда может пойти армия"""
            if i1 == i2 and j1 == j2:
                return False
            elif chart.Chart().get_cell(i2, j2).properties['relief'] == 0:
                return False
            elif abs(i1 - i2) <= 2 and abs(j1 - j2) <= 1:
                return True
            elif i1 == i2 and abs(j1 - j2) <= 2:
                return True
            elif (abs(i1 - i2) <= 1 and j2 - j1 == 2 and i2 % 2 == 0) or\
                 (abs(i1 - i2) <= 1 and j1 - j2 == 2 and i2 % 2 == 1):
                return True
            else:
                return False

        if check(i1, j1, i2, j2):
            x1, x2, x3, x4, x5, x6 = False, False, False, False, False, False

            # для чётных клеток
            if i1 % 2 == 0:
                if j1+1 < 11:
                    if check(i1, j1, i1, j1+1):
                        x1 = True
                if i1+1 < 22:
                    if check(i1, j1, i1+1, j1):
                        x2 = True
                if i1+1 < 22 and j1-1 > -1:
                    if check(i1, j1, i1+1, j1-1):
                        x3 = True
                if j1-1 > -1:
                    if check(i1, j1, i1, j1-1):
                        x4 = True
                if i1-1 > -1 and j1-1 > -1:
                    if check(i1, j1, i1-1, j1-1):
                        x5 = True
                if i1-1 > -1:
                    if check(i1, j1, i1-1, j1):
                        x6 = True

                if j2 == j1 and i1 == i2:
                    return False

                # нахождение соседей
                if j2 == j1+1 and i1 == i2 and x1:
                    return True
                if i2 == i1+1 and j2 == j1 and x2:
                    return True
                if i2 == i1+1 and j2 == j1-1 and x3:
                    return True
                if i2 == i1 and j2 == j1-1 and x4:
                    return True
                if i2 == i1-1 and j2 == j1-1 and x5:
                    return True
                if i2 == i1-1 and j2 == j1 and x6:
                    return True

                # нахождение дальних клеток
                if i2 == i1 and j2 == j1+2 and x1:
                    return True
                if i2 == i1+1 and j2 == j1+1 and (x1 or x2):
                    return True
                if i2 == i1+2 and j2 == j1+1 and x2:
                    return True
                if i2 == i1+2 and j2 == j1 and (x2 or x3):
                    return True
                if i2 == i1+2 and j2 == j1-1 and x3:
                    return True
                if i2 == i1+1 and j2 == j1-2 and (x3 or x4):
                    return True
                if i2 == i1 and j2 == j1-2 and x4:
                    return True

                if i2 == i1-1 and j2 == j1-2 and (x4 or x5):
                    return True
                if i2 == i1-2 and j2 ==j1-1 and x5:
                    return True
                if i2 == i1-2 and j2 == j1 and (x5 or x6):
                    return True
                if i2 == i1-2 and j2 == j1+1 and x6:
                    return True
                if i2 == i1-1 and j2 == j1+1 and (x6 or x1):
                    return True

                return False

            #для нечетной
            else:
                if j1+1 < 11:
                    if check(i1, j1, i1, j1+1):
                        x1 = True
                if i1+1 < 22:
                    if check(i1, j1, i1+1, j1):
                        x2 = True
                if i1+1 < 22 and j1+1 < 22:
                    if check(i1, j1, i1+1, j1+1):
                        x3 = True
                if j1-1 > -1:
                    if check(i1, j1, i1, j1-1):
                        x4 = True
                if i1-1 > -1 and j1+1 < 22:
                    if check(i1, j1, i1-1, j1+1):
                        x5 = True
                if i1-1 > -1:
                    if check(i1, j1, i1-1, j1):
                        x6 = True

                if j2 == j1 and i1 == i2:
                    return False

                # нахождение соседей
                if j2 == j1+1 and i1 == i2 and x1:
                    return True
                if i2 == i1+1 and j2 == j1 and x2:
                    return True
                if i2 == i1+1 and j2 == j1+1 and x3:
                    return True
                if i2 == i1 and j2 == j1-1 and x4:
                    return True
                if i2 == i1-1 and j2 == j1+1 and x5:
                    return True
                if i2 == i1-1 and j2 == j1 and x6:
                    return True

                # нахождение дальних клеток
                if i2 == i1 and j2 == j1+2 and x1:
                    return True
                if i2 == i1+1 and j2 == j1+2 and (x1 or x3):
                    return True
                if i2 == i1+2 and j2 == j1+1 and x3:
                    return True
                if i2 == i1+2 and j2 == j1 and (x2 or x3):
                    return True
                if i2 == i1+2 and j2 == j1-1 and x2:
                    return True
                if i2 == i1+1 and j2 == j1-1 and (x2 or x4):
                    return True
                if i2 == i1 and j2 == j1-2 and x4:
                    return True

                if i2 == i1-1 and j2 == j1-1 and (x4 or x6):
                    return True
                if i2 == i1-2 and j2 ==j1-1 and x6:
                    return True
                if i2 == i1-2 and j2 == j1 and (x5 or x6):
                    return True
                if i2 == i1-2 and j2 == j1+1 and x5:
                    return True
                if i2 == i1-1 and j2 == j1+2 and (x5 or x1):
                    return True

                return False


    def add_podsvet(self):
        '''Добавляет подсветку клеткам'''
        if chart.Chart().get_cell(self.i,self.j).army != None:
           if chart.Chart().get_cell(self.i, self.j).army.player != 0:
                if self.move:
                    for k in range(22):
                        for m in range(11):
                            if self.step(self.i, self.j, k, m):
                                if chart.Chart().get_cell(k,m).army:
                                    if chart.Chart().get_cell(k,m).army.player !=\
                                       chart.Chart().get_cell(self.i,self.j).army.player:
                                        sprite_kletka = Sprite('podsvet_attack.png')
                                    else:
                                        sprite_kletka = Sprite('podsvet.png')
                                else:
                                    sprite_kletka = Sprite('podsvet.png')

                                x = chart.Chart().get_cell(k, m).center[0]
                                y = chart.Chart().get_cell(k, m).center[1]
                                sprite_kletka.position = [x,y]
                                self.sprite_kletka.append(sprite_kletka)

                    for i in range(len(self.sprite_kletka)):
                        chart.Chart().add(self.sprite_kletka[i])

    def delete_podsvet(self):
        """Удаляет подсвеченные клетки"""
        for i in range(len(self.sprite_kletka)):
            self.sprite_kletka[i].kill()
        self.sprite_kletka = []

    def move_army(self, i1, j1):
        """Перемещает армию по указанной клетке"""
        if self.step(self.i, self.j, i1, j1) and self.move:
            self.delete_podsvet()

            army1 = chart.Chart().get_cell(self.i, self.j).army
            army2 = chart.Chart().get_cell(i1, j1).army

            if army2 != None:
                #Случай для слияния двух армий одного игрока
                if army2.player == army1.player:
                    # Проверка на возможность слияния
                    if self.__check_count_armies(army2):
                        self.x = chart.Chart().get_cell(i1, j1).center[0]
                        self.y = chart.Chart().get_cell(i1, j1).center[1]
                        self.xy = [self.x + self.deviation_x, self.y + self.deviation_y]

                        chart.Chart().get_cell(i1, j1).army.sprite.do(Delay(self.move_time)
                                        +ScaleBy(self.scale_size,self.scale_time)
                                        +Reverse(ScaleBy(self.scale_size,self.scale_time))
                                        +Hide())
                        chart.Chart().get_cell(i1,j1).leave_cell()
                        self.merge_army(army2, False)
                        self.sprite.do(MoveTo(self.xy, self.move_time)
                                       +Hide()+Delay(2*self.move_time)
                                       +CallFunc(self.new_sprite))

                        chart.Chart().get_cell(i1, j1).enter_cell(self)
                        chart.Chart().get_cell(self.i, self.j).leave_cell()
                        self.i = i1
                        self.j = j1
                        self.move = False
                    else:
                        self.sprite.do(MoveTo([chart.Chart().get_cell(i1, j1).center[0]
                                +self.deviation_x,chart.Chart().get_cell(i1, j1).center[1]
                                +self.deviation_y], self.move_time)+
                                Rotate(-self.rotation_degree,self.rotation_time)+
                                Rotate(2*self.rotation_degree,self.rotation_time)+
                                Rotate(-self.rotation_degree,self.rotation_time)+
                                MoveTo(self.xy, self.move_time))

                # Сражение двух армий
                else:
                    mas_army = [1,2]
                    attack_army1, defense_army1, attack_army2, defense_army2 = 0,0,0,0

                    for i in range(len(army1.army)):
                        attack_army1 += army1.army[i].attack
                        defense_army1 += army1.army[i].defense
                    for i in range(len(army2.army)):
                        attack_army2 += army2.army[i].attack
                        defense_army2 += army2.army[i].defense

                    if attack_army1 <= defense_army2 and attack_army2 <= defense_army1:
                        self.x = chart.Chart().get_cell(i1, j1).center[0]
                        self.y = chart.Chart().get_cell(i1, j1).center[1]
                        self.xy = [self.x + self.deviation_x, self.y + self.deviation_y]
                        self.sprite.do(MoveTo(self.xy, self.move_time))

                        chart.Chart().get_cell(i1,j1).army.sprite.do(Blink(self.blink_times,
                                                                           self.move_time)
                                                                    +Hide())
                        chart.Chart().get_cell(i1,j1).leave_cell()
                        chart.Chart().get_cell(i1,j1).enter_cell(army1)
                        chart.Chart().get_cell(self.i, self.j).leave_cell()
                        self.i = i1
                        self.j = j1
                        self.move = False

                    else:
                        while len(chart.Chart().get_cell(self.i, self.j).army.army) and\
                              len(chart.Chart().get_cell(i1, j1).army.army):
                            self.__attack(chart.Chart().get_cell(self.i, self.j).army,\
                                   chart.Chart().get_cell(i1, j1).army)
                            chart.Chart().get_cell(self.i, self.j).army,\
                            chart.Chart().get_cell(i1, j1).army =\
                            chart.Chart().get_cell(i1, j1).army, \
                            chart.Chart().get_cell(self.i, self.j).army
                            mas_army[0], mas_army[1] = mas_army[1], mas_army[0]

                        if mas_army[0] != 1:
                            chart.Chart().get_cell(self.i, self.j).army,\
                            chart.Chart().get_cell(i1, j1).army =\
                            chart.Chart().get_cell(i1, j1).army, \
                            chart.Chart().get_cell(self.i, self.j).army

                        if len(chart.Chart().get_cell(self.i, self.j).army.army):
                            self.x = chart.Chart().get_cell(i1, j1).center[0]
                            self.y = chart.Chart().get_cell(i1, j1).center[1]
                            self.xy = [self.x + self.deviation_x,
                                       self.y + self.deviation_y]
                            self.sprite.do(MoveTo(self.xy, self.move_time))

                            chart.Chart().get_cell(i1,j1).army.sprite.do(Blink(\
                                self.blink_times,self.move_time)+Hide())
                            chart.Chart().get_cell(i1,j1).leave_cell()
                            chart.Chart().get_cell(i1,j1).enter_cell(chart.Chart().
                                                        get_cell(self.i,self.j).army)
                            chart.Chart().get_cell(self.i, self.j).leave_cell()
                            self.i = i1
                            self.j = j1
                            self.move = False

                        else:
                            self.x = chart.Chart().get_cell(i1, j1).center[0]
                            self.y = chart.Chart().get_cell(i1, j1).center[1]
                            self.xy = [self.x, self.y]
                            self.sprite.do(MoveTo(self.xy, self.move_time)+
                                           Blink(self.blink_times,self.move_time)
                                           +Hide())
                            chart.Chart().get_cell(self.i, self.j).leave_cell()

            elif army2 == None:
                chart.Chart().get_cell(i1, j1).enter_cell(army1)
                chart.Chart().get_cell(self.i, self.j).leave_cell()
                self.x = chart.Chart().get_cell(i1, j1).center[0]
                self.y = chart.Chart().get_cell(i1, j1).center[1]
                self.xy = [self.x + self.deviation_x, self.y + self.deviation_y]
                self.sprite.do(MoveTo(self.xy, self.move_time))

                self.i = i1
                self.j = j1
                self.move = False

    def __attack(self, army1, army2):
        """Сражение двух армий, когда армия1 атакует армию2"""
        attack, defense, attack_hp = 0,0,0
        for i in range(len(army1.army)):
            attack += army1.army[i].attack
        for i in range(len(army2.army)):
            defense += army2.army[i].defense

        if defense < attack:
            attack_hp = attack - defense
        del_one_unit = 0
        del_units = 0
        for i in range(len(army2.army)):
            for k in range(army2.army[i].count):
                if attack_hp >= army2.army[i].one_unit_hp:
                    del_one_unit += 1
                    attack_hp -= army2.army[i].one_unit_hp
                else:
                    del_one_unit += 1
                    attack_hp = 0
                    break

            if del_one_unit == army2.army[i].count:
                del_units += 1
            else:
                army2.army[i].count -= del_one_unit
            del_one_unit = 0

            if attack_hp == 0:
                break

        army2.army = army2.army[del_units:]

        for i in range(len(army2.army)):
            army2.army[i].update_all()


    def merge_unit(self, one_unit, boole = 'unit'):
        """Слияние нового войска с армией"""
        count_army = 0
        max_army = chart.Chart().get_cell(self.i,self.j).properties['capacity']
        for i in range(len(self.army)):
            count_army += self.army[i].count
        if (one_unit.count+count_army) > max_army:
            one_unit.count = max_army - count_army

        if one_unit.count != 0:
            for i in range(len(self.army)):
                if self.army[i].type_unit == one_unit.type_unit and \
                   self.army[i].one_unit_attack == one_unit.one_unit_attack and\
                   self.army[i].one_unit_defense == one_unit.one_unit_defense and\
                   self.army[i].one_unit_hp == one_unit.one_unit_hp:
                    self.army[i].count += one_unit.count
                    break
            else:
                self.army.append(one_unit)
            for i in range(len(self.army)):
                self.army[i].update_all()

        if boole == 'unit':
            self.__update()


    def __check_count_armies(self, one_army):
        """Проверка на возможность слияния двух армий"""
        count1 = 0
        count2 = 0
        max_army = chart.Chart().get_cell(self.i,self.j).properties['capacity']
        for i in range(len(self.army)):
            count1 += self.army[i].count
        for i in range(len(one_army.army)):
            count2 += one_army.army[i].count
        if (count1 + count2) <= max_army and (self.player == one_army.player\
                                              or one_army.player == 0):
            return True
        else:
            return False

    def merge_army(self, one_army, UPDATE = True):
        """Слияние двух армий"""
        if self.__check_count_armies(one_army):
            for i in range(len(one_army.army)):
                self.merge_unit(one_army.army[i], boole = 'army')
        if UPDATE == True:
            self.__update()

    def new_sprite(self):
        """Добавление нового спрайта для корректной анимации армии"""
        for i in range(len(self.army)):
            if i == 0:
                c = self.army[0].count
                type_unit = self.army[0].type_unit

            elif self.army[i].type_unit == type_unit:
                c += self.army[i].count

            elif self.army[i].count > c:
                c = self.army[i].count
                type_unit = self.army[i].type_unit

        self.sprite = Sprite(self.mas_sprite[type_unit-1])
        self.sprite.scale = 1.4
        self.sprite.position = self.xy
        chart.Chart().add(self.sprite)

    def change_player(self, player):
        """Смена принадлежности армии к игроку и изображения армии"""
        self.player = player
        self.mas_sprite = ['peasant' + str(self.player) + '.png',
                           'priest' + str(self.player) + '.png',
                           'soldier' + str(self.player) + '.png',
                           'knight' + str(self.player) + '.png']
        new_image = pyglet.resource.image(self.mas_sprite\
                                              [self.type_army_global-1])
        self.sprite.image = new_image

    def __update(self):
        """Обновление визуализации армии"""
        for i in range(len(self.army)):
            if i == 0:
                c = self.army[0].count
                type_unit = self.army[0].type_unit

            elif self.army[i].type_unit == type_unit:
                c += self.army[i].count

            elif self.army[i].count > c:
                c = self.army[i].count
                type_unit = self.army[i].type_unit

        if self.type_army_global != type_unit:
            self.type_army_global = type_unit
            new_image = pyglet.resource.image(self.mas_sprite\
                                              [self.type_army_global-1])
            self.sprite.image = new_image
