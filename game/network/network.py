class Network:

    # @staticmethod
    # def __send(message):
    #     print(message)

    @staticmethod
    def move(i, j, i1, j1):
        print('moved from ' + str(i) + ' ' + str(j) + ' to ' + str(i1) + ' ' + str(j1))

    @staticmethod
    def add_podsvet(i, j):
        print('add podsvet for cell ' + str(i) + ' ' + str(j))

    @staticmethod
    def delete_podsvet(i, j):
        print('delete podsvet for cell ' + str(i) + ' ' + str(j))

    @staticmethod
    def buyArmy(cellPurchase, curArmy):
        print('where is updated army - ' + cellPurchase + ' current army"s statment -' + curArmy)

    # def attackArmy(self, army, winner):
    #     self.__send('winner player- ' + winner + 'army in cell' - army)
    #
    # def attackVillage(self, newOwner): # то же самое что и крепости???
    #     self.__send('newOwner - ' + newOwner)