import socket
from time import sleep
from .HexagonProtocol import HexagonProtocol

from PyQt5.QtCore import pyqtSignal

NUM_PLAYERS = 2

class Network:

    # @staticmethod
    # def __send(message):
    #     print(message)
    def __init__(self, sig: pyqtSignal, sig_move_army: pyqtSignal, sig_chg_move: pyqtSignal, sig_add_podsvet: pyqtSignal, sig_delete_podsvet: pyqtSignal):
        self.unlock_player = sig
        self.sig_move_army = sig_move_army
        self.sig_chg_move = sig_chg_move
        self.sig_add_podsvet = sig_add_podsvet
        self.sig_delete_podsvet = sig_delete_podsvet
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '188.244.6.5'
        port = 1322
        self.s.connect((host, port))

        send_mes_dict = {'type': 'connect'}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)

        data = self.s.recv(1000000)
        dict_get = HexagonProtocol.getDataFromByteStr(data)
        print(dict_get)

        self.player = dict_get['player']
        self.session = dict_get['session']

        data = self.s.recv(1000000)
        dict_get = HexagonProtocol.getDataFromByteStr(data)
        print(dict_get)

        # print('received', data.decode(encoding='utf-8'), len(data), 'bytes')
        # self.s.send(bytes('finish', encoding='utf-8'))



        # data = self.wait_server()
        # проверка что data == start
        # if self.player == dict_get['type']: # тут нужно получить номер игрока который ходит от сервера
        if self.player == 0:
            self.unlock_player.emit()

    def __del__(self):
        self.s.close()

    def wait_server(self):
        print('waiting')
        data = self.s.recv(1000000)
        print(len(data))
        dict_get = HexagonProtocol.getDataFromByteStr(data)
        if dict_get['type'] == 'move':
            self.sig_move_army.emit(dict_get['data'])
        elif dict_get['type'] == 'add_podsvet':
            self.sig_add_podsvet.emit(dict_get['data'])
        elif dict_get['type'] == 'delete_podsvet':
            self.sig_delete_podsvet.emit(dict_get['data'])
        elif dict_get['type'] == 'end_move':
            print('end_move got from player', dict_get['player'])
            if dict_get['player'] != self.player:
                self.sig_chg_move.emit()
                if (dict_get['player'] + 1) % NUM_PLAYERS == self.player:
                    self.unlock_player.emit()

    def end_move(self):
        send_mes_dict = {'session': self.session, 'player': self.player, 'type': 'end_move'}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)
        print('end_move sended')

        # self.wait_server()

    def move(self, i, j, i1, j1):
        send_mes_dict = {'session': self.session, 'player': self.player, 'type': 'move', 'data': [i, j, i1, j1]}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)

    def add_podsvet(self, i, j):
        send_mes_dict = {'session': self.session, 'player': self.player, 'type': 'add_podsvet', 'data': [i, j]}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)

    def delete_podsvet(self, i, j):
        send_mes_dict = {'session': self.session, 'player': self.player, 'type': 'delete_podsvet', 'data': [i, j]}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)

    @staticmethod
    def buyArmy(cell):
        print('where is updated army - ' + str(cell.i) + ' ' + str(cell.j))

    # def attackArmy(self, army, winner):
    #     self.__send('winner player- ' + winner + 'army in cell' - army)
    #
    # def attackVillage(self, newOwner): # то же самое что и крепости???
    #     self.__send('newOwner - ' + newOwner)