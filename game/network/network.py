import socket
from time import sleep
from .HexagonProtocol import HexagonProtocol

from PyQt5.QtCore import pyqtSignal

class Network:

    # @staticmethod
    # def __send(message):
    #     print(message)
    def __init__(self, sig: pyqtSignal, sig_move_army: pyqtSignal):
        self.unlock_player = sig
        self.sig_move_army = sig_move_army
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

    def wait_server(self, type_action=""):
        data = self.s.recv(1000000)
        if type_action == 'start':
            return data
        else:
            while True:
                if data == 'move army':
                    self.sig_move_army([])
                if data == self.player:
                    self.unlock_player.emit()
                    return

    def end_move(self):
        send_mes_dict = {'session': self.session, 'player': self.player, 'type': 'end_move'}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)

        self.wait_server()

    def move(self, i, j, i1, j1):
        send_mes_dict = {'session': self.session, 'player': self.player, 'type': 'move', 'data': [i, j, i1, j1]}
        send_mes_bit = HexagonProtocol.getByteStrFromData(send_mes_dict)
        self.s.send(send_mes_bit)

    @staticmethod
    def add_podsvet(i, j):
        print('add podsvet for cell ' + str(i) + ' ' + str(j))

    @staticmethod
    def delete_podsvet(i, j):
        print('delete podsvet for cell ' + str(i) + ' ' + str(j))

    @staticmethod
    def buyArmy(cell):
        print('where is updated army - ' + str(cell.i) + ' ' + str(cell.j))

    # def attackArmy(self, army, winner):
    #     self.__send('winner player- ' + winner + 'army in cell' - army)
    #
    # def attackVillage(self, newOwner): # то же самое что и крепости???
    #     self.__send('newOwner - ' + newOwner)