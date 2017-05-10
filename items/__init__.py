from random import randint

import tools


class ConsumableExpiredException(Exception):
    '''attempted to use expired consumable'''
    pass


def use_item(player, ai=None):
    try:
        choice = tools.interface.choose_from_list(player.inventory)
        item = player.inventory[int(choice)]
        item.use(player, ai)
    except ConsumableExpiredException as e:
        if item.removable:
            _ = player.inventory.pop(choice)
            del _
        print('you are out of {} (quantity={})'.format(item.name, item.quantity))
    except ValueError as e:
        print('Unknow option: {}'.format(choice))


class Item(object):
    '''base class for all items'''
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name


def apply_defence(attack, defence):
    damage = attack - defence
    if damage < 0:
        damage = 0
    return damage

class Damage(object):
    '''represents the different types of damage'''
    def __init__(self, physical=0, physical_min=0, magic=0, fire=0, ice=0, poison=0):
        self.physical = physical
        self.physical_min = physical_min
        self.magic = magic
        self.fire = fire
        self.ice = ice
        self.poison = poison

    def hit(self):
        damage = randint(self.physical_min, self.physical)
        damage += self.magic
        damage += self.fire
        damage += self.ice
        damage += self.poison
        return damage

    def __add__(self, other):
        if isinstance(other, Damage):
            return self._add(other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Damage):
            return self._subtract(other)
        return NotImplemented

    def _add(self, other):
        '''adds damage classes together'''
        # physical damage
        physical_min = self.physical_min + other.physical_min
        physical = self.physical + other.physical
        # magic damage
        magic = self.magic + other.magic
        # fire damage
        fire = self.fire + other.fire
        # ice damage
        ice = self.ice + other.ice
        # poison damage
        poison = self.poison + other.poison
        if isinstance(other, Defence):
            return Defence(physical, physical_min, magic, fire, ice, poison)
        return Damage(physical, physical_min, magic, fire, ice, poison)

    def _subtract(self, other):
        '''subtracts damage (applies defense, elemental as percentage)'''
        if isinstance(other, Defence):
            # physical damage
            physical_min = max(0, self.physical_min - other.physical_min)
            physical = max(0, self.physical - other.physical)
            
            # for elemental apply as percentage!
            # magic damage
            magic = max(0, self.magic-int(self.magic*(other.magic/100)))
            # fire damage
            fire = max(0, self.fire-int(self.fire*(other.fire/100)))
            # ice damage
            ice = max(0, self.ice-int(self.ice*(other.ice/100)))
            # poison damage
            poison = max(0, self.poison-int(self.poison*(other.poison/100)))
            # return hp damage
            return Damage(physical, physical_min, magic, fire, ice, poison)
        
        elif isinstance(other, Damage):
            # physical damage
            physical_min = max(0, self.physical_min - other.physical_min)
            physical = max(0, self.physical - other.physical)
            # magic damage
            magic = max(0, self.magic - other.magic)
            # fire damage
            fire = max(0, self.fire - other.fire)
            # ice damage
            ice = max(0, self.ice - other.ice)
            # poison damage
            poison = max(0, self.poison - other.poison)
            # return hp damage
            return Damage(physical, physical_min, magic, fire, ice, poison)
        
        else:
            return NotImplemented
    
    def __repr__(self):
        template = '{}-{}D, {}M, {}F, {}I, {}P'
        return template.format(self.physical_min, self.physical, self.magic,
                               self.fire, self.ice, self.poison)

class Defence(Damage):
    '''same as damage, but elemental is represented as a percentage'''
    def __repr__(self):
        template = '{}-{}D, {}M%, {}F%, {}I%, {}P%'
        return template.format(self.physical_min, self.physical, self.magic,
                               self.fire, self.ice, self.poison)


class Equipment(Item):
    '''base class for equipment (equipable) items'''
    pass


# Armour
from . import armour


# Weapons
from . import weapons


# consumables
from . import consumables
