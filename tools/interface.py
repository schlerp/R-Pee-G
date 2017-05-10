try:
    import pyfiglet
except ImportError:
    pyfiglet = None

import items
import tools
import battle

# template
template = ''' {head}  
{l_arm}{chest}{r_arm} 
{l_hand}{pelvis}{r_hand} 
{l_leg} {r_leg}{weapon}
{foot} {foot} '''

# parts
head_bare = '0'
head_armour = 'W'

l_arm_bare = '|'
l_arm_armour = '{'
r_arm_bare = '|'
r_arm_armour = '}'

chest_bare = '#'
chest_armour = 'U'

l_hand_bare = 'l'
l_hand_armour = '@'
r_hand_bare = 'l'
r_hand_armour = 't'
weapon = '\\'
no_weapon = ' '

pelvis_bare = 'u'
pelvis_armour = 'V'

l_leg_bare = '|'
l_leg_armour = '['
r_leg_bare = '|'
r_leg_armour = ']'

foot_bare = 'j'
foot_armour = 'J'


def do_intro():
    tools.utils.cls()
    if pyfiglet != None:
        fig_title = pyfiglet.Figlet(font='caligraphy')
        print(fig_title.renderText('R Pee G'))
    print('R-Pee-G, a game by schlerp\n')
    tools.utils.pause()
    tools.utils.cls()
    print('\nwelcome to the game motherfucker!')
    print('---------------------------------\n')
    print('You have woken up in a a castle, you need to escape or face grave danger.')
    print('Battle your way out if you can... **INSERT EVIL LAUGH!**\n')
    print('how it works:')
    print('Upon antering a room, you may be attacked if enemy present.')
    print('Once enemy has been dealt with you will auto-loot the room.')
    print('Once room has been looted you will be able to make a choice as to which direction to head.\n')
    print('Not implemented:')
    print(' * getting items from inventory')
    print('    > using')
    print('    > equipping ')
    print('    > dropping ')
    print('    > etc...')
    print(' * boss fights')
    print(' * level progression and experience/skill trees')
    tools.utils.pause()
    tools.utils.cls()


def text_block(text, force_width=False):
    '''turns multiline string into text block'''
    _max = 0
    for row in text.split('\n'):
        if len(row) > _max:
            _max = len(row)
    if force_width:
        _max = force_width
    ret = ''
    for row in text.split('\n'):
        for i in range(_max):
            try:
                ret += row[i]
            except IndexError:
                ret += ' '
        ret += '\n'
    return ret[0:-1]
    
def text_centre(avatar, width):
    '''centres an avatar'''
    avatar_block = text_block(avatar)
    avatar_width = len(avatar_block.split('\n')[0])
    pre_len = (width - avatar_width) // 2
    post_len = width - pre_len 
    ret = ''
    for row in avatar_block.split('\n'):
        ret += ' '*pre_len + row + ' '*post_len + '\n'
    return ret
    

def side_by_side(left, right, size=30, sep='   '):
    '''joins two pieces of text side by side'''
    left_block = text_block(left, size)
    right_block = text_block(right, size)
    ret = ''
    for line, text in enumerate(left_block.split('\n')):
        ret += text + sep + right_block.split('\n')[line] + '\n'
    return ret


def build_hero_avatar(hero):
    '''scans hero equipment, renders character'''
    # head
    if str(hero.body.head) == 'Bare':
        _head = head_bare
    else:
        _head = head_armour
    
    # chest
    if str(hero.body.chest) == 'Bare':
        _l_arm = l_arm_bare
        _r_arm = r_arm_bare
        _chest = chest_bare
    else:
        _l_arm = l_arm_armour
        _r_arm = r_arm_armour
        _chest = chest_armour

    # shield
    if str(hero.body.shield) == 'Bare':
        _l_hand = l_hand_bare
    else:
        _l_hand = l_hand_armour
    
    # weapon
    if str(hero.weapon) == 'Fists':
        _r_hand = r_hand_bare
        _weapon = no_weapon
    else:
        _r_hand = r_hand_armour
        _weapon = weapon
    
    # legs
    if str(hero.body.legs) == 'Bare':
        _l_leg = l_leg_bare
        _r_leg = r_leg_bare
        _pelvis = pelvis_bare
    else:
        _l_leg = l_leg_armour
        _r_leg = r_leg_armour
        _pelvis = pelvis_armour
    
    # boots
    if str(hero.body.boots) == 'Bare':
        _foot = foot_bare
    else:
        _foot = foot_armour

    return template.format(head=_head, l_arm=_l_arm, r_arm=_r_arm, chest=_chest,
                           l_hand=_l_hand, r_hand=_r_hand, weapon=_weapon,
                           l_leg=_l_leg, r_leg=_r_leg, pelvis=_pelvis, foot=_foot)


