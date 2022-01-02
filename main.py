import pygame
from src.helpers.config import *
from src.astar import AStar
from src.bfs import BFS
from src.dfs import DFS
from src.helpers.node import Node
from src.helpers.helpers import *


def make_grid():
    """
    Create grid full of nodes
    :return <array> 2-D array representing the grid of nodes
    """
    grid = []

    for row in range(GRID_SIZE):
        grid.append([])
        for col in range(GRID_SIZE):
            node = Node(row, col)
            grid[row].append(node)
    
    return grid

def get_clicked_pos(pos):
    """
    Get location of node that was clicked
    :param pos: <array> Position consisting of x and y coordinates as pixels
    :return <array> Postion representing row, column of node
    """
    # Note: row and col counter-intuitive (due to Pygame coordinate system)
    y, x = pos
    row = y // NODE_SIZE
    col = x // NODE_SIZE
    return row, col

def get_pathfinder():
    """
    Get user choice of pathfinding algorithm
    :return: <Pathfinder> Pathfinding algorithm
    """
    valid_input = False
    while not valid_input:
        pathfinder_str = input("Which pathfinding algorithm would you like to use?\n"
                                "(1) A*\n"
                                "(2) Breadth-first\n"
                                "(3) Depth-first\n"
                                "\n"
                                )
        match pathfinder_str:
            case "1":
                pygame.display.set_caption("A* Pathfinder")
                return AStar()
            case "2":
                pygame.display.set_caption("Breadth-first Search")
                return BFS()
            case "3":
                pygame.display.set_caption("Depth-first Search")
                return DFS()
            case _:
                print("Please enter a valid choice (1 - 3)!\n")

def main():
    """
    Run Pygame window until user quits
    :return None
    """
    pathfinder = get_pathfinder()

    grid = make_grid()
    start = None
    end = None
    run = True

    while run:
        draw(grid)
        for event in pygame.event.get():
            # user quit - click red exit button
            if event.type == pygame.QUIT:
                run = False
            # place node - left mouse button
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_obstacle()
            # erase node - right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            # keyboard key
            elif event.type == pygame.KEYDOWN:
                # user quite - escape
                if event.key == pygame.K_ESCAPE:
                    run = False
                # find path - space/enter/return
                if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    pathfinder.path_algorithm(grid, start, end)
                # clear grid - c/delete/backspace
                if event.key == pygame.K_c or event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = make_grid()
    pygame.quit()


# Run Pygame
if __name__ == '__main__':
    main()