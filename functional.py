import pygame
import math
from queue import PriorityQueue
from config import *
from node import Node

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("A* Pathfinder")

class Node:
    """
    Represents a square on the grid
    :attr row: <int> row of grid where located
    :attr col: <int> column of grid where located
    :attr x: <int> x coordinate in pixels where (top left corner) located
    :attr y: <int> y coordinate in pixels where (top left corner) located
    :attr color: <tuple> RGB color
    :attr neighbors: <list> List of a neighboring nodes (up, down, left, right)
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * NODE_SIZE
        self.y = col * NODE_SIZE
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        """
        Get position of Node
        Note: Nodes indexed using (row, col)
        """
        return self.row, self.col

    # Getters and Setters
    def is_closed(self):
        return self.color == PINK

    def make_closed(self):
        self.color = PINK

    def is_open(self):
        return self.color == LIGHT_BLUE

    def make_open(self):
        self.color = LIGHT_BLUE
    
    def is_obstacle(self):
        return self.color == BLACK

    def make_obstacle(self):
        self.color = BLACK

    def is_start(self):
        return self.color == PURPLE

    def make_start(self):
        self.color = PURPLE

    def is_end(self):
        return self.color == RED

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = GREEN

    def reset(self):
        self.color = WHITE

    def draw(self):
        """
        Draw node onto grid
        :return: None
        """
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, NODE_SIZE, NODE_SIZE))

    def update_neighbors(self, grid):
        """
        Update the list of neighbors for each node
        :param grid: <array> 2-D array representing the grid of nodes
        :return: None
        """
        self.neighbors = []
        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        # down
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        # left
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])
        # right
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])

def heuristic_distance(p1, p2):
    """
    Calculate Manhattan distance between two points
    :param p1: <array> Point consisting of x and y coordinates
    :param p2: <array> Point consisting of x and y coordinates
    :return: Manhattan distance
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def path_algorithm(grid, start, end):
    """
    Finds the shortest path using A* algorithm
    :param grid: <array> 2-D array representing the grid of nodes
    :param start: <Node> Starting node
    :param end: <Node> Ending node
    :return: True if path found, False if not
    """
    # tiebreaker
    count = 0
    # sort open nodes for heuristically shortest path
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    # access open nodes
    open_set_hash = {start}
    # store path
    came_from = {}
    # g_score -> current shortest distance to get from start to node
    g_score = { node: float("inf") for row in grid for node in row }
    g_score[start] = 0
    # f_score -> sum of g_score and distance from end node
    f_score = { node: float("inf") for row in grid for node in row }
    f_score[start] = heuristic_distance(start.get_pos(), end.get_pos())

    while not open_set.empty():
        # user quit - click red exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # get and remove node at front of priority queue
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # shortest path found
        if current == end:
            reconstruct_path(came_from, end, grid, end)
            start.make_start()
            return True

        for neighbor in current.neighbors:
            # distance between current and neighbor always 1
            tentative_g_score = g_score[current] + 1 

            # theoretically shorter path found
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_distance(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw(grid)

        if current != start:
            current.make_closed()

    # no path found
    return False

def reconstruct_path(came_from, current, grid, end):
    """
    Draw shortest path
    :param came_from: <dict> key -> nodeA : value -> node used to reach nodeA
    :param current: <Node> Node currently being considered
    :param grid: <array> 2-D array representing the grid of nodes
    :param end: <Node> Ending node
    :return None
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        end.make_end()
        draw(grid)

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
    
def draw_grid():
    """
    Draw grid lines
    :return: None
    """
    for row in range(GRID_SIZE):
        pygame.draw.line(WINDOW, GREY, (0, row * NODE_SIZE), (WINDOW_WIDTH, row * NODE_SIZE))

    for col in range(GRID_SIZE):
        pygame.draw.line(WINDOW, GREY, (col * NODE_SIZE, 0), (col * NODE_SIZE, WINDOW_WIDTH))

def draw(grid):
    """
    Redraw all nodes in grid with updated color
    :param grid: <array> 2-D array representing the grid of nodes
    :return None
    """
    WINDOW.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw()

    draw_grid()
    pygame.display.update()

def get_clicked_pos(pos):
    """
    Get location of node that was clicked
    :param pos: <array> Position consisting of x and y coordinates as pixels
    :return <array> Postion representing row, column of node
    """
    y, x = pos
    row = y // NODE_SIZE
    col = x // NODE_SIZE
    return row, col

def main():
    """
    Run Pygame window until user quits
    :return None
    """
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
                # find path - space/enter/return
                if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path_algorithm(grid, start, end)
                # clear grid - c/delete/backspace
                if event.key == pygame.K_c or event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = make_grid()
    pygame.quit()


# Run Pygame
if __name__ == '__main__':
    main()