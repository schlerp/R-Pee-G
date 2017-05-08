from random import randint

class ConsumableExpiredException(Exception):
    '''attempted to use expired consumable'''
    pass

def use_item(player, ai=None):
    for slot, item in enumerate(player.inventory):
        print('[{}]'.format(slot), str(item))
    print('Select item by number:')
    choice = input('>>> ')
    try:
        item = player.inventory[int(choice)]
        item.use(player, ai)
    except ConsumableExpiredException as e:
        if item.removable:
            _ = player.inventory.pop(choice)
            del _
        print('you are out of {} (quantity={})'.format(item.name, item.quantity))
    #except Exception as e:
        ##import traceback
        ##traceback.format_exc()
        ##print(e.with_traceback(None))
        #print("'{}' is not a valid choice!".format(choice))
        

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
        return Damage(physical, physical_min, magic, fire, ice, poison)

    def _subtract(self, other):
        '''subtracts damage (applies defense)'''
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
    
    def __repr__(self):
        template = '{}-{}D, {}M, {}F, {}I, {}P'
        return template.format(self.physical_min, self.physical, self.magic,
                               self.fire, self.ice, self.poison)

class Equipment(Item):
    '''base class for equipment (equipable) items'''
    pass

class BodyPart(object):
    '''base class for body parts (armour locations)'''
    pass

class AnyPart(BodyPart):
    '''can be placed on any part of body'''
    pass

class Head(BodyPart):
    '''head of body'''
    pass

class Chest(BodyPart):
    '''chest of body'''
    pass

class Legs(BodyPart):
    '''legs of body'''
    pass

class Boots(BodyPart):
    '''feet of body'''
    pass

class Shield(BodyPart):
    '''a shield'''
    pass



# Weapons

class Weapon(Equipment):
    '''base class for all weapons'''
    def __init__(self, name, physical, quality, magic=0, fire=0, ice=0, poison=0, description=None):
        super().__init__(name, description)
        self.damage = Damage(physical, physical-quality, magic, fire, ice, poison)

class Fists(Weapon):
    '''your fists, represents no weapon'''
    def __init__(self):
        super().__init__('Fists', 1, 0, description=self.__doc__)

class Bite(Weapon):
    '''bite with mouth'''
    def __init__(self):
        super().__init__('Bite', 20, 20, description=self.__doc__)

class Dagger(Weapon):
    '''a basic short blade weapon'''
    def __init__(self):
        name = 'Dagger'
        super().__init__(name, 5, 5, description=self.__doc__)

class SmallSword(Weapon):
    '''a small sword weapon'''
    def __init__(self):
        name = 'Small Sword'
        super().__init__(name, 25, 10, description=self.__doc__)

class LongSword(Weapon):
    '''a small sword weapon'''
    def __init__(self):
        name = 'Small Sword'
        super().__init__(name, 40, 25, description=self.__doc__)

class BastardSword(Weapon):
    '''a big fuck-off sword'''
    def __init__(self):
        name = 'Bastard Sword'
        super().__init__(name, 50, 40, description=self.__doc__)

class MagicBlade(Weapon):
    '''a blade imbued with magic'''
    def __init__(self):
        name = 'Magic Blade'
        super().__init__(name, 15, 15, magic=25, description=self.__doc__)

class FireBlade(Weapon):
    '''a burning blade'''
    def __init__(self):
        name = 'Fire Blade'
        super().__init__(name, 15, 15, fire=25, description=self.__doc__)

class IceBlade(Weapon):
    '''a blade made of ice'''
    def __init__(self):
        name = 'Ice Blade'
        super().__init__(name, 15, 15, ice=25, description=self.__doc__)

class PoisonBlade(Weapon):
    '''a blade tipped with poison'''
    def __init__(self):
        name = 'Poison Blade'
        super().__init__(name, 15, 15, poison=25, description=self.__doc__)



# ARMOUR

class Armour(Equipment):
    '''base class for all armour'''
    def __init__(self, name, physical, quality, body_part=AnyPart(), magic=0, fire=0, ice=0, poison=0, description=None):
        super().__init__(name, description)
        self.defence = Damage(physical, physical-quality, magic, fire, ice, poison)
        self.body_part = body_part

