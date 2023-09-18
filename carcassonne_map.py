""" File: carcassonne.map_py
    Author: Amelia Matheson
    Purpose: This file contains a class for a Carcassonne Map in which tiles
        can be placed to form a Carcassonne game. The class supports many
        methods that aid in playing the game. More information below.
        The class CarcassonneTile is imported from carcassonne_tile.py
        Global variables N, E, W, and S represent directions on the map and/or
        edges of a tile. C represents the center of a tile.
    Course: CSc 120, Section 1
"""

import carcassonne_tile

N = 0
E = 1
S = 2
W = 3
C = -1
POINTS = [(N, S), (E, W), (S, N), (W, E)]  # grouping opposite sides together


class CarcassonneMap:
    """
    This class creates an object representing a Carcassonne map game board. The
    constructor takes no parameters, but there are two fields: a dictionary
    containing the coordinates of tiles on the map; tile01 is already included.
    The second field is a set containing coordinates of border spaces that new
    tiles can be added. Methods include:
        get_all_coords()
        find_map_border()
        get()
        add()
        check_add_tile() - private method
        find_poss_neighbors() - private method
    """

    def __init__(self):
        self._map_dict = dict()
        self._map_dict[(0, 0)] = carcassonne_tile.tile01
        self._border_states = {(-1, 0), (1, 0), (0, -1), (0, 1)}
        self._tile_neighbors = {(0, 0): [(0, 1), (1, 0), (0, -1), (-1, 0)]}
        self._loopDups = []

    def get_all_coords(self):
        """
        This method creates a set of all tile coordinates that exist on the
        map.
        :return: a set of all tile coordinates
        """
        coords = set()
        for place in self._map_dict:
            coords.add(place)
        return coords

    def _find_poss_neighbors(self):
        """
        This method populates a dictionary that maps tiles to their individual
        border states. While self._border_states is a set of all border states,
        self._tile_neighbors organizes these states by tile and this dictionary
        does not remove borders that are eventually filled.
        The method also acts as a helper method for find_border_map.
        :return: a dictionary that maps tile coordinates to an array of border
            tuples
        """
        for coor in self._map_dict:
            x = coor[0]
            y = coor[1]

            # find the adjacent spaces, open or not
            poss_east = (x + 1, y)
            poss_west = (x - 1, y)
            poss_north = (x, y + 1)
            poss_south = (x, y - 1)

            # map them to the specific tile. Overlap is possible and expected
            self._tile_neighbors[coor] = [poss_north, poss_east, poss_south,
                                          poss_west]
        return self._tile_neighbors

    def find_map_border(self):
        """
        This method creates a set containing coordinates of open and valid
        places to add new tiles using the four spaces adjacent to each tile on
        the map. The set is updated as the map dictionary is
        updated as long as the method is called.
        :return: a set containing open spaces where new tiles can be added
        """
        self._find_poss_neighbors()
        for coor in self._map_dict:  # for each tile on the map
            if coor in self._border_states:
                # remove tile if it has just been added to map
                self._border_states.remove(coor)

        for tile, neighbors in self._tile_neighbors.items():
            for position in neighbors:  # position: coordinate of adjacent spot
                if position not in self._map_dict:  # if there is no tile there
                    self._border_states.add(position)

        return self._border_states

    def get(self, x, y):
        """
        This method informs the user of the state of a position on the map;
        whether there is a tile there or not. If no tile exists at that
        position, method returns None. Otherwise, method returns the tile that
        exists there.
        :param x: an integer representing x-coordinate on map
        :param y: an integer representing y-coordinate on map
        :return: None or a Carcassonne Tile
        """
        if (x, y) not in self._map_dict:
            return None
        return self._map_dict[(x, y)]

    def add(self, x, y, tile, confirm=True, tryOnly=False):
        """
        This method attempts to add a new tile to the map based on
        specifications provided by the caller.
        :param x: an integer representing x-coordinate on map
        :param y: an integer representing y-coordinate on map
        :param tile: a Carcassonne Tile object to be added to the map
        :param confirm: a Boolean value specifying whether tile should be added
        :param tryOnly: a Boolean value specifying whether method should only
            attempt to add the tile
        :return: a Boolean value indicating whether tile can and/or was added
            to map
        """
        self.find_map_border()
        if confirm:
            # tile must match up with edges of existing tiles around it
            if self._check_add_tile(x, y, tile):
                if tryOnly:
                    return True
                self._map_dict[(x, y)] = tile  # add tile to the map
                return True
            return False
        # if both confirm and tryOnly are False, tile is added without checks
        self._map_dict[(x, y)] = tile
        return True

    def _check_add_tile(self, x, y, tile):
        """
        This method is a helper method for add(). It checks the edges of the
        tile to be added against existing adjacent tiles on the map.
        :param x: an integer representing x-coordinate on map
        :param y: an integer representing y-coordinate on map
        :param tile: a Carcassonne Tile to be added
        :return: a Boolean value
        """
        if (x, y) in self._map_dict:  # cannot overwrite an existing tile
            return False
        # new tiles must be placed adjacent to existing tiles
        if (x, y) not in self._border_states:
            return False

        # place - coordinate of a tile on map
        # neighbors - array of 4 tuples representing adjacent spaces
        for place, neighbors in self._tile_neighbors.items():
            if (x, y) in neighbors:
                # record where space is in relation to tile it is adjacent to
                ind = neighbors.index((x, y))  # 0:N, 1:E, 2:S, 3:W
                if self._map_dict[place].get_edge(POINTS[ind][0]) != \
                        tile.get_edge(POINTS[ind][1]):
                    return False
        return True

    def trace_road_one_direction(self, x, y, side):
        """
        This method follows a road on the map until in ends, given a starting
        point, (x, y). It builds the road's path using a while loop. It also is
        a helper function for the trace_road method.
        :param x: an integer representing the x_coordinate of a tile on the map
        :param y: an integer representing the y_coordinate of a tile on the map
        :param side: an integer representing the direction the road should be
            traced first.
        :return: an array of tuples representing the path of the road
        """
        orginal_x, orginal_y = x, y
        increment_coors = {E: [(1, 0), W], W: [(-1, 0), E], N: [(0, 1), S],
                           S: [(0, -1), N]}
        retval = []
        while True:
            if side == C or (x, y) not in self._map_dict:  # the road has ended
                break

            next_x = x + increment_coors[side][0][0]  # x_coord of next tile
            next_y = y + increment_coors[side][0][1]  # y coord of next tile
            enter = increment_coors[side][1]  # side that enter next tile from

            exit_side = -1  # will change this if need to
            if (next_x, next_y) in self._map_dict:
                exit_side = self._map_dict[
                    (next_x, next_y)].road_get_connection(
                    enter)  # side that exit next tile from
                traveled = (next_x, next_y, enter, exit_side)
                retval += [traveled]
            x, y, side = next_x, next_y, exit_side  # update coords and side

            # if the road goes in around in a loop, stop documenting the path
            if next_x == orginal_x and next_y == orginal_y:
                break
        return retval

    def trace_road(self, x, y, side):
        """
        This method follows a road in both directions given a starting point.
        :param x: an integer representing the x_coordinate of a tile on the map
        :param y: an integer representing the y_coordinate of a tile on the map
        :param side: an integer representing the direction the road should be
            traced first.
        :return: an array of tuples representing the path of the road
        """
        # Get connection of the road in current, given tile
        conn = self._map_dict[(x, y)].road_get_connection(side)
        # the road will eventually goes through given tile, so need that path
        tile_pass = (x, y, conn, side)

        backwards = self.trace_road_one_direction(x, y, conn)
        backwards.reverse()

        new_backwards = []
        for step in backwards:
            step = list(step)
            # rearrange enter-exit relation
            step[2], step[3] = step[3], step[2]
            step = tuple(step)
            new_backwards.append(step)

        if tile_pass in new_backwards:
            new_backwards.pop(0)
            new_backwards.append(tile_pass)
            return new_backwards

        full_path = new_backwards + [tile_pass] + \
                    self.trace_road_one_direction(x, y, side)
        return full_path


    """
    trace_city() is a method that traces a city across multiple tiles on the 
    map. There are two ways the city can be expanded: 1) a city on a tile's 
    edge connects to another edge (city_connects return True) and 2) tiles that
    share borders have cities on connecting edges. The method also tells the 
    caller if the city is complete (totally enclosed by grass or roads). 
    :param x: an integer representing the x_coordinate of a tile on the map
    :param y: an integer representing the y_coordinate of a tile on the map
    :param side: an integer representing the direction the city should be
            traced first.
    """

    def trace_city(self, x, y, side):
        self._find_poss_neighbors()
        edges = [N, E, S, W]
        city = {(x, y, side)}
        complete = True

        finding_new_pieces = True  # if finding new city pieces, loop will run
        while finding_new_pieces:
            finding_new_pieces = False  # will change later if need to
            dup_city = list(city)
            for land in dup_city:
                x_coord, y_coord, side = land[0], land[1], land[2]
                for edge in edges:
                    if edge != side:
                        if self._map_dict[(x_coord, y_coord)].city_connects(
                                side, edge):  # if city stretches across tile
                            new_piece_1 = (x_coord, y_coord, edge)
                            if new_piece_1 not in city:
                                city.add(new_piece_1)
                                finding_new_pieces = True

                neighbor = self._obtain_neighbor(x_coord, y_coord, side)
                if neighbor in self._map_dict:
                    opposite_side = POINTS[side][1]  # side enter neighbor from
                    new_piece_2 = (neighbor[0], neighbor[1], opposite_side)
                    if new_piece_2 not in city:
                        city.add(new_piece_2)
                        finding_new_pieces = True
                else:
                    complete = False
        return (complete, city)

    def _obtain_neighbor(self, x, y, side):
        """
       This method finds a desired neighbor for a provided tile at (x, y) on
       the map given the side that the caller is leaving the tile. It returns
       the coordinates of the adjacent tile in that direction.
       :param x: an integer representing the x_coordinate of a tile on the map
       :param y: an integer representing the y_coordinate of a tile on the map
       :param side: an integer representing the direction we are leaving the
            tile; the direction the resulting adjacent tile should be located
            in relation to the provided tile
       :return:
       """
        target = (x, y)
        neighbor = self._tile_neighbors[target][side]
        return neighbor
