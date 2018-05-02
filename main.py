from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
# spell_name = Spell('name', cost, dmg, 'type')
fire = Spell('Fire', 10, 600, 'black')
thunder = Spell('Thunder', 10, 600, 'black')
blizzard = Spell('Blizzard', 10, 600, 'black')
meteor = Spell('Meteor', 50, 1200, 'black')
quake = Spell('Quake', 14, 1140, 'black')

# Create White Magic
# spell_name = Spell('name', cost, dmg, 'type')
cure = Spell('Cure', 12, 620, 'white')
cura = Spell('Cura', 18, 1500, 'white')

# Create Items
# item_name = Item('name', 'type', 'description', 'prop')
potion = Item('Potion', 'potion', 'Heals 50 HP', 50)
hipotion = Item('Hi-Potion', 'potion', 'Heals 100 HP', 100)
superpotion = Item('Super Potion', 'potion', 'Heals 500 HP', 1500)
elixer = Item('Elixer', 'elixer', 'Fully restores HP/MP of one party member', 9999)
hielixer = Item('Mega Elixer', 'elixer', 'Fully restores party\'s HP/MP', 9999)

grenade = Item('Grenade', 'attack', 'Deals 500 damage', 500)

player_spells = [fire, thunder,blizzard, meteor, cure, cura]
player_items = [{'item': potion, 'quantity': 15}, {'item': hipotion, 'quantity': 5},
                {'item': superpotion, 'quantity': 5}, {'item': elixer, 'quantity': 5},
                {'item': hielixer, 'quantity': 2}, {'item': grenade, 'quantity': 5}]

# Create Pawns
# entity_name = Spell(name, hp, mp, atk, df, magic, items)
player1 = Person('ElfIRL:     ', 3460, 300, 132, 34, player_spells, player_items)
player2 = Person('Jade:       ', 1460, 288, 188, 34, player_spells, player_items)
player3 = Person('Sixdemonbag:', 5460, 400, 174, 34, player_spells, player_items)

enemy1 = Person('Janus', 18200, 701, 451, 25, [], [])
enemy2 = Person('Imp  ', 1250, 130, 475, 325, [], [])
enemy3 = Person('Imp  ', 1250, 130, 475, 325, [], [])

players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + 'AN ENEMY ATTACKS!' + bcolors.ENDC)
while running:
  print('=======================')

  print('\n\n')
  print('NAME                     HP                                    MP')
  for player in players:
    player.get_stats()

  print('\n')

  for enemy in enemies:
    enemy.get_enemy_stats()

  for player in players:
    player.choose_action()
    choice = input('    Choose action: ')
    index = int(choice) - 1

    if index == 0:
      dmg = player.generate_damage()
      enemy = player.choose_target(enemies)
      enemies[enemy].take_damage(dmg)
      print('You attacked ' + enemies[enemy].name.replace(' ', '') + ' for', dmg, 'points of damage.')

      if enemies[enemy].get_hp() == 0:
        print(enemies[enemy].name.replace(' ', '') + ' has died.')
        del enemies[enemy]

    elif index == 1:
      player.choose_magic()
      magic_choice = int(input('    Choose magic: ')) - 1

      if magic_choice == -1:
        continue

      spell = player.magic[magic_choice]
      magic_dmg = spell.generate_damage()

      current_mp = player.get_mp()

      if spell.cost > current_mp:
        print(bcolors.FAIL + '\nNot enough MP\n' + bcolors.ENDC)
        continue

      player.reduce_mp(spell.cost)

      if spell.type == 'white':
        player.heal(magic_dmg)
        print(bcolors.OKBLUE + '\n' + spell.name + ' heals for', str(magic_dmg), 'HP.' + bcolors.ENDC)
      elif spell.type == 'black':
        enemy = player.choose_target(enemies)
        enemies[enemy].take_damage(magic_dmg)

        print(bcolors.OKBLUE + '\n' + spell.name + ' deals', str(magic_dmg), 'points of damage to ' + enemies[enemy].name.replace(' ', '') + bcolors.ENDC)

        if enemies[enemy].get_hp() == 0:
          print(enemies[enemy].name.replace(' ', '') + ' has died.')
          del enemies[enemy]

    elif index == 2:
      player.choose_item()
      item_choice = int(input('    Choose item: ')) - 1

      if item_choice == -1:
        continue

      item = player.items[item_choice]['item']

      if player.items[item_choice]['quantity'] == 0:
        print(bcolors.FAIL + '\n' + 'None left...' + bcolors.ENDC)
        continue

      player.items[item_choice]['quantity'] -= 1

      if item.type == 'potion':
        player.heal(item.prop)
        print(bcolors.OKGREEN + '\n' + item.name + ' heals for', str(item.prop), 'HP' + bcolors.ENDC)
      elif item.type == 'elixer':
        if item.name == 'MegaElixer':
          for i in players:
            i.hp = i.maxhp
            i.mp = i.maxmp
        else:
          player.hp = player.maxhp
          player.mp = player.maxmp
        print(bcolors.OKGREEN + '\n' + item.name + ' fully restores HP/MP' + bcolors.ENDC)
      elif item.type == 'attack':
        enemy = player.choose_target(enemies)
        enemies[enemy].take_damage(item.prop)
        
        print(bcolors.FAIL + '\n' + item.name + ' deals', str(item.prop), 'points of damage to ' + enemies[enemy].name.replace(' ', '') + bcolors.ENDC)

        if enemies[enemy].get_hp() == 0:
          print(enemies[enemy].name.replace(' ', '') + ' has died.')
          del enemies[enemy]

  enemy_choice = 1
  target = random.randrange(len(players))
  enemy_dmg = enemies[0].generate_damage()

  players[target].take_damage(enemy_dmg)
  print('Enemy attacks for', enemy_dmg, 'points of damage.')

  defeated_enemies = 0
  defeated_players = 0

  for enemy in enemies:
    if enemy.get_hp() == 0:
      defeated_enemies += 1

  for player in players:
    if player.get_hp() == 0:
      defeated_players += 1

  if defeated_enemies == 3:
    print(bcolors.OKGREEN + 'You win! \n' + bcolors.ENDC)
    running = False

  elif defeated_players == 3:
    print(bcolors.FAIL + 'Your enemies have defeated you!' + bcolors.ENDC)
    running = False

