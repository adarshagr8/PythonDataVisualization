import csv
import classes
import matplotlib


class DataProcessor:
    state = classes.State()
    board = classes.Board()

    def __init__(self, path):
        self.path = path

    def makeAndUpdateBoards(self):
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
                print(date)
                values = row[1:]
                for i in range(len(values)):
                    for item in vars(self.board)['items']:
                        if vars(item)['originalIndex'] == i:
                            vars(item)['value'] = values[i]

                self.state.updateState(date, self.board)

                # Print data
                # for item in vars(self.board)['items']:
                #     print(vars(item))
