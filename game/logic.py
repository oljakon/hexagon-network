from game import chart
from game.network.network import *
from PyQt5.QtCore import pyqtSignal, QObject

class CommunicateLogic(QObject):
    sig = pyqtSignal(list)

class Logic:

    """в методе происходит передвижение армии + сражение"""
    def __init__(self, sig, sig_chg_move):
        self.sig_move_army = CommunicateLogic()
        self.sig_move_army.sig.connect(self.move_army_client)

        self.sig_add_podsvet = CommunicateLogic()
        self.sig_add_podsvet.sig.connect(self.add_podsvet_army)

        self.sig_delete_podsvet = CommunicateLogic()
        self.sig_delete_podsvet.sig.connect(self.delete_podsvet_army)

        self.sig_enter_ok = CommunicateLogic()
        self.sig_enter_ok.sig.connect(self.enter_ok_client)

        self.network = Network(sig, self.sig_move_army.sig,
                               sig_chg_move,
                               self.sig_add_podsvet.sig,
                               self.sig_delete_podsvet.sig,
                               self.sig_enter_ok.sig)


    @staticmethod
    def add_podsvet_army(args: list):
        chart.Chart().get_cell(args[0], args[1]).army.add_podsvet()

    @staticmethod
    def delete_podsvet_army(args: list):
        chart.Chart().get_cell(args[0], args[1]).army.delete_podsvet()

    @staticmethod
    def move_army_client(args: list):
        chart.Chart().get_cell(args[0], args[1]).army.move_army(args[2], args[3])

    @staticmethod
    def enter_ok_client(args: list):
        args[0].enter_ok(args[1].town.type_city, args[2])

    def move_army(self, i, j, i1, j1):
        Logic.move_army_client([i, j, i1, j1])
        self.network.move(i, j, i1, j1)

    def add_podsvet(self, i, j):
        Logic.add_podsvet_army([i, j])
        self.network.add_podsvet(i, j)

    def delete_podsvet(self, i ,j):
        Logic.delete_podsvet_army([i,j])
        self.network.delete_podsvet(i, j)

    def enter_ok(self, hiring, entered_cell):
        mas_label = self.enter_ok_client([hiring, entered_cell, None])
        self.network.buyArmy(hiring, entered_cell, mas_label)

    def wait_other_player(self):
        self.network.wait_server()

    def end_move(self):
        self.network.end_move()