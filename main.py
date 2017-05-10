
import sys
try:
    import pyfiglet
except ImportError:
    pyfiglet = None
    

import characters
import battle
import items
import tools
import world


# screen width
block_width = 35


def main():
    
    # figlet fonts
    if pyfiglet != None:
        fig_death = pyfiglet.Figlet(font='poison')
        fig_win = pyfiglet.Figlet(font='doom')
    
    # print intro
    tools.interface.do_intro()
    
    # get game setup
    player_name, difficulty, starting_items = tools.interface.game_setup()
    
    # define hero
    me = characters.Hero(name=player_name, hp=100, lvl=1)
    
    # apply difficulty
    if difficulty == tools.interface.DIFF_EASY:
        height = 5
        width = 5
        enemy_rooms = 5
        loot_rooms = 15
        
    elif difficulty == tools.interface.DIFF_MEDIUM:
        height = 7
        width = 7
        enemy_rooms = 15
        loot_rooms = 15
    
    elif difficulty == tools.interface.DIFF_HARD:
        height = 8
        width = 8
        enemy_rooms = 50
        loot_rooms = 5
    
    
    if starting_items == tools.interface.ITEMS_FEW:
        me.weapon = items.weapons.HandAxe()
        me.body.head = items.armour.LeatherHelmet()
        me.inventory.append(items.consumables.Medkit(quantity=1))
        
    elif starting_items == tools.interface.ITEMS_MEDIUM:
        me.weapon = items.weapons.Scimitar()
        me.body.chest = items.armour.LeatherChest()
        me.body.head = items.armour.LeatherHelmet()
        me.body.legs = items.armour.LeatherLegs()
        me.body.shield = items.armour.SmallShield()
        me.inventory.append(items.consumables.Medkit(quantity=3))
        
    elif starting_items == tools.interface.ITEMS_LOTS:
        me.weapon = items.weapons.Katana()
        me.body.boots = items.armour.LeatherBoots()
        me.body.chest = items.armour.LeatherChest()
        me.body.head = items.armour.LeatherHelmet()
        me.body.legs = items.armour.LeatherLegs()
        me.body.shield = items.armour.SmallShield()
        me.inventory.append(items.consumables.Medkit(quantity=5))
    
    world_map = world.mapping.Map(width, height, loot_rooms, enemy_rooms)
    
    start_location = world.mapping.pick_rand_room(width, height)
    me.location = start_location
    
    try:
        while True:
            tools.utils.cls()
            room = world_map.get_room(me.location)
            print(tools.interface.build_room_scene(me, room, block_width))
            
            if room.enemies:
                for enemy in room.enemies:
                    if enemy.is_alive():
                        try:
                            battle.battle(me, enemy, room.boss)
                        except characters.WinException:
                            if pyfiglet != None:
                                print(fig_win.renderText('You defeated!'))
                            else:
                                print('You Defeated!')
                            # enemy drops loot
                            while len(enemy.loot) > 0:
                                _loot = enemy.loot.pop()
                                room.loot.append(_loot)
                                print('{} dropped {}'.format(enemy.name, _loot))                        
                            room.description = '{} lays dead on the floor Dead!'.format(enemy.name)
                            tools.utils.pause()
                        except characters.DeadException:
                            if pyfiglet != None:
                                print(fig_death.renderText('You died!'))
                            else:
                                print('You Died!')
                            sys.exit(2)
                        except characters.EscapeException:
                            print('You ran from the battle!')
                            tools.utils.pause()
            if room.loot:
                room.description += '\n{} '.format(me.name)
                room.description +='took the following from this room:\n'
                while len(room.loot) > 0:
                    _loot = room.loot.pop()
                    me.add_item(_loot)
                    print('{} found {}'.format(me.name, _loot))
                    room.description += '[{}] '.format(_loot)
                tools.utils.pause()
            
            # add support for vendor/shop rooms
            # coming soon...
            
            # allow item use
            tools.utils.cls()
            print(tools.interface.build_room_scene(me, room, block_width))
            tools.interface.use_item_free(me)
            
            # get direction
            tools.utils.cls()
            print(tools.interface.build_room_scene(me, room, block_width))
            direction = world.mapping.handle_move(world_map, me)
            
            tools.utils.cls()
            print(tools.interface.build_room_scene(me, room, block_width))
            print("You head off towards the {}".format(direction))
    
            tools.utils.pause()
    
    except characters.WinBossException:
        if pyfiglet != None:
            fig_boss_win = pyfiglet.Figlet(font='caligraphy')        
            print(fig_boss_win.renderText('You'))
            print(fig_boss_win.renderText('Win'))
        else:
            print('\n\nYOU WON!!!!!\n\n')
        sys.exit(0)


if __name__ == '__main__':
    main()