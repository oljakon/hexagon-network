from game import chart
from game.network.network import *
from PyQt5.QtCore import pyqtSignal, QObject

class CommunicateLogic(QObject):
    sig = pyqtSignal(list)

class Logic:

    """в методе происходит передвижение армии + сражение"""
    def __init__(self, sig):
        self.sig_move_army = CommunicateLogic()
        self.sig_move_army.sig.connect(self.move_army_client)

        self.network = Network(sig, self.sig_move_army.sig)

    @staticmethod
    def move_army_client(args: list):
        chart.Chart().get_cell(args[0], args[1]).army.move_army(args[2], args[3])

    def move_army(self, i, j, i1, j1):
        Logic.move_army_client([i, j, i1, j1])
        self.network.move(i, j, i1, j1)

    @staticmethod
    def add_podsvet(i, j):
        chart.Chart().get_cell(i, j).army.add_podsvet()
        Network.add_podsvet(i, j)

    @staticmethod
    def delete_podsvet(i ,j):
        chart.Chart().get_cell(i, j).army.delete_podsvet()
        Network.delete_podsvet(i, j)

    @staticmethod
    def enter_ok(hiring, entered_cell):
        hiring.enter_ok(entered_cell.town.type_city)
        Network.buyArmy(entered_cell)

    def wait_other_player(self):
        self.network.wait_server()

    @staticmethod
    def end_move():
        Network.end_move()