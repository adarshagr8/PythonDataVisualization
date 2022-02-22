import copy

# Represents each bar in the board
class Item:

    def __init__(self, name, icon, color, originalIndex, value=0):
        self.name = name
        self.icon = icon
        self.color = color
        self.originalIndex = originalIndex
        self.value = value
        self.out = False

# Contains all the items present in the board
class Board:

    def __init__(self, size=10, dec=True, W=1920, H=1080):
        self.items = []
        self.mn = 0
        self.mx = 0
        self.size = size
        self.graphWPer = 70
        self.graphHPer = 94
        self.barPer = 50
        self.sepPer = 1
        self.barLPer = (self.graphHPer - self.size * self.sepPer) / self.size
        self.iconPer = 9
        self.valuePer = 10
        self.leftPer = 20
        self.rightPer = 5
        self.headerPer = 15
        self.footerPer = 3
        self.circleRadius = 6
        self.clockPosW = 85
        self.clockPosH = 75

        self.W = W
        self.H = H
        self.dec = True

    def addItem(self, item):
        self.items.append(item)

    def sortItems(self):
        self.items.sort(key=lambda item: -item.value if self.dec else item.value)

    def top(self):
        self.sortItems()
        return self.items[:min(self.size, len(self.items))]

    def graphBeg(self):
        return (self.W * self.leftPer / 100, self.H * self.headerPer / 100)

    def findItem(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None


class State:

    def __init__(self):
        self.boards = []
        self.date = None
        self.duration = 0
        self.count = 0
        self.standstill = 3
        self.topPlaceItem = set()

    def updateState(self, board, date):
        copy_board = copy.deepcopy(board)
        copy_board.sortItems()
        self.topPlaceItem.add(copy_board.items[0].name)
        self.count += 1
        self.boards.append((date, copy_board))

    def currentBoard(self, t):
        unit_time = self.duration / self.count
        day_index = min(len(self.boards) - 1, int(t // unit_time))
        return self.boards[day_index]

    def nextBoard(self, t):
        unit_time = self.duration / self.count
        day_index = min(len(self.boards) - 1, int(t // unit_time))
        if day_index == len(self.boards) - 1:
            return None
        return self.boards[day_index + 1]

    def printState(self):
        for i in self.boards:
            for j in i[1].items:
                pass
                # print(vars(j))