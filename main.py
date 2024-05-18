import os
import random
import requests
from time import sleep

import discord
from discord import app_commands
from replit import db

from character import Character
import printer
import modify

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

admins = ["531288319859097601", "262320046653702145"]
db["ADMINS"] = admins


# my_char = Character("Simon", 1, 0)
# my_char.legendary[3] += 1
# my_char.legendary[5] += 1
# my_char.id = "262320046653702145"

# felix_char = Character("Felix", 2, 20)
# felix_char.legendary[5] += 1
# felix_char.id = names["FELIX"]

# mike_char = Character("Michael", 3, 164)
# mike_char.legendary = [1, 0, 1, 0, 1, 2, 0]
# mike_char.id = names["MIKEY"]


# jack_char = Character("Jack", 9, 1495)
# jack_char.legendary[4] += 2
# jack_char.legendary[5] += 1
# jack_char.legendary[6] += 1
# #jack_char.tal.append["Vision's Necklace", 5, 1, ""]
# #jack_char.talisman("Wrapped Ribbon", 1, 2)
# #jack_char.talisman("Dragon's Bane Armor", 4, 4)
# jack_char.thp = 40
# jack_char.id = names["JACK"]


def char_to_list(char: Character):
  # Converts a Character object to a list for storage
  return [char.name, char.level, char.xp, char.hp, char.thp, 
          char.tal, char.aff, char.rep, char.pt, char.mod, char.legendary, 
          char.id, char.update_message]

def list_to_char(li_char: list):
  # Converts a character from a list to a Character object
  char = Character(li_char[0], li_char[1], li_char[2])
  char.hp = li_char[3]
  char.thp = li_char[4]
  char.tal = list(li_char[5])
  char.aff = list(li_char[6])
  char.rep = li_char[7]
  char.pt = list(li_char[8])
  char.mod = li_char[9]
  char.legendary = li_char[10]
  char.id = li_char[11]
  char.update_message = li_char[12]
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

async def save_char(char: Character):
  # Saves a character's changes to the database,
  # Assuming there's already a copy there.
  char_list = char_to_list(char)
  db[char.id] = char_list
  deleted_messages = []
  if char.id not in db['linked_csh']:
    db['linked_csh'][char.id] = []
  links = db['linked_csh'][char.id]
  for link in links:
    channel_id, message_id = link
    channel_to_edit = client.get_channel(channel_id)
    try:
      message_to_edit = await channel_to_edit.fetch_message(message_id)
      printable = ":link: "
      printable += "\n".join(printer.printchar(char))
      await message_to_edit.edit(content=printable)
      print("Message updated!")
    except:
      pass
      
def check_csh(msg: str):
  if msg.startswith("__"):
    msg = msg.split('__', 1)[1]
    msg = msg.split(':', 1)[0].upper()
    if msg in db['name2id']:
      return db['name2id'][msg]
  return False

# RUN ONE TIME COMMANDS HERE



############################

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await client.change_presence(activity=discord.Game('9..help'))

@client.event
async def on_guild_join(guild):
  for channel in guild.channels:
    if "the-streets" == channel.name:
      await channel.send("Hello! I'm Nine, glad to be here!\n")
      break

@client.event
async def on_raw_message_delete(payload):
  print("Message deleted.")
  for cur_char in db['linked_csh']:
    links = db['linked_csh'][cur_char]
    for link in links:
      channel_id, message_id = link
      if message_id == payload.message_id:
        db['linked_csh'][cur_char].remove(link)
        await client.get_channel(payload.channel_id).send("Linked CSH deleted.")
        break
  

