import copy

# Represents each bar in the board
class Item:

    def __init__(self, name, icon, color, originalIndex, value=0):
        self.name = name
        self.icon = icon
        self.color = color
        self.originalIndex = originalIndex
        self.value = value

# Contains all the items present in the board


class Board:

    def __init__(self, size=10, dec=True, W=1920, H=1080):
        self.items = []
        self.mn = 0
        self.mx = 0
        self.size = size
        self.graphWPer = 70
        self.graphHPer = 90
        self.barPer = 50
        self.barLPer = 8
        self.sepPer = 1
        self.iconPer = 8
        self.valuePer = 10
        self.leftPer = 25
        self.rightPer = 5
        self.headerPer = 7
        self.footerPer = 3
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
        return (self.H * self.headerPer / 100, self.W * self.rightPer / 100)

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

    def updateState(self, board, date):
        self.count += 1
        self.boards.append((date, copy.deepcopy(board)))

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