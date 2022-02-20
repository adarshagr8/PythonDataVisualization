# Represents each bar in the board
class Item:
    
    def __init__(self, name, icon, color, value=0):
        self.name = name
        self.icon = icon
        self.value = value
        self.color = color

# Contains all the items present in the board
class Board:
    
    def __init__(self, size=10, dec=True, W=1920, H=1080):
        self.items = []
        self.mn = 0
        self.mx = 0
        self.size = size
        self.graphWPer = 70
        self.graphHPer = 90
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
        self.items.sort(key = lambda item: -item.value if dec else item.value)
    
    def top(self):
        self.sortItems()
        x = min(x, len(self.items))
        return self.Items[:self.size]
    
    def graphBeg(self):
        return (self.H * self.headerPer / 100, self.W * self.rightPer / 100)

class State:
    
    def __init__(self, duration, count):
        self.boards = []
        self.date = Null
        self.duration = duration
        self.count = count
        
    def updateState(self, board, date):
        self.boards.append((date, board))

    def currentBoard(self, t):
        unit_time = duration / count
        day_index = t / unit_time
        return self.boards[day_index]


