from random import randint

import items

import world

class Body(object):
    '''represents body slots, defence items'''
    def __init__(self, shield=items.armour.Bare(), head=items.armour.Bare(), chest=items.armour.Bare(), legs=items.armour.Bare(), boots=items.armour.Bare()):
        self.shield = shield
        self.head = head
        self.chest = chest
        self.legs = legs
        self.boots = boots

    def get_equipment(self, body_part):
        if str(body_part) == 'head':
            return self.head
        elif str(body_part) == 'chest':
            return self.chest
        elif str(body_part) == 'legs':
            return self.legs
        elif str(body_part) == 'boots':
            return self.boots
        elif str(body_part) == 'shield':
            return self.shield
        return None
    
    def set_equipment(self, body_part, _item):
        if _item.body_part == body_part:
            if str(body_part) == 'head':
                self.head == _item
            elif str(body_part) == 'chest':
                self.chest == _item
            elif str(body_part) == 'legs':
                self.legs == _item
            elif str(body_part) == 'boots':
                self.boots == _item
            elif str(body_part) == 'shield':
                self.shield == _item
            else:
                return False
            return True
        return False
    
    def replace_equipment(self, body_part, _item):
        old_item = self.get_equipment(body_part)
        self.set_equipment(body_part, _item)
        return old_item
        
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
        self.weapon = items.weapons.Fists()
        self.body = Body()
        self.defending = False
        self.gold = items.consumables.Gold(quantity=0)
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
        if isinstance(_item, items.consumables.Gold):
            self.gold.quantity += _item.quantity
            return True

        if isinstance(_item, items.consumables.Consumable):
            for index, test_item in enumerate(self.inventory):
                if isinstance(test_item, type(_item)):
                    self.inventory[index].quantity += _item.quantity
                    return True

        # if equipment only add if not there already
        if isinstance(_item, items.Equipment):
            for test_item in self.inventory:
                if isinstance(test_item, type(_item)):
                    return False

        # else add as a unique item
        self.inventory.append(_item)
        return True

class Hero(Character):
    '''base class for heros'''
    def __init__(self, name, hp=10, lvl=0):
        super().__init__(name, hp)
        self.lvl = lvl
        self.location = world.world.Location(0,0)

class Enemy(Character):
    '''base class for all enemies'''
    def __init__(self, name, hp=10, loot=None):
        super().__init__(name, hp)
        if loot == None:
            self.loot = []
        else:
            self.loot = loot


class Orc(Enemy):
    '''An orc, occasional leather armour and dagger or small sword'''
    def __init__(self, name='Orc frik', hp=50, loot=None):
        super().__init__(name, hp, loot)
        self._randomise()

    def _randomise(self):
        self.hp = randint(25, 75)
        # helmet
        if randint(0,99) < 20:
            self.body.head = items.armour.LeatherHelmet()
            self.loot.append(items.armour.LeatherHelmet())
        # chest
        if randint(0,99) < 20:
            self.body.chest = items.armour.LeatherChest()
            self.loot.append(items.armour.LeatherChest())
        # legs
        if randint(0,99) < 20:
            self.body.legs = items.armour.LeatherLegs()
            self.loot.append(items.armour.LeatherLegs())
        # boots
        if randint(0,99) < 20:
            self.body.boots = items.armour.LeatherBoots()
            self.loot.append(items.armour.LeatherBoots())
        # weapon
        weapon_roll = randint(0,99)
        if weapon_roll < 25:
            self.weapon = items.weapons.Dagger()
            self.loot.append(items.weapons.Dagger())
        elif weapon_roll < 50:
            self.weapon = items.weapons.SmallSword()
            self.loot.append(items.weapons.SmallSword())
        # random chance to drop medpacks
        if randint(0,99) < 20:
            self.loot.append(items.consumables.Medkit(randint(1,3)))        


class Golem(Enemy):
    '''A golem, occasional chainmail armour and stuff'''
    def __init__(self, name='Golem', hp=100, loot=[]):
        super().__init__(name, hp, loot)
        self._randomise()

    def _randomise(self):
        self.hp = randint(50, 150)
        # helmet
        if randint(0,99) < 20:
            self.body.head = items.armour.ChainmailHelmet()
            self.loot.append(items.armour.ChainmailHelmet())
        # chest
        if randint(0,99) < 20:
            self.body.chest = items.armour.ChainmailChest()
            self.loot.append(items.armour.ChainmailChest())
        # legs
        if randint(0,99) < 20:
            self.body.legs = items.armour.ChainmailLegs()
            self.loot.append(items.armour.ChainmailLegs())
        # boots
        if randint(0,99) < 20:
            self.body.boots = items.armour.ChainmailBoots()
            self.loot.append(items.armour.ChainmailBoots())
        # weapon
        weapon_roll = randint(0,99)
        if weapon_roll < 25:
            self.weapon = items.weapons.SmallSword()
            self.loot.append(items.weapons.SmallSword())
        elif weapon_roll < 50:
            self.weapon = items.weapons.LongSword()
            self.loot.append(items.weapons.LongSword())
        # random chance to drop medpacks
        if randint(0,99) < 50:
            self.loot.append(items.consumables.BigMedkit(randint(1,2)))
        

class SimpleBoss(Enemy):
    '''a big dog boss cunt with armour n weps for dayz'''
    def __init__(self, name='Big boss', hp=200, loot=[]):
        super().__init__(name, hp, loot)
        self._randomise()

    def _randomise(self):
        self.hp = randint(150, 250)
        # helmet
        if randint(0,99) < 50:
            self.body.head = items.armour.PlateHelmet()
        # chest
        if randint(0,99) < 50:
            self.body.chest = items.armour.PlateChest()     
        # legs
        if randint(0,99) < 50:
            self.body.legs = items.armour.PlateLegs()         
        # boots
        if randint(0,99) < 50:
            self.body.boots = items.armour.PlateBoots()
        # weapon
        weapon_chance = randint(0,99)
        if weapon_chance < 80:
            self.weapon = items.weapons.LongSword()
        else:
            self.weapon = items.weapons.BastardSword()

# exceptions
class DeadException(Exception):
    pass

class WinException(Exception):
    pass

class WinBossException(Exception):
    pass

class EscapeException(Exception):
    pass
