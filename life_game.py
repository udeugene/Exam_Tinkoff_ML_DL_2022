from time import sleep
import argparse
import random


class Cell:
    def __init__(self, live=False):
        self.live = live
        self.n_neighbors = 0


class Field:
    def __init__(self, a=10, b=10, n=None):
        self.a = a
        self.b = b
        if not n:
            self.n = a * b // 5
        else:
            self.n = n
        self.field = [Cell() for i in range(self.a * self.b)]

    def reshaper(self, inplace=True):
        if inplace:
            if len(self.field) == self.a * self.b:
                self.field = [[self.field[self.a * i + j] for j in range(self.a)] for i in
                              range(len(self.field) // self.a)]
            else:
                self.field = [cell for cell_field in self.field for cell in cell_field]
        else:
            return [[self.field[self.a * i + j] for j in range(self.a)] for i in range(len(self.field) // self.a)]

    def create_population(self):
        indices = random.sample(list(range(self.a * self.b)), self.n)
        for i in indices:
            self.field[i].live = True

    def count_neighbors(self):
        self.reshaper()
        for rowNumber in range(self.a):
            for colNumber in range(self.b):
                for rowAdd in range(-1, 2):
                    newRow = rowNumber + rowAdd
                    if newRow >= 0 and newRow <= len(self.field) - 1:
                        for colAdd in range(-1, 2):
                            newCol = colNumber + colAdd
                            if newCol >= 0 and newCol <= len(self.field) - 1:
                                if newCol == colNumber and newRow == rowNumber:
                                    continue
                                if self.field[newRow][newCol].live:
                                    self.field[rowNumber][colNumber].n_neighbors += 1
        self.reshaper()

    def reset_neighbors(self):
        for cell in self.field:
            cell.n_neighbors = 0

    def new_gen(self):
        for cell in self.field:
            if cell.n_neighbors not in [2, 3]:
                cell.live = False
            elif cell.n_neighbors == 3:
                cell.live = True

    def plotter(self):
        live_symb = '\u2588\u2588'
        not_live_symb = '  '
        to_print = ''
        print_data = self.reshaper(inplace=False)
        for row in print_data:
            to_print += "-" * 3 * self.a + '\n'
            to_print += ('|')
            for cell in row:
                if cell.live:
                    to_print += live_symb + '|'
                else:
                    to_print += not_live_symb + '|'
            to_print += '\n'
        print(to_print)

    def start_simulation(self, n_iter=10):
        self.create_population()
        print('Initial population')
        self.plotter()
        sleep(1)
        for i in range(n_iter):
            print(f'Iteration number {i+1}')
            self.reset_neighbors()
            self.count_neighbors()
            self.new_gen()
            self.plotter()
            sleep(1)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('a', type = int)
    argparser.add_argument('b', type = int)
    argparser.add_argument('-n', type = int)
    argparser.add_argument('-n_iter', type = int, default=5)
    args = argparser.parse_args()

    game = Field(a=args.a, b=args.b, n=args.n)
    game.start_simulation(n_iter=args.n_iter)
