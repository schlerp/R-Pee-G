#from items import Item

import items

# CONSUMABLES

class Consumable(items.Item):
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