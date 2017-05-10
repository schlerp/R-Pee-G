from random import randint

import characters
import tools
import items


class ActionNotFound(Exception):
    pass


class Action(object):
    '''base class for all actions, allows compare'''
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __eq__(self, other):
        if isinstance(other, Action):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal == NotImplemented:
            return equal
        return not equal

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.__repr__()

class Attack(Action):
    '''represents a choice of attack during battle'''
    def __init__(self):
        super().__init__('attack', 'Hit opponent with weapon')

    @staticmethod
    def do(attacker, defender):
        attack =  attacker.weapon.damage - defender.get_defence()
        this_hit = attack.hit()
        defender.hp -= this_hit
        print('{} hit {} for {} damage'.format(attacker.name, defender.name, this_hit))

class Defend(Action):
    '''represents a choice of defend during battle'''
    def __init__(self):
        super().__init__('defend', 'Raise shield if equipped')

    @staticmethod
    def do(player):
        player.defending = True
        

class Item(Action):
    '''represents using an item from inventory'''
    def __init__(self):
        super().__init__('item', 'Use an item from inventory')

    @staticmethod
    def do():
        pass

class Run(Action):
    '''attempt running from fight'''
    def __init__(self):
        super().__init__('run', 'Try escape battle (enemy attack on re-entering room)')


#Attack = Action('attack', 'Hit the opponent with currently equiped weapon.')
#Defend = Action('defend', 'Raise your shield to cushion the oncoming blow.')
#Item = Action('item', 'Use an item from your inventory.')
#Run = Action('run', 'Attempt to escape to the previous room')

actions = (Attack(), Defend(), Item(), Run())


def do_attack(attacker, defender, defending=False, single_hand=False):
    attack =  attacker.weapon.damage - defender.get_defence(defending)
    this_hit = attack.hit()
    if single_hand:
        this_hit = this_hit // 2
    defender.hp -= this_hit
    print('')
    #get defense status
    if defending:
        status = 'defending'
    else:
        status = 'aggressive'
    # get attack type
    if single_hand:
        hit = 'hit (single handed)'
    else:
        hit = 'hit (dual handed)'
    print('{attacker} {hit} {defender} ({status}) for {damage} damage'.format(attacker=attacker.name,
                                                                              hit=hit,
                                                                              defender=defender.name, 
                                                                              status=status, 
                                                                              damage=this_hit))

def get_action(_input):
    if _input == '':
        return None
    elif _input.lower() == 'attack':
        return Attack()
    elif _input.lower() == 'defend':
        return Defend()
    elif _input.lower() == 'item':
        return Item()
    elif _input.lower() == 'run':
        return Run()
    else:
        raise ActionNotFound()


def battle(player, ai, boss=False):
    last_action = Attack()
    print('{} ({})  vs. {} ({})'.format(player.name, player.hp, ai.name, ai.hp))
    tools.utils.pause('press retrun to start battle...')
    while True:
        tools.utils.cls()
        print(tools.interface.build_battle_scene(player, ai))
        print()
        
        if player.is_alive():
            action = tools.interface.battle_choose(default=last_action)
            
            # apply default
            if action == None:
                action = last_action
    
            # handle actions
            if action.name == 'attack':
                do_attack(player, ai)                
                if ai.is_alive():
                    do_attack(ai, player)
            if action.name == 'defend':
                do_attack(player, ai, single_hand=True)
                if ai.is_alive():
                    do_attack(ai, player, defending=True)
            if action.name == 'item':
                items.use_item(player, ai)
            if action.name == 'run':
                if randint(0,9) <= 2 :
                    raise EscapeException
                print('{} tries to escape but fails!'.format(player.name))
                do_attack(ai, player)

        last_action = action

        if not player.is_alive():
            raise characters.DeadException()
        if not ai.is_alive():
            if boss:
                raise characters.WinBossException
            else:
                raise characters.WinException
            
        
        tools.utils.pause()