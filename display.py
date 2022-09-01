import pygame

pygame.init()

WIDTH = 1500
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Visualizer")
HeadFont = pygame.font.Font("freesansbold.ttf", 30)
ButtonsFont = pygame.font.SysFont("cambriacambriamath", 30)
gui_font = pygame.font.Font(None, 30)
text_heading = HeadFont.render('Path Finding Visualizer', True, (255, 255, 255))
text_reset = ButtonsFont.render('Reset', True, (255, 255, 255))
text_visualize = ButtonsFont.render('Visualize', True, (255, 255, 255))
text_astar = ButtonsFont.render('A-Star', True, (255, 255, 255))
text_dijkstra = ButtonsFont.render('Dijkstra', True, (255, 255, 255))
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
DARK_GREY = (34, 41, 48)


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
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def drawBarrier(self, win):
        pygame.draw.rect(
            win, DARK_GREY, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
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


buttons = []


class Button:
    def __init__(self, text_heading, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text_heading
        self.text_heading = text_heading
        self.text_surf = gui_font.render(text_heading, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        buttons.append(self)

    def change_text(self, newtext):
        self.text_surf = gui_font.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(
            WIN, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(
            WIN, self.top_color, self.top_rect, border_radius=12)
        WIN.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.text_heading}")
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.change_text(self.text_heading)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'


def reconstruct_path(came_from, current, draw):
    current.make_end()
    current = came_from[current]
    current.make_path()
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


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


def buttons_draw():
    for b in buttons:
        b.draw()

    


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

    WIN.blit(text_heading, (570, 10))
    buttons_draw()
    draw_grid(win, rows, width)
    pygame.display.update()



def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


button1 = Button('Reset', 85, 35, (1235, 38), 3)
button2 = Button('Visualize', 125, 35, (1345, 38), 3)
button3 = Button('A star', 85, 35, (35, 38), 3)
button4 = Button('Dijkstra', 115, 35, (145, 38), 3)
