# Represents each bar in the board
class Item:
    
    def __init__(self, name, icon, color, value=0):
        self.name = name
        self.icon = icon
        self.value = value
        self.color = color

# Contains all the items present in the board
class Board:
    
    def __init__(self, size=10):
        self.items = []
        self.mn = 0
        self.mx = 0
        self.size = size
    
    def addItem(self, item):
        self.items.append(item)
    
    def sortItems(self):
        self.items.sort(key = lambda item: -item.value)
    
    def top(self):
        self.sortItems()
        x = min(x, len(self.items))
        return self.Items[:self.size]
    
class State:
    
    def __init__(self):
        self.board = Board()
        self.date = Null
        
    def updateState(self, board, date):
        self.prevBoard = self.board
        self.board = board
        self.date = date

    def make_frame(self, t):

