import tkinter as tk
import random
import time

class Tetris:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.canvas = tk.Canvas(self.root, width=300, height=600, bg="black")
        self.canvas.pack()
        self.board = [[0] * 10 for _ in range(20)]
        self.score = 0
        self.delay = 500
        self.game_over = False
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[1, 1], [1, 1]]
        ]
        self.current_shape = random.choice(self.shapes)
        self.current_x = 5
        self.current_y = 0
        self.draw_board()
        self.draw_shape()
        self.root.bind("<Left>", lambda e: self.move_shape(-1))
        self.root.bind("<Right>", lambda e: self.move_shape(1))
        self.root.bind("<Down>", lambda e: self.move_down())
        self.root.bind("<space>", lambda e: self.rotate_shape())
        self.root.after(self.delay, self.update)
        self.root.mainloop()
        self.high_score = self.load_high_score()
        self.update_title()

    """ハイスコアをファイルから読み込む"""
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.load())
        except FileNotFoundError:
            return 0

    """ハイスコアをファイルに保存する"""
    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

    def draw_board(self):
        self.canvas.delete("shape")
        for y in range(20):
            for x in range(10):
                if self.board[y][x]:
                    self.canvas.create_rectangle(
                        x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill="blue", tags="shape")

    def draw_shape(self):
        self.canvas.delete("current_shape")
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x]:
                    self.canvas.create_rectangle(
                        (self.current_x + x) * 30, (self.current_y + y) * 30,
                        (self.current_x + x + 1) * 30, (self.current_y + y + 1) * 30,
                        fill="red", tags="current_shape")

    def move_shape(self, dx):
        if not self.game_over:
            if 0 <= self.current_x + dx < 10 and not self.collides(dx, 0):
                self.current_x += dx
                self.draw_shape()

    def move_down(self):
        if not self.game_over:
            if not self.collides(0, 1):
                self.current_y += 1
                self.draw_shape()
            else:
                self.freeze_shape()
                self.clear_lines()
                self.new_shape()

    def rotate_shape(self):
        if not self.game_over:
            rotated_shape = list(zip(*self.current_shape[::-1]))
            if not self.collides(0, 0, rotated_shape):
                self.current_shape = rotated_shape
                self.draw_shape()

    def collides(self, dx, dy, shape=None):
        shape = shape or self.current_shape
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] and (
                        not 0 <= self.current_x + x + dx < 10 or
                        not 0 <= self.current_y + y + dy < 20 or
                        self.board[self.current_y + y + dy][self.current_x + x + dx]):
                    return True
        return False

    def freeze_shape(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[y])):
                if self.current_shape[y][x]:
                    self.board[self.current_y + y][self.current_x + x] = 1

    def clear_lines(self):
        lines_to_clear = []
        for y in range(20):
            if all(self.board[y]):
                lines_to_clear.append(y)
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0] * 10)
            self.score += 1
        self.root.title("Tetris - Score: {}".format(self.score))

    def new_shape(self):
        self.current_shape = random.choice(self.shapes)
        self.current_x = 5
        self.current_y = 0
        if self.collides(0, 0):
            self.game_over = True
            self.canvas.create_text(
                150, 300, text="Game Over", font=("Helvetica", 36), fill="white")

    def update(self):
        if not self.game_over:
            self.move_down()
        self.draw_board()
        if not self.game_over:
            self.root.after(self.delay, self.update)

if __name__ == "__main__":
    Tetris()
