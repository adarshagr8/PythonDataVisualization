class Item:
    
    def __init__(self, name, icon, color, value=0):
        self.name = name
        self.icon = icon
        self.value = value
        self.color = color

class Board:
    
    def __init__():
        self.items = []
    
    def addItem(self, item):
        self.items.append(item)
    
    def sortItems(self):
        self.items.sort(key = lambda item: -item.value)
    
    def topX(self, x = 10):
        self.sortItems()
        x = min(x, len(self.items))
        return self.Items[:x]
    
class State:
    
    def __init__(self):
        self.board = Board()
        self.date = Null
        
    def updateState(self, board, date):
        self.prevBoard = self.board
        self.board = board
        self.date = date
