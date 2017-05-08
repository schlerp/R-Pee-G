from random import randint

import item

from world import Location

class Body(object):
    '''represents body slots, defence items'''
    def __init__(self, shield=item.Bare(), head=item.Bare(), chest=item.Bare(), legs=item.Bare(), boots=item.Bare()):
        self.shield = shield
        self.head = head
        self.chest = chest
        self.legs = legs
        self.boots = boots
    def get_defence(self, defending=False):
        defence = self.chest.defence
        defence += self.head.defence
        defence += self.legs.defence
        if defending:
            defence += self.shield.defence
        return defence

class Character(object):
    def __init__(self, name, hp=10):
        self.name = name
        self.hp = hp
        self.weapon = item.Fists()
        self.body = Body()
        self.defending = False
        self.gold = item.Gold(quantity=0)
        self.inventory = []

    def __repr__(self):
        return '{} [{}] ({})'.format(self.name, self.weapon, self.hp)

    def is_alive(self):
        return self.hp > 0

    def get_defence(self, defending=False):
        return self.body.get_defence(defending)
    
    def get_offence(self):
        return self.weapon.damage
    
    def add_item(self, _item):
        '''adds gold to player gold, adds an item to inventory, merges consumables'''
        if isinstance(_item, item.Gold):
            self.gold.quantity += _item.quantity
            return True
        if isinstance(_item, item.Consumable):
            for index, test_item in enumerate(self.inventory):
                if isinstance(test_item, item.Consumable):
                    if test_item.name == _item.name:
                        self.inventory[index].quantity += _item.quantity
                        return True
        # else add as a unique item
        self.inventory.append(_item)
        return True

class Hero(Character):
    '''base class for heros'''
    def __init__(self, name, hp=10, lvl=0):
        super().__init__(name, hp)
        self.lvl = lvl
        self.location = Location(0,0)

class Enemy(Character):
    '''base class for all enemies'''
    def __init__(self, name, hp=10, loot=[]):
        super().__init__(name, hp)
        self.loot = loot

class Orc(Enemy):
    '''An orc, occasional leather armour and dagger'''
    def __init__(self, name='Orc frik', hp=50, loot=[]):
        super().__init__(name, hp, loot)
        self._randomise()

    def _randomise(self):
        # helmet
        if randint(0,99) < 10:
            self.body.head = item.LeatherHelmet()
        # chest
        if randint(0,99) < 10:
            self.body.chest = item.LeatherChest()     
        # legs
        if randint(0,99) < 10:
            self.body.legs = item.LeatherLegs()         
        # boots
        if randint(0,99) < 10:
            self.body.boots = item.LeatherBoots()
        # weapon
        if randint(0,99) < 10:
            self.weapon = item.Dagger()

class SimpleBoss(Enemy):
    '''a big dog boss cunt with armour n weps for dayz'''
    def __init__(self, name='Big boss', hp=200, loot=[]):
        super().__init__(name, hp, loot)
        self._randomise()

    def _randomise(self):
        # helmet
        if randint(0,99) < 50:
            self.body.head = item.LeatherHelmet()
        # chest
        if randint(0,99) < 50:
            self.body.chest = item.LeatherChest()     
        # legs
        if randint(0,99) < 50:
            self.body.legs = item.LeatherLegs()         
        # boots
        if randint(0,99) < 50:
            self.body.boots = item.LeatherBoots()
        # weapon
        weapon_chance = randint(0,99)
        if weapon_chance < 10:
            self.weapon = item.Dagger()
        elif weapon_chance < 30:
            self.weapon = item.SmallSword()
        elif weapon_chance < 80:
            self.weapon = item.LongSword()
        else:
            self.weapon = item.BastardSword()

# exceptions
class DeadException(Exception):
    pass

class WinException(Exception):
    pass

class WinBossException(Exception):
    pass

class EscapeException(Exception):
    pass
