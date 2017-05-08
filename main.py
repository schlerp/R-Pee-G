import sys
import pyfiglet

from character import Hero, Enemy, DeadException, WinException, EscapeException, WinBossException
from item import Dagger, BastardSword, MagicBlade, FireBlade, IceBlade, PoisonBlade, Bite
from item import LeatherBoots, LeatherChest, LeatherHelmet, LeatherLegs, SmallShield, Medkit, ConsumableExpiredException
from item import use_item
from mapping import Map, pick_rand_room, handle_move
from battle import battle
from interface import build_hero_avatar, get_hero_stats, text_centre, build_room_scene, do_intro, use_item_free
from utils import cls, pause


if __name__ == '__main__':

    # define hero and enemy
    me = Hero(name='schlerp', hp=100, lvl=1)
    me.weapon = BastardSword()
    me.body.boots = LeatherBoots()
    me.body.chest = LeatherChest()
    me.body.head = LeatherHelmet()
    me.body.legs = LeatherLegs()
    me.body.shield = SmallShield()
    me.inventory.append(Medkit(quantity=3))
    
    height = 5
    width = 5
    
    enemy_rooms = 10
    loot_rooms = 10
    
    block_width = 35

    world_map = Map(width, height, loot_rooms, enemy_rooms)
    
    start_location = pick_rand_room(width, height)
    me.location = start_location

    # figlet fonts
    fig_death = pyfiglet.Figlet(font='poison')
    fig_win = pyfiglet.Figlet(font='doom')
    
    do_intro()
    try:
        while True:
            cls()
            room = world_map.get_room(me.location)
            print(build_room_scene(me, room, block_width))
            
            if room.enemies:
                for enemy in room.enemies:
                    if enemy.is_alive():
                        try:
                            battle(me, enemy, room.boss)
                        except WinException:
                            print(fig_win.renderText('You defeated!'))
                            # enemy drops hit loot
                            while len(enemy.loot) > 0:
                                _loot = enemy.loot.pop()
                                room.inventory.append(_loot)
                                print('{} dropped {}'.format(me.name, _loot))                        
                            room.description += ' ({} Dead!)'.format(enemy.name)
                            pause()
                        except DeadException:
                            print(fig_death.renderText('You died!'))
                            sys.exit(2)
                        except EscapeException:
                            print('You ran from the battle!')
                            pause()
            if room.loot:
                while len(room.loot) > 0:
                    print('Got item!')
                    _loot = room.loot.pop()
                    me.add_item(_loot)
                    print('{} found {}'.format(me.name, _loot))
                room.desciption = 'A room that has been looted already.'
                pause()
            
            # add support for vendor/shop rooms
            # coming soon...
            
            # allow item use
            cls()
            print(build_room_scene(me, room, block_width))
            use_item_free(me)
            
            # get direction
            cls()
            print(build_room_scene(me, room, block_width))
            direction = handle_move(world_map, me)
            
            cls()
            print(build_room_scene(me, room, block_width))
            print("You head off towards the {}".format(direction))
    
            pause()
    except WinBossException:
        fig_boss_win = pyfiglet.Figlet(font='caligraphy')        
        print(fig_boss_win.renderText('You'))
        print(fig_boss_win.renderText('Win!'))
        sys.exit(0)
    
    ## define hero and enemy
    #me = Hero(name='schlerp', hp=100, lvl=0)
    #me.weapon = BastardSword()
    #me.body.boots = LeatherBoots()
    #me.body.chest = LeatherChest()
    #me.body.head = LeatherHelmet()
    #me.body.legs = LeatherLegs()
    #me.body.shield = SmallShield()
    
    #orc = Enemy(name='orc frik', hp=100)
    #orc.weapon = MagicBlade()
    
    #dog = Enemy(name='big dog', hp=50)
    #dog.weapon = Bite()

    ## game example starts here:    
    #cls() 
    #print('welcome to the game motherfucker!\n')
    #pause()
    
    #cls()
    #print('suddenly an orc approches! You are thrust into battle.\n')
    #pause()
    
    #try:
        #battle(me, orc)
    #except DeadException:
        #print("You died...")
        #sys.exit(2)
    #except WinException:
        #print("You won!")
    #except EscapeException:
        #print("You Escaped!")
    #pause()
    
    #cls()
    #print('suddenly a big dog approches! You are thrust into battle.\n')
    #pause()

    #try:
        #battle(me, dog)
    #except DeadException:
        #print("You died...")
        #sys.exit(2)
    #except WinException:
        #print("You won!")
    #except EscapeException:
        #print("You Escaped!")
    #pause()
    
    #cls()
    #print("You finished the example!\n")
    #pause()