@client.event
async def on_raw_reaction_add(payload):
  rtn_name = str(payload.emoji.name)
  channel = client.get_channel(payload.channel_id)
  msg = await channel.fetch_message(payload.message_id)
  print(f"Reaction detected: {rtn_name}")
  match rtn_name:
    case '🔗':
      print("case LINK entered.")
      msg_content = msg.content
      id = check_csh(msg_content)
      print(f"ID: {id}")
      if id:
        if id not in db['linked_csh']:
          db['linked_csh'][id] = []
        db['linked_csh'][id].append((payload.channel_id, payload.message_id))
        await msg.remove_reaction(payload.emoji, payload.member)
        await save_char(find_char(id))
        
    case '❌':
      print("case X entered.")
      msg_content = msg.content
      if msg_content.startswith(':link: '):
        msg_content = msg_content.split(':link: ', 1)[1]
        id = check_csh(msg_content)
        print(f"ID: {id}")
        if id in db['linked_csh']:
          for i in range(len(db['linked_csh'][id])):
            channel_id, message_id = db['linked_csh'][id][i]
            if message_id == payload.message_id:
              db['linked_csh'][id].pop(i)
              await msg.edit(content=msg_content)
              break
          await msg.remove_reaction(payload.emoji, payload.member)
      

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  id = str(message.author.id)
  channel_id = message.channel.id
  requester = (message.author.display_name, str(message.author.display_avatar))
  original_msg = message.content
  msg = message.content.upper()
      
  if msg.startswith('9..HELLO') or "HI NINE" in msg or "HELLO NINE" in msg:
    await message.channel.send(random.choice(printer.greetings_back))

  if ("I LOVE" in msg or "ILY" in msg) and "NINE" in msg:
    if id == names['MIKEY']:
      await message.channel.send("I love you too Mikey!")
    else:
      await message.channel.send(random.choice(printer.affection_back))

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
    if len(original_command) > 1 and original_command[-2].upper() == '-T':
      original_command.pop()
      original_command.pop()
    command = msg.split('9..', 1)[1]
    if command == '':
      print("What's your command?")
    command = command.split()
    if len(command) > 1 and command[-2] == '-T':
      id = db["name2id"][command[-1]]
      command.pop()
      command.pop()
    char = find_char(id)
    if command[0] == 'REGISTER' or command[0] == 'HELP':
      char = True
    if char:
      match command[0]:
      
        # Prints out helpful information
        case 'HELP':
          await message.delete()
          printable = ""
          if len(command) == 1:
            printable = printer.printhelp("MAIN", requester)
            await message.author.send(embed=printable)
          elif len(command) == 2:
            printable = printer.printhelp(command[1], requester)
            await message.author.send(embed=printable)
        
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
            printable = "\n".join(printer.printchar(char))
            await message.channel.send(printable)

        # Prints out, or modifies HP
        case 'HP':
          if len(command) == 1:
            printable = ""
            if char.thp > 0:
              printable += f"THP - {char.thp}\n"
            await message.reply(printable + f"HP - {char.hp} / {char.max_hp}")
          elif len(command) == 2:
            hp_change = 500 if command[1] == "FULL" else int(command[1])
            printable = modify.modhp(char, hp_change)
            await save_char(char)
            await message.reply(printable)
            
        # Prints out, or modifies THP
        case 'THP':
          if len(command) == 1:
            await message.reply(f"THP - {char.thp}")
          elif len(command) == 2:
            old_thp = char.thp
            char.thp += int(command[1])
            if char.thp < 0:
              char.thp = 0
            await save_char(char)
            await message.reply(f"THP - {old_thp} -> **{char.thp}**")

        # Rolls a d20, and optionally adds stats
        case 'ROLL':
          result = random.randint(1, 20)
          if len(command) == 1:
            await message.reply (f"Rolling a d20... **-{result}-**")
            if result == 20:
              await message.channel.send("**Natural 20!**")
          elif len(command) == 2:
            printable = printer.printroll(char, result, command[1])
            await message.reply(printable)
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
            await message.reply(f"XP - {char.xp}/{240 * char.level - 100}")
          elif len(command) == 2:
            xp_change = int(command[1])
            printable = modify.modxp(char, xp_change)
            await save_char(char)
            await message.reply(printable)

        # Prints out current level and XP
        case 'LEVEL': 
          if len(command) == 1:
            await message.reply(f"Level - LV{char.level}, "
                                       f"{char.xp}/{240 * char.level - 100}")
          if len(command) == 3 and command[1] == "SET":
            printable = f"Level - LV{char.level} -> **LV{command[2]}**, "\
            f"{char.xp}/{240*char.level-100} -> **0/{240*int(command[2])-100}**"
            old_level = char.level
            char.level = int(command[2])
            char.xp = 0
            modify.restat(char)
            if old_level != char.level:
              char.hp = char.max_hp
            await save_char(char)
            await message.reply(printable)

        # Prints out, or modifies legendary bonuses
        case 'LEGEND':
          if len(command) == 1:
            printable = printer.printleg(char)
            await message.reply(printable)
          elif len(command) == 3:
            printable = modify.modleg(char, command[1], int(command[2]))
            await save_char(char)
            await message.reply(printable)

        # Prints out, adds, or removes talismans
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
            await save_char(char)
            await message.reply(printable)

        # Prints out, adds, or removes afflictions
        case 'AFF':
          if len(command) == 1:
            printable = printer.printaff(char)
            await message.channel.send(printable)
          else:
            action = command[1]
            if action == 'ADD':
              aff_name = command[2]
              aff_tier = 0
              if command[3].isdigit():
                aff_tier = int(command.pop(3))
                original_command.pop(3)
              
              i = 0;
              aff_stat = []
              aff_mod = []
              if len(command) > 3:
                while command[3] in modify.stat_to_int:
                  aff_stat.append(command.pop(3))
                  aff_mod.append(int(command.pop(3)))
                  original_command.pop(i)
                  original_command.pop(i)
                  if len(command) < 4:
                    break
                  
              aff_desc = ""
              for i in range(3, len(original_command)):
                aff_desc += f"{original_command[i]} "

              aff = [aff_name, aff_tier, aff_stat, aff_mod, aff_desc]
              printable = modify.modaff(char, action, aff)
              
            elif action == 'RM':
              printable = modify.modaff(char, action, command[2])
            await save_char(char)
            await message.channel.send(printable)

        # Registers a new character if one does not exist
        case 'REGISTER':
          if id in db:
            await message.channel.send("You already have a character!")
          elif len(command) == 1:
            await message.channel.send("You need to input a name!\n "\
            "e.g. 9..register Felix")
          elif len(command) == 2:
            new_name = command[1]
            new_char = Character(new_name.capitalize(), 1, 0)
            new_char.id = id
            modify.restat(new_char)
            db["name2id"][new_name] = id
            db[id] = char_to_list(new_char)
            char_cache[id] = new_char
            await message.channel.send("New character registered!\n"\
              f"Welcome to the Magic Casino, {new_name.capitalize()}!")

        # Unregisters an existing character.
        case 'UNREGISTER':
          if len(command) == 1:
            db.pop(id)
            rm_char = char_cache.pop(id)
            await message.channel.send(f"Character unregistered: {rm_char.name}")

        # Ticks forward certain effects like bleeding
        case 'TICK':
          if len(command) == 1:
            printable = modify.tick(char)
            await save_char(char)
            await message.channel.send(printable)

        # Prints out a list of admins (WIP)
        case 'ADMIN':
          if len(command) == 1:
            printable = "Current Admins:\n"
            for member_id in db['ADMINS']:
              member = await client.fetch_user(int(member_id))
              printable += f"{member.display_name}\t"
            await message.channel.send(printable)

        # Takes in a user ID to output the tul commands to copy them
        case 'CLONE':
          if len(command) == 2:
            clone_id = int(command[1])
            clone = await client.fetch_user(int(clone_id))
            clone_name = clone.display_name
            clone_avatar = str(clone.avatar)
            await message.channel.send(
              f"`tul!register '{clone_name}' text>>{clone_name}`"
            )
            await message.channel.send(
              f"`tul!avatar '{clone_name}' {clone_avatar}`"
            )

        # Prints out, or modifies reputation.
        case 'REP':
          if len(command) == 1:
            printable = f"Current Rep for {char.name}: {char.rep}\n"
            if char.rep <= 0:
              printable += "**DEADBEAT**"
          elif len(command) == 2:
            printable = f"Rep for {char.name}: {char.rep} -> "
            char.rep += int(command[1])
            printable += f"**{char.rep}**\n"
            if char.rep <= 0:
              printable += "**DEADBEAT**"
            await save_char(char)
          elif len(command) == 3 and command[1] == 'SET':
            printable = f"Rep for {char.name}: {char.rep} -> "
            char.rep = int(command[2])
            printable += f"**{char.rep}**\n"
            await save_char(char)
          await message.channel.send(printable)

        # Makes, or resets linked CSHs for all characters.
        case 'ALL-LEVELS':
          if len(command) == 1:
            print("all levels case entered")
            not_first = False
            for cur_char_name in db["name2id"]:
              cur_id = db["name2id"][cur_char_name]
              cur_char = find_char(cur_id)
              if cur_char:
                printable = ":link:  "
                printable += "\n".join(printer.printchar(cur_char))
                if not_first:
                  await message.channel.send("​")
                msg = await message.channel.send(printable)
                not_first = True
                channel_id = message.channel.id
                cur_char.update_message.append((channel_id, msg.id))
                if cur_id not in db['linked_csh']:
                  db['linked_csh'][cur_id] = []
                db['linked_csh'][cur_id].append((channel_id, msg.id))
                await save_char(cur_char)
          elif len(command) == 2 and command[1] == 'RESET':
            for cur_char in db["linked_csh"]:
              db['linked_csh'][cur_char] = []
            await message.channel.send("Update Messages reset.")
          elif len(command) == 3 and command[1] == 'ADD':
            print(f"Add case entered, adding {command[2]}")
            cur_id = db["name2id"][command[2]]
            cur_char = find_char(cur_id)
            if cur_char:
              printable = ":link: "
              printable += "\n".join(printer.printchar(cur_char))
              msg = await message.channel.send(printable)
              channel_id = message.channel.id
              cur_char.update_message.append((channel_id, msg.id))
              if cur_id not in db['linked_csh']:
                db['linked_csh'][cur_id] = []
              db['linked_csh'][cur_id].append((channel_id, msg.id))
              await save_char(cur_char)

        # Shows the data stored in the database.
        case 'DB':
          if len(command) == 1:
            printable = ""
            for key in db.keys():
              printable += f"{key}\t"
            await message.channel.send(printable)
          elif len(command) == 2:
            key = command[1].lower()
            if key in db:
              printable = db[key]
              await message.channel.send(printable)
            
            
    else:
      await message.channel.send("You don't have a character yet! "\
                                 "Make one with `9..register`, or check out "\
                                 "`9..help` for more info!")
      
my_secret = os.environ['TOKEN']
client.run(my_secret)