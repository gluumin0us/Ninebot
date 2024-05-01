import os
import random

import discord
from replit import db

from character import Character

"""
str dex cha int att wil luc
 0   1   2   3   4   5   6
"""

names = {
  # Names and their associated user IDs
  "JACK": "359489732134305793",
  "FELIX": "531288319859097601",
  "SIMON": "262320046653702145",
  "MICHAEL": "962543637445615656",
  "MIKEY": "962543637445615656",
  "ALEX": "634509185198981141",
  "JOAUQIN": "251897105038180365",
  "PASTA": "251897105038180365",
  "DYLAN": "900187776836862003"
}

"""
my_char = Character("Simon", 1, 0)
my_char.legendary[3] += 1
my_char.legendary[5] += 1
my_char.id = "262320046653702145"

felix_char = Character("Felix", 2, 20)
felix_char.legendary[5] += 1
felix_char.id = names["FELIX"]

mike_char = Character("Michael", 3, 164)
mike_char.legendary = [1, 0, 1, 0, 1, 2, 0]
mike_char.talisman("Pearl Necklace", 0, 0)
mike_char.id = names["MIKEY"]

jack_char = Character("Jack", 9, 1495)
jack_char.legendary[4] += 2
jack_char.legendary[5] += 1
jack_char.legendary[6] += 1
jack_char.talisman("Vision's Necklace", 5, 1)
jack_char.talisman("Wrapped Ribbon", 1, 2)
jack_char.talisman("Dragon's Bane Armor", 4, 4)
jack_char.thp = 40
jack_char.id = names["JACK"]
"""

def char_to_list(char: Character):
  # Converts a Character object to a list for storage
  return [char.name, char.level, char.xp, char.hp, char.thp, 
          char.tal, char.effect, char.ss, char.pt, char.mod, char.legendary, 
          char.id]

def list_to_char(li_char: list):
  # Converts a character from a list to a Character object
  char = Character(li_char[0], li_char[1], li_char[2])
  char.hp = li_char[3]
  char.thp = li_char[4]
  char.tal = list(li_char[5])
  char.effect = list(li_char[6])
  char.ss = li_char[7]
  char.pt = list(li_char[8])
  char.mod = li_char[9]
  char.legendary = li_char[10]
  char.id = li_char[11]
  char.restat()
  return char

def printchar(char: Character):
  # Takes in a Character object
  # Returns a string that prints out a character's info
  printable = ""
  printable += (f"__{char.name}: LV{char.level}, {char.xp}/{char.xp_til_next}__\n")
  mark = ["", "", "", "", "", "", ""]
  for i in range(len(char.legendary)):
    for j in range(char.legendary[i]):
      mark[i] += '+'
  printable += (f"{mark[0]}Strength - {char.str}\n")
  printable += (f"{mark[1]}Dexterity - {char.dex}\n")
  printable += (f"{mark[2]}Charisma - {char.cha}\n")
  printable += (f"{mark[3]}Intelligence - {char.int}\n")
  printable += (f"{mark[4]}Attack - {char.att}\n")
  printable += (f"{mark[5]}Willpower - {char.wil}\n")
  printable += (f"{mark[6]}Luck - {char.luc}\n")
  for i in range(len(char.tal)):
    printable += (f"*TAL{i+1} - {char.tal[i]}*\n")
  printable += (f"HP - {char.hp}/{char.max_hp}\n")
  if char.thp > 0:
    printable += (f"THP - {char.thp}\n")
  return printable

# db["359489732134305793"] = char_to_list(jack_char)
# db["531288319859097601"] = char_to_list(felix_char)
# db["962543637445615656"] = char_to_list(mike_char)
# db["262320046653702145"] = char_to_list(my_char)

char_cache = {}

def find_char(id: str):
  # Finds and returns a character by ID.
  # First look in cache, then look in database.
  # If character found in database, store it in cache.
  # If no character is found, return False.
  if id in char_cache:
    return char_cache[id]
  elif id in db:
    char_cache[id] = list_to_char(db[id])
    return char_cache[id]
  else:
    return False

def save_char(char: Character):
  # Saves a character's changes to the database,
  # Assuming there's already a copy there.
  print(f"Saving character to {char.id}.")
  char_list = char_to_list(char)
  db[char.id] = char_list
  print(db[char.id])

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

greetings_back = ["Hello!", "Hi!", "Good to see you!", "Howdy!"]

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  id = str(message.author.id)
  msg = message.content.upper()
      
  if msg.startswith('9..hello'):
    await message.channel.send(random.choice(greetings_back))

  if "LOVE" in msg or "ILY" in msg and "NINE" in msg and id == names['MIKEY']:
    await message.channel.send("I love you too Mikey!")

  if "THANKS" in msg or "THANK YOU" in msg and "NINE" in msg:
    await message.channel.send("You're welcome!")

  # Most methods of Ninebot starts with 9..
  if msg.startswith('9..'):
    print("message detected.")
    command = msg.split('9..', 1)[1]
    if command == '':
      print("There is nothing")
    command = command.split()
    
    match command[0]:
      case 'CHAR':
        print("character case entered.")
        if len(command) == 1:
          char = find_char(id)
          if char:
            printable = printchar(char)
            await message.channel.send(printable)
          else:
            await message.channel.send("Character not found.")
        elif len(command) == 2:
          char = find_char(names[command[1].upper()])
          if char:
            printable = printchar(char)
            await message.channel.send(printable)
          else:
            await message.channel.send("Character not found.")
        else:
          await message.channel.send("Error - cannot parse command")

      case 'HP':
        print("HP case entered.")
        if len(command) == 1:
          char = find_char(id)
          if char:
            if char.thp > 0:
              await message.channel.send(f"THP - {char.thp}")
            await message.channel.send(f"HP - {char.hp} / {char.max_hp}")
          else:
            await message.channel.send("Character not found.")
        elif len(command) == 2:
          char = find_char(id)
          if char:
            hp_change = int(command[1])
            thp_blocked = False
            if char.thp > 0 and hp_change < 0:
              old_thp = char.thp
              if char.thp < -hp_change:
                hp_change += char.thp
                char.thp = 0
                await message.channel.send(f"THP - {old_thp} -> **0**")
              elif char.thp >= -hp_change:
                char.thp += hp_change
                save_char(char)
                await message.channel.send(f"THP - {old_thp} -> **{char.thp}**")
                thp_blocked = True
            if not thp_blocked:
              old_hp = char.hp
              char.hp += hp_change
              if char.hp > char.max_hp:
                char.hp = char.max_hp
              elif char.hp < 0:
                char.hp = 0
              save_char(char)
              await message.channel.send(f"HP - {old_hp}/{char.max_hp} -> "
              f"**{char.hp}/{char.max_hp}**")
          else:
            await message.channel.send("Character not found.")

      case 'THP':
        char = find_char(id)
        if len(command) == 1:
          if char:
            await message.channel.send(f"THP - {char.thp}")
          else:
            await message.channel.send("Character not found.")
        elif len(command) == 2:
          if char:
            old_thp = char.thp
            char.thp = int(command[1])
            save_char(char)
            await message.channel.send(f"THP - {old_thp} -> **{char.thp}**")
          else:
            await message.channel.send("Character not found.")

my_secret = os.environ['TOKEN']
client.run(my_secret)