# Represents each bar in the board
class Item:
    
    def __init__(self, name, icon, color, value=0):
        self.name = name
        self.icon = icon
        self.value = value
        self.color = color

# Contains all the items present in the board
class Board:
    
    def __init__(self, size=10, dec=True):
        self.items = []
        self.mn = 0
        self.mx = 0
        self.size = size
        self.graphWPer = 70
        self.graphHPer = 90
        self.leftPer = 30
        self.dec = True
    
    def addItem(self, item):
        self.items.append(item)
    
    def sortItems(self):
        self.items.sort(key = lambda item: -item.value if dec else item.value)
    
    def top(self):
        self.sortItems()
        x = min(x, len(self.items))
        return self.Items[:self.size]
    
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


