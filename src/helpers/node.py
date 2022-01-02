import pygame
from src.helpers.config import *


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
        return self.color == ORANGE

    def make_open(self):
        self.color = ORANGE
    
    def is_obstacle(self):
        return self.color == BLACK

    def make_obstacle(self):
        self.color = BLACK

    def is_start(self):
        return self.color == LIGHT_BLUE

    def make_start(self):
        self.color = LIGHT_BLUE

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
        # Note: row and col counter-intuitive (due to Pygame coordinate system)
        # left
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        # right
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        # up
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])
        # down
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])
