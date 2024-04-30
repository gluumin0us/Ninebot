import os

import discord
from replit import db

from character import Character

"""
str dex cha int att wil luc
 0   1   2   3   4   5   6
"""

names = {
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

my_char = Character("Simon", 1, 0)
my_char.legendary[3] += 1
my_char.legendary[5] += 1

felix_char = Character("Felix", 2, 20)
felix_char.legendary[5] += 1

jack_char = Character("Jack", 9, 1495)
jack_char.legendary[4] += 2
jack_char.legendary[5] += 1
jack_char.legendary[6] += 1
jack_char.talisman("Vision's Necklace", 5, 1)
jack_char.talisman("Wrapped Ribbon", 1, 2)
jack_char.talisman("Dragon's Bane Armor", 4, 4)
jack_char.thp = 40
print(jack_char.stats)

def char_to_list(char: Character):
  return [char.name, char.level, char.xp, char.hp, char.thp, 
          char.tal, char.effect, char.ss, char.pt, char.mod, char.legendary]

def list_to_char(li_char: list):
  char = Character(li_char[0], li_char[1], li_char[2])
  char.hp = li_char[3]
  char.thp = li_char[4]
  char.tal = list(li_char[5])
  char.effect = list(li_char[6])
  char.ss = li_char[7]
  char.pt = list(li_char[8])
  char.mod = li_char[9]
  char.legendary = li_char[10]
  return char

def printchar(char: Character):
  printable = ""
  printable += (f"__{char.name}: LV{char.level}, {char.xp}/{char.xp_til_next}__\n")
  printable += (f"Strength - {char.stats[0]}\n")
  printable += (f"Dexterity - {char.stats[1]}\n")
  printable += (f"Charisma - {char.stats[2]}\n")
  printable += (f"Intelligence - {char.stats[3]}\n")
  printable += (f"Attack - {char.stats[4]}\n")
  printable += (f"Willpower - {char.stats[5]}\n")
  printable += (f"Luck - {char.stats[6]}\n")
  for i in range(len(char.tal)):
    printable += (f"*TAL{i+1} - {char.tal[i]}*\n")
  printable += (f"HP - {char.hp}/{char.max_hp}\n")
  if char.thp > 0:
    printable += (f"THP - {char.thp}\n")
  return printable

db["359489732134305793"] = char_to_list(jack_char)
db["531288319859097601"] = char_to_list(felix_char)
db["262320046653702145"] = char_to_list(my_char)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  id = str(message.author.id)
  msg = message.content
  if msg.startswith('9..hello'):
    await message.channel.send('Hello!')

  if msg.startswith('9..'):
    print("message detected.")
    command = msg.split('9..', 1)[1]
    if command == '':
      print("There is nothing")
    command = command.split()
    match command[0]:
      case 'char':
        print("character case entered.")
        if len(command) == 1:
          if id in db:
            printable = printchar(list_to_char(db[id]))
            await message.channel.send(printable)
          else:
            await message.channel.send("Character not found.")
        elif names[command[1].upper()] in db:
          printable = printchar(list_to_char(db[names[command[1].upper()]]))
          await message.channel.send(printable)
        else:
          await message.channel.send("Character not found.")
        
my_secret = os.environ['TOKEN']
client.run(my_secret)

