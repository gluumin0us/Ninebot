import os
import random
import requests
from time import sleep

import discord
from replit import db

from character import Character
import printer
import modify

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
"""
"""
jack_char = Character("Jack", 9, 1495)
jack_char.legendary[4] += 2
jack_char.legendary[5] += 1
jack_char.legendary[6] += 1
#jack_char.tal.append["Vision's Necklace", 5, 1, ""]
#jack_char.talisman("Wrapped Ribbon", 1, 2)
#jack_char.talisman("Dragon's Bane Armor", 4, 4)
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
  modify.restat(char)
  return char

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
  char_list = char_to_list(char)
  db[char.id] = char_list

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

greetings_back = ["Hello!", "Hi!", "Good to see you!", "Howdy!"]
affection_back = ["I'm honored?", "Uhm... who are you again?", 
                  "I'm glad?", "Uh- Thanks!", "Thank you?"]
hatred_back = ["Aw, what? Why?", ":(", "Well I uh, I hate you too!"]

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await client.change_presence(activity=discord.Game('9..help'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  id = str(message.author.id)
  requester = (message.author.display_name, str(message.author.display_avatar))
  original_msg = message.content
  msg = message.content.upper()
      
  if msg.startswith('9..HELLO') or "HI NINE" in msg or "HELLO NINE" in msg:
    await message.channel.send(random.choice(greetings_back))

  if ("I LOVE" in msg or "ILY" in msg) and "NINE" in msg:
    if id == names['MIKEY']:
      await message.channel.send("I love you too Mikey!")
    else:
      await message.channel.send(random.choice(affection_back))

  if"I HATE" in msg and "NINE" in msg:
    await message.channel.send(random.choice(hatred_back))

  if ("THANKS" in msg or "THANK YOU" in msg) and "NINE" in msg:
    await message.channel.send("You're welcome!")

  if "TELL" in msg and "JOKE" in msg and "NINE" in msg:
    response = requests.get('https://v2.jokeapi.dev/joke/Pun')
    json_data = response.json()
    if json_data["type"] == "single":
      await message.channel.send(json_data["joke"])
    elif json_data['type'] == 'twopart':
      await message.channel.send(json_data['setup'])
      sleep(2)
      await message.channel.send(json_data['delivery'])

  # Most methods of Ninebot starts with 9..
  if msg.startswith('9..'):
    original_command = original_msg.split('9..', 1)[1]
    original_command = original_command.split()
    command = msg.split('9..', 1)[1]
    if command == '':
      print("What's your command?")
    command = command.split()
    if len(command) > 1 and command[-2] == '-T':
      id = names[command[-1]]
      command.pop()
      command.pop()
    char = find_char(id)
    if char:
      match command[0]:

        case 'TEST':
          embedVar = printer.test_embed(requester)
          await message.channel.send(embed=embedVar)
      
        # Prints out helpful information
        case 'HELP':
          printable = ""
          if len(command) == 1:
            printable = printer.printhelp("MAIN", requester)
            await message.channel.send(embed=printable)
          elif len(command) == 2:
            printable = printer.printhelp(command[1], requester)
            await message.channel.send(embed=printable)
        
        # Tells a joke
        case 'JOKE':
          response = requests.get('https://v2.jokeapi.dev/joke/Miscellaneous,Pun?blacklistFlags=racist')
          json_data = response.json()
          if json_data['type'] == "single":
            await message.channel.send(json_data["joke"])
          elif json_data['type'] == 'twopart':
            await message.channel.send(json_data['setup'])
            sleep(2)
            await message.channel.send(json_data['delivery'])

        # Prints out character information
        case 'CHAR':
          if len(command) == 1:
            printable = printer.printchar(char)
            await message.channel.send(printable)

        # Prints out, or modifies HP
        case 'HP':
          print("HP case entered.")
          if len(command) == 1:
            if char.thp > 0:
              await message.channel.send(f"THP - {char.thp}")
            await message.channel.send(f"HP - {char.hp} / {char.max_hp}")
          elif len(command) == 2:
            hp_change = 500 if command[1] == "FULL" else int(command[1])
            printable = modify.modhp(char, hp_change)
            save_char(char)
            await message.channel.send(printable)
            
        # Prints out, or modifies THP
        case 'THP':
          if len(command) == 1:
            await message.channel.send(f"THP - {char.thp}")
          elif len(command) == 2:
            old_thp = char.thp
            char.thp += int(command[1])
            if char.thp < 0:
              char.thp = 0
            save_char(char)
            await message.channel.send(f"THP - {old_thp} -> **{char.thp}**")

        # Rolls a d20, and optionally adds stats
        case 'ROLL':
          result = random.randint(1, 20)
          if len(command) == 1:
            await message.channel.send (f"Rolling a d20... **-{result}-**")
            if result == 20:
              await message.channel.send("**Natural 20!**")
          elif len(command) == 2:
            printable = printer.printroll(char, result, command[1])
            await message.channel.send(printable)
            if result == 20:
              legendary = random.randint(1, 10)
              await message.channel.send("Rolling for legendaries...")
              sleep(0.5)
              await message.channel.send(":drum: :drum: :drum: ")
              sleep(2)
              if legendary == 10:
                await message.channel.send("**10!**\n **LEGENDARY!!!**")
              else:
                await message.channel.send(f"{legendary}\nBetter luck next time!")

        # Prints out, or modifies XP
        case 'XP':
          if len(command) == 1:
            await message.channel.send(f"XP - {char.xp}/{240 * char.level - 100}")
          elif len(command) == 2:
            xp_change = int(command[1])
            printable = modify.modxp(char, xp_change)
            save_char(char)
            await message.channel.send(printable)

      # Prints out current level and XP
        case 'LEVEL':
          if len(command) == 1:
            await message.channel.send(f"Level - LV{char.level}, "
                                       f"{char.xp}/{240 * char.level - 100}")

        case 'LEGEND':
          if len(command) == 1:
            printable = printer.printleg(char)
            await message.channel.send(printable)
          elif len(command) == 3:
            printable = modify.modleg(char, command[1], int(command[2]))
            save_char(char)
            await message.channel.send(printable)

        case 'TAL':
          if len(command) == 1:
            printable = printer.printtal(char)
            await message.channel.send(printable)
          else:
            action = command[1]
            if action == 'ADD':
              action = command[1]
              # handing multi-word names
              tal_name = original_command.pop(2)
              while original_command[2].upper() not in modify.stat_to_int:
                tal_name += f" {original_command.pop(2)}"

              # handing description
              tal_desc = ""
              for i in range(4, len(original_command)):
                if original_command[i].upper() not in modify.stat_to_int and \
                not original_command[i].startswith('+') and \
                not original_command[i].startswith('-'):
                  tal_desc += f"{original_command[i]} "

              tal_stat = []
              tal_mod = []
              for i in range(len(command)):
                if command[i] in modify.stat_to_int:
                  tal_stat.append(command[i])
                  tal_mod.append(int(command[i+1]))
              
              tal = [tal_name, tal_stat, tal_mod, tal_desc]

              printable = modify.modtal(char, action, tal)
            elif action == 'RM':
              printable = modify.modtal(char, action, int(command[2]))
            save_char(char)
            await message.channel.send(printable)
          

my_secret = os.environ['TOKEN']
client.run(my_secret)