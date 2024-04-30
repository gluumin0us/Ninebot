import os

import discord
from replit import db

from character import Character

"""
name = 0
level = 1
xp = 2
xp_til_next = 3
max_hp = 4
hp = 5     7
thp = 6    8
str = 7    0
dex = 8    1
cha = 9    2
int = 10   3
att = 11   4
wil = 12   5
luc = 13   6
tal = 14
effect = 15
ss = 16
pt = 17
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

felix_char = Character("Felix", 2, 20)
felix_char.legendary[5] += 1

jack_char = Character("Jack", 9, 1495)
jack_char.str = 12
jack_char.dex += 2
jack_char.att += 4
jack_char.legendary[4] += 2
jack_char.wil += 1
jack_char.legendary[5] += 1
jack_char.legendary[6] += 1
jack_char.tal.append("Vision's Necklace")
jack_char.tal.append("Wrapped Ribbon")
jack_char.tal.append("Dragon's Bane Armor")
jack_char.thp = 40

def convert_char_to_list(char: Character):
  return [char.name, char.level, char.xp, char.xp_til_next, 
          char.max_hp, char.hp, char.thp, char.str, char.dex, 
          char.cha, char.int, char.att, char.wil, char.luc, 
          char.tal, char.effect, char.ss, [char.pt1, char.pt2, 
          char.pt3, char.pt4], char.mod, char.legendary]

def printchar(char: list):
  printable = ""
  printable += (f"__{char[0]}: LV{char[1]}, {char[2]}/{char[3]}__\n")
  printable += (f"Strength - {char[7]}\n")
  printable += (f"Dexterity - {char[8]}\n")
  printable += (f"Charisma - {char[9]}\n")
  printable += (f"Intelligence - {char[10]}\n")
  printable += (f"Attack - {char[11]}\n")
  printable += (f"Willpower - {char[12]}\n")
  printable += (f"Luck - {char[13]}\n")
  if len(char[14]) > 0:
    for i in range(len(char[14])):
      printable += (f"*TAL{i} - {char[14][i]}*\n")
  printable += (f"HP - {char[5]}/{char[4]}\n")
  if char[6] > 0:
    printable += (f"THP - {char[6]}\n")
  return printable

db["359489732134305793"] = convert_char_to_list(jack_char)
db["531288319859097601"] = convert_char_to_list(felix_char)

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
  if message.content.startswith('$hello'):
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
            printable = printchar(db[id])
            await message.channel.send(printable)
          else:
            await message.channel.send("Character not found.")
        elif names[command[1].upper()] in db:
          printable = printchar(db[names[command[1].upper()]])
          await message.channel.send(printable)
        else:
          await message.channel.send("Character not found.")
        
my_secret = os.environ['TOKEN']
client.run(my_secret)

