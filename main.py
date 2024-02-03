import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

window_size = (450, 500)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic Tac Toe Game")


class TicTacToe:
    def __init__(self, table_size):
        self.table_size = table_size
        self.cell_size = table_size // 3
        self.table_space = 20

        self.player = "X"
        self.winner = None
        self.taking_move = True
        self.running = True
        self.table = []
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")

        self.background_color = (255, 174, 66)
        self.table_color = (50, 50, 50)
        self.line_color = (190, 0, 10)
        self.instructions_color = (17, 53, 165)
        self.game_over_bg_color = (47, 98, 162)
        self.game_over_color = (255, 179, 1)
        self.font = pygame.font.SysFont("Courier New", 35)
        self.FPS = pygame.time.Clock()

    # menggambar representasi tabel
    def draw_table(self):
        tb_space_point = (self.table_space, self.table_size - self.table_space)
        cell_space_point = (self.cell_size, self.cell_size * 2)
        r1 = pygame.draw.line(
            screen,
            self.table_color,
            [tb_space_point[0], cell_space_point[0]],
            [tb_space_point[1], cell_space_point[0]],
            8,
        )
        c1 = pygame.draw.line(
            screen,
            self.table_color,
            [cell_space_point[0], tb_space_point[0]],
            [cell_space_point[0], tb_space_point[1]],
            8,
        )
        r2 = pygame.draw.line(
            screen,
            self.table_color,
            [tb_space_point[0], cell_space_point[1]],
            [tb_space_point[1], cell_space_point[1]],
            8,
        )
        c2 = pygame.draw.line(
            screen,
            self.table_color,
            [cell_space_point[1], tb_space_point[0]],
            [cell_space_point[1], tb_space_point[1]],
            8,
        )
    # untuk memproses pergantian pemain

    def change_player(self):
        self.player = "O" if self.player == "X" else "X"

    # memproses klik untuk memindahkan
    def move(self, pos):
        try:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            if self.table[x][y] == "-":
                self.table[x][y] = self.player
                self.draw_char(x, y, self.player)
                self.game_check()
                self.change_player()
        except:
            print("Only click what's in the table")

    # menggambar karakter pemain terakhir ke sel tabel yang dipilih
    def draw_char(self, x, y, player):
        if self.player == "O":
            img = pygame.image.load("assets/cricl.png")
        elif self.player == "X":
            img = pygame.image.load("assets/X.png")
        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
        screen.blit(
            img,
            (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
        )
    # Instruksi dan pesan status permainan

    def message(self):
        if self.winner is not None:
            screen.fill(self.game_over_bg_color, (130, 445, 193, 35))
            msg = self.font.render(
                f"{self.winner} WON!!!", True, self.game_over_color
            )
        elif not self.taking_move:
            screen.fill(self.game_over_bg_color, (130, 445, 193, 35))
            instructions = self.font.render(
                "It's a TIE!!", True, self.game_over_color)
            screen.blit(instructions, (165, 445))
        else:
            screen.fill(self.background_color, (135, 445, 188, 35))
            instructions = self.font.render(
                f"{self.player} to move", True, self.instructions_color
            )
            screen.blit(instructions, (135, 445))

    def game_check(self):
        # vertical check
        for x_index, col in enumerate(self.table):
            win = True
            pattern_list = []
            for y_index, content in enumerate(col):
                if content != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((x_index, y_index))
            if win == True:
                self.pattern_strike(pattern_list[0], pattern_list[-1], "ver")
                self.winner = self.player
                self.taking_move = False
                break
        # horizontal check
        for row in range(len(self.table)):
            win = True
            pattern_list = []
            for col in range(len(self.table)):
                if self.table[col][row] != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((col, row))
            if win == True:
                self.pattern_strike(pattern_list[0], pattern_list[-1], "hor")
                self.winner = self.player
                self.taking_move = False
                break
        # Diagonal left check
        for index, row in enumerate(self.table):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self.pattern_strike((0, 0), (2, 2), "left-diag")
            self.winner = self.player
            self.taking_move = False

        # Diagonal right check
        for index, row in enumerate(self.table[::-1]):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self.pattern_strike((2, 0), (0, 2), "right-diag")
            self.winner = self.player
            self.taking_move = False

        # Blank table cells check to draw
        blank_cells = 0
        for row in self.table:
            for cell in row:
                if cell == "-":
                    blank_cells += 1
        if blank_cells == 0:
            self.taking_move = False
    # membuat garis ke pola kemenangan

    def pattern_strike(self, start_point, end_point, line_type):
        # gets the middle value of the cell
        mid_val = self.cell_size // 2

        # garis untuk pola kemenangan vertikal
        if line_type == "ver":
            start_x, start_y = (
                start_point[0] * self.cell_size + mid_val,
                self.table_space,
            )
            end_x, end_y = (
                end_point[0] * self.cell_size + mid_val,
                self.table_size - self.table_space,
            )
        # garis untuk pola kemenangan horizontal
        elif line_type == "hor":
            start_x, start_y = (
                self.table_space,
                start_point[-1] * self.cell_size + mid_val,
            )
            end_x, end_y = (
                self.table_size - self.table_space,
                end_point[-1] * self.cell_size + mid_val,
            )
        # garis untuk pola kemenangan diagonal
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = (
                self.table_size - self.table_space,
                self.table_size - self.table_space,
            )
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        # Variable untuk menggambar garisnya
        line_strike = pygame.draw.line(
            screen, self.line_color, [start_x, start_y], [end_x, end_y], 8
        )

    # membuat fungsi main
    def main(self):
        screen.fill(self.background_color)
        self.draw_table()
        while self.running:
            self.message()
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.taking_move:
                        self.move(self.event.pos)
            pygame.display.flip()
            self.FPS.tick(60)


# untuk implementasi dari sebuah permainan TicTacToe
if __name__ == "__main__":
    g = TicTacToe(window_size[0])
    g.main()
