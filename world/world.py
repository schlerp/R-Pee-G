import sys


class Direction():
    up = ('n', 'north', 'u', 'up')
    down = ('s', 'south', 'u', 'up')
    left = ('w', 'west', 'l', 'left')
    right = ('e', 'east', 'r', 'right')

    def get(self, direction):
        if direction in self.up:
            return 'north'
        if direction in self.down:
            return 'south'
        if direction in self.left:
            return 'west'
        if direction in self.right:
            return 'east'
        # no match found, return None
        return None


def print_directions():
    print(Direction.up)
    print(Direction.right)
    print(Direction.down)
    print(Direction.left)

class Location(object):
    '''this is a location, basic x and y points'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        if self.x == other.x:
            if self.y == other.y:
                return True
        return False

    def __ne__(self, other):
        equal = self.__eq__(other)
        if ret == NotImplemented:
            return NotImplemented
        return not equal

class Room(Location):
    '''the base class for all rooms'''
    def __init__(self, x, y, name, description, loot=[], enemies=[], boss=False):
        super().__init__(x, y)
        self.name = name
        self.description = description
        self.loot = loot
        self.enemies = enemies
        self.boss = boss
    def __repr__(self):
        return self.name     
