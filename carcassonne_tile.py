""" File: carcassonne_tile.py
    Author: Amelia Matheson
    Purpose: This file contains a class called CarcassonneTile which can be
        used to build a tile for the Carcassonne board game. The class supports
        many methods which makes a variety of useful information about the tile
        accessible to the player. It also includes the 16 tiles of the game.
    Course: CSc 120, Section 1
"""


N = 0
E = 1
S = 2
W = 3


class CarcassonneTile:
    """
    This class creates an object representing a Carcassonne tile. The
    constructor takes five parameters: 4 providing data on the tile's 4 sides,
    and a fifth providing information about the middle. A dictionary stores
    this information. There is also a second dictionary for a rotated tile.
    Methods:
        get_edge()
        edge_has_road()
        edge_has_city()
        has_crossroads()
        road_get_connection()
        city_connects()
        rotate()
    """
    def __init__(self, n_side, e_side, s_side, w_side, middle):
        self._edge_info = dict()
        self._edge_info[N] = n_side  # directional side maps to provided info
        self._edge_info[E] = e_side
        self._edge_info[S] = s_side
        self._edge_info[W] = w_side

        self._middle = middle

        self._rotated_info = dict()
        self._rotated = None

    def get_edge(self, edge):
        """
        This method returns the details of the tile's edge to the player.
        :param edge: an integer representing a directional side of the tile
        :return: a string stating the details of the tile's side
        """
        return self._edge_info[edge]

    def get_middle(self):
        return self._middle

    def edge_has_road(self, edge):
        """
        This method tells the player whether an edge has a road or not
        :param edge: an integer representing a directional side of the tile
        :return: a Boolean value. True if has road, False if doesn't have road
        """
        if 'road' in self._edge_info[edge]:
            return True
        return False

    def edge_has_city(self, edge):
        """
        This method tells the player whether an edge has a city or not
        :param edge: an integer representing a directional side of the tile
        :return: a Boolean value. True if has city, False if doesn't have city
        """
        if self._edge_info[edge] == 'city':
            return True
        return False

    def has_crossroads(self):
        """
        This method tells the player whether the tile has crossroads or not.
        Tiles with roads leading to a city in the middle have crossroads.
        :return: a Boolean value. True if has crossroads, False if doesn't have
            crossroads
        """
        if self._middle == 'city+road':
            return True
        return False

    def road_get_connection(self, from_edge):
        """
        This method tells the player which edges are connected by a road. If
        the tile has crossroads, the method returns -1 (the middle)
        :param from_edge: an integer representing a tile edge that has a road
        :return: an integer representing the side the road leads to.
        """
        if self._middle == 'city+road':
            return -1
        for side, info in self._edge_info.items():
            if side != from_edge:
                if 'road' in info:
                    return side

    def city_connects(self, sideA, sideB):
        """
        This method tells player if two tile edges share the same city.
        :param sideA: an integer representing a directional side of the tile
        :param sideB: an integer representing a directional side of the tile
        :return: a Boolean value. True of they share a city, False otherwise
        """
        if sideA == sideB:
            return True
        if self._edge_info[sideB] == 'city' and self._middle == 'city':
            return True
        return False

    def rotate(self):
        """
        This method creates a new tile with the original sides rotated 90
        degrees clockwise.
        :return: a new Carcassonne tile object
        """
        # Calculate rotated values
        self._rotated_info[N] = self._edge_info[W]
        self._rotated_info[E] = self._edge_info[N]
        self._rotated_info[S] = self._edge_info[E]
        self._rotated_info[W] = self._edge_info[S]

        new_north = self._rotated_info[N]
        new_east = self._rotated_info[E]
        new_south = self._rotated_info[S]
        new_west = self._rotated_info[W]
        middle = self._middle

        self._rotated = CarcassonneTile(new_north, new_east, new_south,
                                        new_west, middle)  # create new tile
        return self._rotated


# The 16 tiles for the Carcassonne game
tile01 = CarcassonneTile('city', 'grass+road', 'grass', 'grass+road', 'road')
tile02 = CarcassonneTile('city', 'city', 'grass', 'city', 'city')
tile03 = CarcassonneTile('grass+road', 'grass+road', 'grass+road',
                         'grass+road', 'city+road')
tile04 = CarcassonneTile('city', 'grass+road', 'grass+road', 'grass', 'road')
tile05 = CarcassonneTile('city', 'city', 'city', 'city', 'city')
tile06 = CarcassonneTile('grass+road', 'grass', 'grass+road', 'grass', 'road')
tile07 = CarcassonneTile('grass', 'city', 'grass', 'city', 'grass')
tile08 = CarcassonneTile('grass', 'city', 'grass', 'city', 'city')
tile09 = CarcassonneTile('city', 'city', 'grass', 'grass', 'city')
tile10 = CarcassonneTile('grass', 'grass+road', 'grass+road', 'grass+road',
                         'city+road')
tile11 = CarcassonneTile('city', 'grass+road', 'grass+road', 'city', 'city')
tile12 = CarcassonneTile('city', 'grass', 'grass+road', 'grass+road', 'road')
tile13 = CarcassonneTile('city', 'grass+road', 'grass+road', 'grass+road',
                         'city+road')
tile14 = CarcassonneTile('city', 'city', 'grass', 'grass', 'grass')
tile15 = CarcassonneTile('grass', 'grass', 'grass+road', 'grass+road', 'road')
tile16 = CarcassonneTile('city', 'grass', 'grass', 'grass', 'grass')
