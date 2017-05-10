#from item import Equipment, Defence
#from interface import choose_from_list

import items
import tools.interface


class BodyPart(object):
    '''base class for body parts (armour locations)'''
    def __init__(self, name='body part'):
        self.name = name
    def __repr__(self):
        return self.name


class AnyPart(BodyPart):
    '''can be placed on any part of body'''
    def __init__(self):
        super().__init__(name='any')

class Head(BodyPart):
    '''head of body'''
    def __init__(self):
        super().__init__(name='head')

class Chest(BodyPart):
    '''chest of body'''
    def __init__(self):
        super().__init__(name='chest')    

class Legs(BodyPart):
    '''legs of body'''
    def __init__(self):
        super().__init__(name='legs')

class Boots(BodyPart):
    '''feet of body'''
    def __init__(self):
        super().__init__(name='boots')    

class Shield(BodyPart):
    '''a shield'''
    def __init__(self):
        super().__init__(name='shield')


body_parts = [Head, Chest, Legs, Boots, Shield]

class Armour(items.Equipment):
    '''base class for all armour'''
    def __init__(self, name, physical, quality, body_part=AnyPart(), magic=0, fire=0, ice=0, poison=0, description=None):
        super().__init__(name, description)
        self.defence = items.Defence(physical, physical-quality, magic, fire, ice, poison)
        self.body_part = body_part
    def use(self, player, ai=None):
        for index, _item in enumerate(player.inventory):
            if isinstance(_item, type(self)):
                new_armour = player.inventory.pop(index)
                if new_armour.body_part == AnyPart():
                    choice = tools.interface.choose_from_list(body_parts)
                    if choice == None:
                        return
                    body_part = body_parts[choice]
                else:
                    body_part = new_armour.body_part
                old_item = player.body.replace_equipment(body_part, new_armour)
                player.add_item(old_item)


class Bare(Armour):
    '''bare unprotected skin'''
    def __init__(self):
        name = 'Bare'
        super().__init__(name=name, body_part=AnyPart(), physical=0, quality=0, magic=0, fire=0, 
                         ice=0, poison=0, description=self.__doc__)


# leather armour
class LeatherHelmet(Armour):
    '''helmet made of leather'''
    def __init__(self):
        name = 'Leather Helmet'
        super().__init__(name=name, body_part=Head(), physical=3, quality=3, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class LeatherChest(Armour):
    '''chest armour made of leather'''
    def __init__(self):
        name = 'Leather Chest'
        super().__init__(name=name, body_part=Chest(), physical=5, quality=2, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class LeatherLegs(Armour):
    '''pants made of leather'''
    def __init__(self):
        name = 'Leather Pants'
        super().__init__(name=name, body_part=Legs(), physical=5, quality=5, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)

class LeatherBoots(Armour):
    '''boots made of leather'''
    def __init__(self):
        name = 'Leather Boots'
        super().__init__(name=name, body_part=Boots(), physical=3, quality=0, magic=1, fire=1, 
                         ice=1, poison=1, description=self.__doc__)



# chainmail armour
class ChainmailHelmet(Armour):
    '''helmet made of chainmail'''
    def __init__(self):
        name = 'Chainmail Helmet'
        super().__init__(name=name, body_part=Head(), physical=7, quality=7, magic=3, fire=3, 
                         ice=3, poison=3, description=self.__doc__)

class ChainmailChest(Armour):
    '''chest armour made of chainmail'''
    def __init__(self):
        name = 'Chainmail Chest'
        super().__init__(name=name, body_part=Chest(), physical=10, quality=3, magic=3, fire=3, 
                         ice=3, poison=3, description=self.__doc__)

class ChainmailLegs(Armour):
    '''pants made of chainmail'''
    def __init__(self):
        name = 'Chainmail Pants'
        super().__init__(name=name, body_part=Legs(), physical=7, quality=2, magic=3, fire=3, 
                         ice=3, poison=3, description=self.__doc__)

class ChainmailBoots(Armour):
    '''boots made of chainmail'''
    def __init__(self):
        name = 'Chainmail Boots'
        super().__init__(name=name, body_part=Boots(), physical=5, quality=0, magic=3, fire=3, 
                         ice=3, poison=3, description=self.__doc__)


# plate armour
class PlateHelmet(Armour):
    '''helmet made of plate'''
    def __init__(self):
        name = 'Plate Helmet'
        super().__init__(name=name, body_part=Head(), physical=12, quality=7, magic=5, fire=5, 
                         ice=5, poison=5, description=self.__doc__)

class PlateChest(Armour):
    '''chest armour made of plate'''
    def __init__(self):
        name = 'Plate Chest'
        super().__init__(name=name, body_part=Chest(), physical=20, quality=5, magic=5, fire=5, 
                         ice=5, poison=5, description=self.__doc__)

class PlateLegs(Armour):
    '''pants made of plate'''
    def __init__(self):
        name = 'Plate Pants'
        super().__init__(name=name, body_part=Legs(), physical=10, quality=4, magic=5, fire=5, 
                         ice=5, poison=5, description=self.__doc__)

class PlateBoots(Armour):
    '''boots made of plate'''
    def __init__(self):
        name = 'Plate Boots'
        super().__init__(name=name, body_part=Boots(), physical=7, quality=0, magic=5, fire=5, 
                         ice=5, poison=5, description=self.__doc__)


# shields
class SmallShield(Armour):
    '''a small shield'''
    def __init__(self):
        name = 'Helmet'
        super().__init__(name=name, body_part=Shield(), physical=15, quality=10, magic=10, fire=10, 
                         ice=10, poison=10, description=self.__doc__)

class MidShield(Armour):
    '''a medium shield'''
    def __init__(self):
        name = 'Helmet'
        super().__init__(name=name, body_part=Shield(), physical=25, quality=15, magic=15, fire=15, 
                         ice=15, poison=15, description=self.__doc__)

class LargeShield(Armour):
    '''a large shield'''
    def __init__(self):
        name = 'Large Shield'
        super().__init__(name=name, body_part=Shield(), physical=50, quality=25, magic=25, fire=25, 
                         ice=25, poison=25, description=self.__doc__)