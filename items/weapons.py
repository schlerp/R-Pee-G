#from item import Equipment, Damage

import items

class Weapon(items.Equipment):
    '''base class for all weapons'''
    def __init__(self, name, physical, quality, magic=0, fire=0, ice=0, poison=0, description=None):
        super().__init__(name, description)
        self.damage = items.Damage(physical, physical-quality, magic, fire, ice, poison)
    def use(self, player, ai=None):
        if player.weapon != Fists():
            player.inventory.append(player.weapon)
        for index, _item in enumerate(player.inventory):
            if isinstance(_item, type(self)):
                player.weapon = player.inventory.pop(index)


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

class HandAxe(Weapon):
    '''an axe weapon, low to mid damage'''
    def __init__(self):
        name = 'Hand Axe'
        super().__init__(name, 25, 20, description=self.__doc__)

class SmallSword(Weapon):
    '''a small sword weapon'''
    def __init__(self):
        name = 'Small Sword'
        super().__init__(name, 25, 10, description=self.__doc__)

class LongSword(Weapon):
    '''a small sword weapon'''
    def __init__(self):
        name = 'Long Sword'
        super().__init__(name, 40, 25, description=self.__doc__)

class Rapier(Weapon):
    '''a rapier weapon, always low-mid damage'''
    def __init__(self):
        name = 'Rapier'
        super().__init__(name, 20, 5, description=self.__doc__)

class Scimitar(Weapon):
    '''a scimitar weapon, always mid damage'''
    def __init__(self):
        name = 'Scimitar'
        super().__init__(name, 30, 5, description=self.__doc__)

class Katana(Weapon):
    '''a katana weapon, possible high damage'''
    def __init__(self):
        name = 'Katana'
        super().__init__(name, 50, 40, description=self.__doc__)

class BastardSword(Weapon):
    '''a big fuck-off sword, always high damage'''
    def __init__(self):
        name = 'Bastard Sword'
        super().__init__(name, 100, 20, description=self.__doc__)



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