def get_hero_stats(hero):
    defence = hero.get_defence()
    defending = hero.get_defence(True)
    ret = 'attack  {}\n'.format(hero.get_offence())
    ret += 'def agg {}\ndef def {}\n'.format(defence, defending)
    return ret
    
def get_hero_inventory(hero):
    ret = 'Inventory:\n'
    if len(hero.inventory) == 0:
        ret += '[EMPTY!]'
    else:
        for item in hero.inventory:
            ret += '[' + str(item) + '] '
    return ret

def check_boolean(choice):
    if choice.lower() in ('y', 'yes', 'true', 't', 'positive'):
        return 'yes'
    if choice.lower() in ('n', 'no', 'false', 'f', 'negative'):
        return 'no'

def use_item_free(player):
    while True:
        try:
            choice = input('Would you like to use an item? [y/N]: ')
            if choice == '':
                choice = 'no'
            if check_boolean(choice) == 'yes':
                tools.utils.cls()
                items.use_item(player)
            elif check_boolean(choice) == 'no':
                break
            else:
                print('Unknown option! please choose yes or no')
        except items.ConsumableExpiredException as e:
            pass

class NotValidChoice(Exception):
    '''when a non valid choice is chosen'''
    pass

def choose_from_list(iterable):
    choice_max = len(iterable) - 1
    for index, name in enumerate(iterable):
        print('[{}] {}'.format(index, str(name)))
    print('Select number:')
    while True:
        choice = input('>>> ')
        try:
            choice = int(choice)
            if choice > choice_max:
                raise NotValidChoice
            return choice
        except ValueError as e:
            print('Unknow option: {}'.format(choice))
            pass
        except NotValidChoice:
            print('Choice outside of range (0-{})'.format(choice_max))
            pass
        except KeyboardInterrupt:
            print('User cancelled choice...')
            return None

def battle_choose(default=''):
    while True:
        print('Current actions:')
        for act in battle.actions:
            name_block = text_block("[{}]".format(act.name), 10)
            print('  {} {}'.format(name_block, act.description))
        print('')
        try:
            choice = input('[{}]>>> '.format(default))
            return battle.get_action(choice)
        except battle.ActionNotFound:
            print('Action not found!')


def build_battle_scene(player, ai, width=35):
    '''draws the battle scene'''
    #ret = side_by_side(str(player), str(ai), width)
    #ret = '{} ({})  vs. {} ({})\n'.format(player.name, player.hp, ai.name, ai.hp)
    player_stats = get_hero_stats(player)
    ai_stats = get_hero_stats(ai)
    ret = ''
    ret += str(player) + '\n'
    ret += player_stats
    ret += text_centre('vs.', width)
    ret += str(ai) + '\n'
    ret += ai_stats +'\n'
    #ret += side_by_side(player_stats, ai_stats, size=width)
    player_avatar = build_hero_avatar(player)
    ai_avatar = build_hero_avatar(ai)
    ret += side_by_side(text_centre(player_avatar, width//2), 
                        text_centre(ai_avatar, width//2),
                        width//2)
    return ret


def build_room_scene(player, room, width=35):
    '''draws the current room/player stats'''
    ret = str(player) + '\n'
    ret += get_hero_stats(player) + '\n'
    ret += text_centre(build_hero_avatar(player), width) + '\n'
    ret += get_hero_inventory(player) + '\n\n'
    ret += '[' + room.name + ']\n'
    ret += room.description + '\n'
    return ret