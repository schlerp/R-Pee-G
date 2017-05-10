from random import randint

import items

def low_loot():
    loot_choice = randint(0,99)
    if loot_choice < 25:
        # gold
        amount = randint(1,50)
        return items.consumables.Gold(quantity=amount)
    elif loot_choice < 50:
        # weapon
        wep_choice = randint(0,99)
        if wep_choice < 33:
            return items.weapons.Dagger()
        if wep_choice < 66:
            return items.weapons.HandAxe()
        else:
            return items.weapons.Rapier()
    elif loot_choice < 75:
        # armour
        armour_choice = randint(0,99)
        if armour_choice < 20:
            return items.armour.LeatherBoots()
        elif armour_choice < 40:
            return items.armour.LeatherLegs()
        elif armour_choice < 60:
            return items.armour.LeatherChest()
        elif armour_choice < 80:
            return items.armour.LeatherHelmet()
        else:
            return items.armour.SmallShield()
    else:
        # medkits
        amount = randint(1,2)
        return items.consumables.Medkit(quantity=amount)


def mid_loot():
    loot_choice = randint(0,99)
    if loot_choice < 25:
        # gold
        amount = randint(50, 100)
        return items.consumables.Gold(quantity=amount)
    elif loot_choice < 50:
        # weapon
        wep_choice = randint(0,99)
        if wep_choice < 25:
            return items.weapons.LongSword()
        elif wep_choice < 50:
            return items.weapons.Katana()
        elif wep_choice < 75:
            return items.weapons.GreatSword()
        else:
            return items.weapons.BastardSword()
    elif loot_choice < 75:
        # armour
        armour_choice = randint(0,99)
        if armour_choice < 20:
            return items.armour.ChainmailBoots()
        if armour_choice < 40:
            return items.armour.ChainmailLegs()
        if armour_choice < 60:
            return items.armour.ChainmailChest()
        if armour_choice < 80:
            return items.armour.ChainmailHelmet()
        else:
            return items.armour.MidShield()
    else:
        # medkits
        amount = randint(1,2)
        return items.consumables.BigMedkit(quantity=amount)


def high_loot():
    loot_choice = randint(0,99)
    if loot_choice < 25:
        # gold
        amount = randint(100,200)
        return items.consumables.Gold(quantity=amount)
    elif loot_choice < 50:
        # weapon
        wep_choice = randint(0,99)
        if wep_choice < 25:
            return items.weapons.MagicBlade()
        if wep_choice < 50:
            return items.weapons.FireBlade()
        elif wep_choice < 75:
            return items.weapons.IceBlade()
        else:
            return items.weapons.PoisonBlade()
    elif loot_choice < 75:
        # armour
        armour_choice = randint(0,99)
        if armour_choice < 20:
            return items.armour.PlateBoots()
        if armour_choice < 40:
            return items.armour.PlateLegs()
        if armour_choice < 60:
            return items.armour.PlateChest()
        if armour_choice < 80:
            return items.armour.PlateHelmet()
        else:
            return items.armour.LargeShield()
    else:
        # medkits
        return items.consumables.GoldenApple(quantity=1)       