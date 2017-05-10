from random import randint

import characters
import world
import items


def pick_rand_room(width, height, blacklist=[]):
    '''selects a random room from the map'''
    while True:
        x = randint(0, width-1)
        y = randint(0, height-1)
        choice = world.world.Location(x,y)
        if choice not in blacklist:
            break
    return choice

def init_rooms(width, height, loot=10, enemies=10, vendors=2, boss=1):
    '''creates a set of random rooms'''
    rooms = []
    # initialise empty rooms
    for i in range(height):
        row = []
        for j in range(width):
            row.append(world.world.Room(j, i, 'empty room ({},{})'.format(j, i), 'An empty room, there is nothing of use here.'))
        rooms.append(row)
    replaced_rooms = []
    
    # insert loot rooms
    for i in range(enemies):
        current_room = pick_rand_room(width, height, blacklist=replaced_rooms)
        replaced_rooms.append(current_room)
        loot_amount = randint(1, 50)
        loot = items.consumables.Gold(quantity=loot_amount)
        rooms[current_room.x][current_room.y] = world.world.Room(x=current_room.x, 
                                                                 y=current_room.y,
                                                                 name='loot room ({},{})'.format(current_room.x, current_room.y),
                                                                 description='A room with something abandoned on the floor',
                                                                 loot=[loot])

    # insert enemy rooms
    for i in range(enemies):
        current_room = pick_rand_room(width, height, blacklist=replaced_rooms)
        replaced_rooms.append(current_room)
        enemy_type = randint(0,99)
        if enemy_type < 75:
            enemy = characters.Orc()
        else:
            enemy = characters.Golem()
        rooms[current_room.x][current_room.y] = world.world.Room(x=current_room.x, 
                                                                 y=current_room.y,
                                                                 name='enemy room ({},{})'.format(current_room.x, current_room.y),
                                                                 description='A room with an enemy lurking!',
                                                                 enemies=[enemy])
    
    # insert boss room
    current_room = pick_rand_room(width, height, blacklist=replaced_rooms)
    replaced_rooms.append(current_room)
    boss = characters.SimpleBoss()
    rooms[current_room.x][current_room.y] = world.world.Room(x=current_room.x, 
                                                             y=current_room.y,
                                                             name='Boss room ({},{})'.format(current_room.x, current_room.y),
                                                             description='The boss awaits your challenge!',
                                                             enemies=[boss], 
                                                             boss=True)    
    return rooms

class Map(object):
    '''a collection of rooms arranged as a list of lists'''
    def __init__(self, width=5, height=5, loot=10, enemies=10, boss=1):
        self._random_map(width, height, loot, enemies, boss)
    def _random_map(self, width, height, loot, enemies, boss):
        '''creates a random map'''
        self.rooms = init_rooms(width, height, loot, enemies, boss)
    def get_room(self, location):
        return self.rooms[location.x][location.y]
            

def move(_map, player, direction):
    max_x = len(_map.rooms[0]) - 1 # length of first row (width)
    max_y = len(_map.rooms) - 1    # how many rows (height)
    if direction == None:
        raise DirectionException
    if direction == 'north':
        new_y = player.location.y - 1
        if new_y < 0 or new_y > max_y:
            raise OffMapException
        else:
            player.location.y += -1
    elif direction == 'south':
        new_y = player.location.y + 1
        if new_y < 0 or new_y > max_y:
            raise OffMapException
        else:
            player.location.y += 1
    elif direction == 'west':
        new_x = player.location.x - 1
        if new_x < 0 or new_x > max_x:
            raise OffMapException
        else:
            player.location.x += -1
    elif direction == 'east':
        new_x = player.location.x + 1
        if new_x < 0 or new_x > max_x:
            raise OffMapException
        else:
            player.location.x += 1


def handle_move(_map, player):
    while True:
        print("Please choose a direction to continue...")
        world.world.print_directions()
        choice = input('>>> ')
        try:
            direction = world.world.Direction().get(choice)
            move(_map, player, direction)
            break
        except DirectionException:
            print('I dont know which direction {} is in!'.format(choice))
        except OffMapException:
            print('{} passage is blocked'.format(direction))
    return direction

class DirectionException(Exception):
    '''represents an unknown direction'''

class OffMapException(Exception):
    '''raised when player attempts to move off map'''
