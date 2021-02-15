from game import *
from game.network.network import *

class Logic:

    """в методе происходит передвижение армии + сражение"""
    @staticmethod
    def move_army(i, j, i1, j1):
        chart.Chart().get_cell(i, j).army.move_army(i1, j1)
        Network.move(i, j, i1, j1)

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
