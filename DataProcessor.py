import csv
import classes
import matplotlib

state = classes.State()
board = classes.Board()

rows = []
with open("Data_Format.csv", 'r') as file:
    csvreader = csv.reader(file)

    # making Items
    name = next(csvreader)[1:]
    icon = next(csvreader)[1:]
    color = [matplotlib.colors.to_rgb(col) for col in next(csvreader)[1:]]

    # making Board at None date
    for i in range(len(name)):
        board.addItem(classes.Item(name[i], icon[i], color[i], i))

    # print(vars(vars(board)['items'][0]))
    for row in csvreader:
        date = row[0]
        print(date)
        values = row[1:]
        for i in range(len(values)):
            for item in vars(board)['items']:
                if vars(item)['originalIndex'] == i:
                    vars(item)['value'] = values[i]

        state.updateState(board, date)

        for st in vars(vars(state)['board'])['items']:
            print(vars(st))
