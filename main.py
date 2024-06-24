import random
import os
from itertools import chain

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.print_board()

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

        print("Score:", self.score)
        for row in self.board:
            print(" | ".join("{:4}".format(tile) if tile != 0 else "    " for tile in row))
            print("-" * (self.size * 6 - 1))

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if empty_cells:
            (i, j) = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def move(self, direction):
        if direction == 'W':  # Up
            self.board = [list(x) for x in zip(*self.board)]
            self.board = [self.merge(row) for row in self.board]
            self.board = [list(x) for x in zip(*self.board)]
        elif direction == 'S':  # Down
            self.board = [list(x) for x in zip(*self.board[::-1])]
            self.board = [self.merge(row) for row in self.board]
            self.board = [list(x) for x in zip(*self.board[::-1])]
        elif direction == 'A':  # Left
            self.board = [self.merge(row) for row in self.board]
        elif direction == 'D':  # Right
            self.board = [self.merge(row[::-1])[::-1] for row in self.board]
        else:
            return False
        
        self.add_new_tile()
        self.print_board()
        return True

    def merge(self, row):
        new_row = [tile for tile in row if tile != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row[i + 1] = 0
        new_row = [tile for tile in new_row if tile != 0] + [0] * row.count(0)
        return new_row[:self.size]

    def check_win(self):
        return any(any(tile == 2048 for tile in row) for row in self.board)

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                    return False
        return True

    def play_game(self):
        while True:
            if self.check_win():
                print("Congratulations! You've reached 2048!")
                break
            if self.check_game_over():
                print("Game over! No more valid moves.")
                break
            
            move = input("Enter your move (W/A/S/D): ").upper()
            if move in ['W', 'A', 'S', 'D']:
                if not self.move(move):
                    print("Invalid move! Use W/A/S/D.")
            else:
                print("Invalid input! Use W/A/S/D.")

if __name__ == "__main__":
    game = Game2048()
    game.play_game()
