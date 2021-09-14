import sys
import pygame
from math import ceil
from queue import PriorityQueue

pygame.init()

WIDTH = 1500
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Visualizer")
HeadFont = pygame.font.Font("freesansbold.ttf", 30)
ButtonsFont = pygame.font.SysFont("cambriacambriamath", 30)
text = HeadFont.render('Path Finding Visualizer', True, (255, 255, 255))
text1 = ButtonsFont.render('Reset', True, (255, 255, 255))
text2 = ButtonsFont.render('Visualize', True, (255, 255, 255))
text3 = ButtonsFont.render('A-Star', True, (255, 255, 255))
text4 = ButtonsFont.render('Dijsktra', True, (255, 255, 255))
rect1 = pygame.Rect(1250, 45, 80, 25)
rect2 = pygame.Rect(1350, 45, 120, 25)
rect3 = pygame.Rect(30, 50, 80, 25)
rect4 = pygame.Rect(120, 50, 120, 25)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
COLOR_INACTIVE = (47, 79, 79)
COLOR_ACTIVE = (255, 100, 100)
COLOR_LIST_INACTIVE = (47, 79, 79)
COLOR_LIST_ACTIVE = (255, 100, 100)
DARK_GREY = pygame.Color("#2F4F4F")


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def drawBarrier(self, win):
        pygame.draw.rect(win, DARK_GREY, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        # ADD DIAGONALS

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][
            self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col + 1])

        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col - 1])

    def __lt__(self, other):
        return False


def heuristics(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    D = 1
    D2 = 1.41421356237
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    h = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    return h


def reconstruct_path(came_from, current, draw):
    current.make_end()
    current = came_from[current]
    current.make_path()
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def Dijsktra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def Astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristics(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristics(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(3, rows + 3):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 90), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        count = 0
        for spot in row:
            if count < 3:
                spot.drawBarrier(win)
            elif 2 < count < 48:
                spot.draw(win)
            else:
                spot.drawBarrier(win)
            count += 1
    WIN.blit(text, (570, 10))
    pygame.draw.rect(WIN, DARK_GREY, rect1)
    WIN.blit(text1, (1250, 40))
    pygame.draw.rect(WIN, DARK_GREY, rect2)
    WIN.blit(text2, (1350, 40))
    pygame.draw.rect(WIN, DARK_GREY, rect3)
    WIN.blit(text3, (30, 45))
    pygame.draw.rect(WIN, DARK_GREY, rect4)
    WIN.blit(text4, (120, 45))
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    flag_aStar = False
    flag_dijsktra = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if rect3.collidepoint(mouse):
                    flag_aStar = True
                elif rect4.collidepoint(mouse):
                    flag_dijsktra = True
                elif rect2.collidepoint(mouse) and flag_aStar:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    Astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    flag_aStar = False
                elif rect2.collidepoint(mouse) and flag_dijsktra:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    Dijsktra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    flag_dijsktra = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if rect1.collidepoint(mouse):
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


main(WIN, WIDTH)