class Bare(Armour):
    '''bare unprotected skin'''
    def __init__(self):
        name = 'Bare'
        super().__init__(name=name, body_part=AnyPart(), physical=0, quality=0, magic=0, fire=0, 
                         ice=0, poison=0, description=self.__doc__)

class LeatherHelmet(Armour):
    '''a simple leather helmet'''
    def __init__(self):
        name = 'Leather Helmet'
        super().__init__(name=name, body_part=Head(), physical=3, quality=3, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class LeatherChest(Armour):
    '''a simple leather chest plate'''
    def __init__(self):
        name = 'Leather Chest'
        super().__init__(name=name, body_part=Chest(), physical=5, quality=2, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class LeatherLegs(Armour):
    '''simple leather pants'''
    def __init__(self):
        name = 'Leather Pants'
        super().__init__(name=name, body_part=Legs(), physical=5, quality=5, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class LeatherBoots(Armour):
    '''a simple helmet'''
    def __init__(self):
        name = 'Leather Boots'
        super().__init__(name=name, body_part=Boots(), physical=3, quality=0, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class SmallShield(Armour):
    '''a small shield'''
    def __init__(self):
        name = 'Helmet'
        super().__init__(name=name, body_part=Shield(), physical=15, quality=10, magic=10, fire=10, 
                         ice=10, poison=10, description=self.__doc__)



# CONSUMABLES

class Consumable(Item):
    '''base class for all consumable items'''
    def __init__(self, name, description='consumable', quantity=1, removable=True):
        super().__init__(name, description)
        self.quantity = quantity
        self.removable = removable

    def use(self, character, ai=None):
        print('{} tries to use {}...'.format(character.name, self.name))
        if not self.expired:
            self.do_action(character, ai)
        else:
            raise ConsumableExpiredException
    
    def do_action(self, character, ai=None):
        '''apply the action of the item here'''
        pass

    def _consume(self):
        self.quantity -= 1
        if self.quantity < 1:
            self.expired = True

    def __repr__(self):
        return '{} ({})'.format(self.name, self.quantity)


class Gold(Consumable):
    '''the base currency'''
    def __init__(self, name='Gold', description='A small pile of gold', quantity=1, removable=False):
        super().__init__(name, description, quantity, removable)
    
    def do_action(self, character, ai=None, quantity=1):
        '''either pays for or drops gold'''
        if self.quantity < quantity:
            raise NotEnoughGoldException
        if ai:
            self.quantity -= quantity
            return True
        return False

class Medkit(Consumable):
    '''medkit regenerates small amount of health'''
    def __init__(self, quantity=1):
        description = self.__doc__
        super().__init__('Medkit', description, quantity=quantity)
        self.expired = False
        self.restore_hp = 25
    
    def do_action(self, character, ai=None):
        hp_before = character.hp
        character.hp += self.restore_hp
        hp_after = character.hp
        print('{} hp gained {}hp   ({} -> {})'.format(character.name, self.restore_hp, 
                                                      hp_before, hp_after))        

class BigMedkit(Consumable):
    '''medkit regenerates moderate amount of health'''
    def __init__(self, quantity=1):
        description = self.__doc__
        super().__init__('Big Medkit', description, quantity=1)
        self.expired = False
        self.restore_hp = 50
    
    def do_action(self, player, ai=None):
        hp_before = character.hp
        character.hp += self.restore_hp
        hp_after = character.hp
        print('{} hp gained {}: {} -> {}'.format(player.name, self.restore_hp, 
                                                         hp_before, hp_after)) 

class GoldenApple(Consumable):
    '''golden apple regenerates large amount of health'''
    def __init__(self, quantity=1):
        description = self.__doc__
        super().__init__('Golden Apple', description, quantity=1)
        self.expired = False
        self.restore_hp = 50
    
    def do_action(self, player, ai=None):
        hp_before = character.hp
        character.hp += self.restore_hp
        hp_after = character.hp
        print('{} hp gained {}: {} -> {}'.format(player.name, self.restore_hp, 
                                                         hp_before, hp_after)) 