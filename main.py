import pygame
import display
import algorithms

def main(win, width):
    ROWS = 50
    grid = display.make_grid(ROWS, width)
    start = None
    end = None
    run = True
    flag_aStar = False
    flag_dijsktra = False
    while run:
        display.draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = display.get_clicked_pos(pos, ROWS, width)
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
                row, col = display.get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if display.rect3.collidepoint(mouse):
                    flag_aStar = True
                elif display.rect4.collidepoint(mouse):
                    flag_dijsktra = True
                elif display.rect2.collidepoint(mouse) and flag_aStar:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithms.Astar(lambda: display.draw(win, grid, ROWS, width), grid, start, end)
                    flag_aStar = False
                elif display.rect2.collidepoint(mouse) and flag_dijsktra:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithms.Dijkstra(lambda: display.draw(win, grid, ROWS, width), grid, start, end)
                    flag_dijsktra = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if display.rect1.collidepoint(mouse):
                    start = None
                    end = None
                    grid = display.make_grid(ROWS, width)


main(display.WIN, display.WIDTH)
