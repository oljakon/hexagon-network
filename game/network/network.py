class Network:


    def __send(self, message):
        print(message)


    def move(self, cellStart, cellEnd):
        self.__send('moved from' + cellStart + ' to ' + cellEnd)

    def attackArmy(self, army, winner):
        self.__send('winner player- ' + winner + 'army in cell' - army)

    def attackVillage(self, newOwner): # то же самое что и крепости???
        self.__send('newOwner - ' + newOwner)

    def buyArmy(self, cellPurchase, curArmy):
        self.__send('where is updated army - ' + cellPurchase + ' current army"s statment -' + curArmy)
