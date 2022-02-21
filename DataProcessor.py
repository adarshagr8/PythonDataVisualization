import csv
import classes
import matplotlib


class DataProcessor:
    state = classes.State()
    board = classes.Board()

    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as file:
            csvreader = csv.reader(file)

            # making Items
            name = next(csvreader)[1:]
            icon = next(csvreader)[1:]
            color = [matplotlib.colors.to_rgb(col)
                     for col in next(csvreader)[1:]]

            # making Board at None date
            for i in range(len(name)):
                self.board.addItem(classes.Item(name[i], icon[i], color[i], i))

            for row in csvreader:
                date = row[0]
                values = row[1:]
                for i in range(len(values)):
                    for item in vars(self.board)['items']:
                        if vars(item)['originalIndex'] == i:
                            vars(item)['value'] = int(values[i])

                self.state.updateState(self.board, date)

                # Print data
                # for item in vars(self.board)['items']:
                #     print(vars(item))
