# Fill the methods here
import numpy as np
import collections
import itertools
import csv




def string_puzzle_to_arr(puzzle):
    return np.array([list(map(int, line.strip())) for line in puzzle.split('\n') if line.strip()], dtype=int)

class Board:
    def __init__(self, puzzle):
        if isinstance(puzzle, str):
            puzzle = string_puzzle_to_arr(puzzle)
        self.arr = puzzle

    def get_row(self, row_index):
        return self.arr[row_index]

    def get_column(self, col_index):
        return self.arr[:, col_index]

    def get_block(self, pos_1, pos_2):
        row_start = pos_1 * 3
        col_start = pos_2 * 3
        return self.arr[row_start:row_start + 3, col_start:col_start + 3]

    def iter_rows(self):
        return [self.get_row(i) for i in range(9)]

    def iter_columns(self):
        return [self.get_column(i) for i in range(9)]

    def iter_blocks(self):
        return [self.get_block(i, j) for i in range(3) for j in range(3)]



def is_subset_valid(arr):
    count = dict(collections.Counter(arr.flatten()))
    if 0 in count:
        del count[0]
    return len([key for key, val in count.items() if val > 1]) == 0

def is_valid(board):
    rows = board.iter_rows()
    cols = board.iter_columns()
    blocks = board.iter_blocks()
    for subset in itertools.chain(rows, cols, blocks):
        if not is_subset_valid(subset):
            return False
    return True
    


def find_empty(board):
    empty_cells = np.argwhere(board.arr == 0)
    if len(empty_cells) == 0:
        return None
    return empty_cells




def is_full(board):
    return bool(np.sum(board.arr == 0) == 0)




def find_possibilities(board, x, y):
    block_pos_1, block_pos_2 = x // 3, y // 3
    all_elements = (board.get_row(x), board.get_column(y), board.get_block(block_pos_1, block_pos_2).flatten())
    values = np.concatenate(all_elements)
    non_zero = values[values != 0]
    uniques = np.unique(non_zero)
    return np.setdiff1d(np.arange(1, 10), uniques)


def adapt_long_sudoku_line_to_array(line):
    return np.array([int(c) for c in line]).reshape(9, 9)


def read_sudokus_from_csv(filename, read_solutions=False):
    index = 0 if not read_solutions else 1
    with open(filename) as fp:
        reader = csv.reader(fp)
        next(reader)  # يسكب الهيدر 
        puzzles = [
            adapt_long_sudoku_line_to_array(line[index])
            for line in reader
        ]
    return np.array(puzzles)


def detect_invalid_solutions(filename):
    solutions = read_sudokus_from_csv(filename, read_solutions=True)
    return np.array([solution for solution in solutions if not is_valid(Board(solution))])