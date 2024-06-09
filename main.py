import os
import random
import requests
import re
from time import sleep, time
from datetime import datetime

import discord
from discord import app_commands
from replit import db

from character import Character
import printer
import modify
import spells

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

ARCHIVE_ID = 1241883869549170748
GM_ID = 262320046653702145

CHECKBOOK_ID = (797199351515447296, 1245834122232860702)


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
          char.id, char.counter]

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
  char.counter = li_char[12]
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
    except:
      pass

async def update_rep():
  check_channel_id, check_msg_id = CHECKBOOK_ID
  check_channel = client.get_channel(check_channel_id)
  try:
    check_message = check_channel.get_partial_message(check_msg_id)
    printable = printer.printcheck(db['checkbook'])
    await check_message.edit(content=printable)
  except:
    pass

async def wrong_command(channel):
  await channel.send("I'm not sure if I understand your command. "\
                    "Check `9..help` for more information.")
      
def check_csh(msg: str):
  if msg.startswith("__"):
    msg = msg.split('__', 1)[1]
    msg = msg.split(':', 1)[0].upper()
    if msg in db['name2id']:
      return db['name2id'][msg]
  return False


def is_me(msg):
  return msg.author == client.user

async def parse_command(id, channel, requester, msg):
  # preparing the original message command
  original_id = id
  original_command = msg.split('9..', 1)[1]
  original_command = original_command.split()
  if len(original_command) > 1 and original_command[-2].upper() == '-T':
    original_command.pop()
    original_command.pop()

  # preparing the command
  command = msg.upper().split('9..', 1)[1]
  if command == '':
    print("What's your command?")
  command = command.split()
  reply = True

  macros = {}
  try:
    macros = db['macros'][id]
  except:
    pass
  if command[0] in macros:
    # cascading specifiers
    specifier = ""
    has_specifier = True
    while has_specifier:
      has_specifier = False
      if len(command) > 1 and command[-1] == '-S':
        has_specifier = True
        specifier += f" {command.pop(-1)}"
      if len(command) > 2 and command[-2] == '-T':
        has_specifier = True
        specifier += f" {command.pop(-2)} {command.pop(-1)}"
    len_cmd = len(command)

    output = {}
    # iterating through macro commands
    for macro_cmd in macros[command[0]]:

      # getting outputs
      has_output = False
      if "->" in macro_cmd:
        split_cmd = re.split("->\s*", macro_cmd, 1)
        macro_cmd = split_cmd[0]
        has_output = split_cmd[1]
      
      # replacing arguments
      args = re.findall("arg[0-9]+", macro_cmd)
      for arg in args:
        arg_pos = int(arg.split("arg")[1])
        if arg_pos >= len_cmd or command[arg_pos] == 'NULL':
          macro_cmd = re.sub(arg, "", macro_cmd)
        else:
          macro_cmd = re.sub(arg, command[arg_pos].capitalize(), macro_cmd)

      # replacing outputs
      print(output)
      for out_name in output:
        if out_name in macro_cmd:
          if output[out_name] is None:
            macro_cmd = re.sub(out_name, "", macro_cmd)
          else:
            macro_cmd = re.sub(out_name, f" {output[out_name]}", macro_cmd)

      # replacing python evals
      while re.search("<py>", macro_cmd):
        py_cmd = macro_cmd.split("<py>", 1)[1].split("</py>", 1)[0]
        py_result = eval(py_cmd)
        macro_cmd = re.sub("<py>.*</py>", str(py_result), macro_cmd, 1)
          
      # calling subcommands
      macro_cmd = f"{macro_cmd}{specifier}"
      if has_output:
        output[has_output] = await parse_command(id, channel, requester, macro_cmd)
      else:
        await parse_command(id, channel, requester, macro_cmd)
    return

  # Parsing targeting
  if len(command) > 1 and command[0] == 'MACRO' and command[1] == 'ADD':
    command = msg.upper().split('9..', 1)[1].split('\n- ')[0].split()
  has_specifier = True
  while has_specifier:
    has_specifier = False
    if len(command) > 1 and command[-1] == '-S':
      reply = False
      has_specifier = True
      command.pop()
    if len(command) > 2 and command[-2] == '-T':
      has_specifier = True
      name2id = db['name2id']
      found_name = False
      for name in name2id:
        if name.startswith(command[-1]):
          id = name2id[name]
          found_name = True
          break
      command.pop()
      command.pop()
      if not found_name:
        await channel.send("Error: target name not found.\n")
        return
  char = find_char(id)
  if command[0] in ['REGISTER', 'HELP', 'DM']:
    char = True
  if char:
    
    match command[0]:

      # Prints out helpful information
      case 'HELP':
        printable = ""
        if len(command) == 1:
          printable = printer.printhelp("MAIN", requester)
          await channel.send(embed=printable)
        elif len(command) == 2:
          printable = printer.printhelp(command[1], requester)
          await channel.send(embed=printable)
        else:
          await wrong_command(channel)

      # Tells a joke
      case 'JOKE':
        response = requests.get('https://v2.jokeapi.dev/joke/Miscellaneous,Pun?blacklistFlags=racist')
        json_data = response.json()
        if json_data['type'] == "single":
          await channel.send(json_data["joke"])
        elif json_data['type'] == 'twopart':
          await channel.send(json_data['setup'])
          sleep(2)
          await channel.send(json_data['delivery'])

      # Prints out character information
      case 'CHAR':
        if len(command) == 1:
          printable = "\n".join(printer.printchar(char))
          if reply:
            await channel.send(printable)
        else:
          await wrong_command(channel)
        return char.name

      # Prints out, or modifies HP
      case 'HP':
        if len(command) == 1:
          printable = printer.printhp(char)
          if reply:
            await channel.send(printable)
        elif len(command) == 2:
          hp_change = 500 if command[1] == "FULL" else int(command[1])
          printable = modify.modhp(char, hp_change)
          await save_char(char)
          if reply:
            await channel.send(printable)
        elif len(command) == 3 and command[1] == 'SET':
          hp_change = int(command[2]) - char.hp
          printable = modify.modhp(char, hp_change)
          await save_char(char)
          if reply:
            await channel.send(printable)
        else:
          await wrong_command(channel)
          return
        return char.hp

      # Prints out, or modifies THP
      case 'THP':
        if len(command) == 1:
          if reply:
            await channel.send(f"THP - {char.thp}")
        elif len(command) == 2:
          old_thp = char.thp
          char.thp += int(command[1])
          if char.thp < 0:
            char.thp = 0
          await save_char(char)
          if reply:
            await channel.send(f"THP - {old_thp} -> **{char.thp}**")
        elif len(command) == 3 and command[1] == 'SET':
          old_thp = char.thp
          char.thp = int(command[2])
          if char.thp < 0:
            char.thp = 0
          await save_char(char)
          if reply:
            await channel.send(f"THP - {old_thp} -> **{char.thp}**")
        else:
          await wrong_command(channel)
          return
        return char.thp

      # Rolls a d20, and optionally adds stats
      case 'ROLL':
        result = random.randint(1, 20)
        if len(command) == 1:
          printable = f"Rolling a d20... **-{result}-**\n"
          if result == 20:
            printable += "**Natural 20!**"
          if reply:
            await channel.send(printable)
          return result
          
        elif len(command) == 2:
          return_result = printer.printroll(char, result, command[1])
          printable = return_result[0]
          if reply:
            await channel.send(printable)
            if result == 20:
              legendary = random.randint(1, 10)
              if reply:
                await channel.send("Rolling for legendaries...")
              sleep(0.5)
              if reply:
                await channel.send(":drum: :drum: :drum: ")
              sleep(2)
              if legendary == 10:
                if reply:
                  await channel.send("**10!**\n **LEGENDARY!!!**")
              else:
                if reply:
                  await channel.send(f"{legendary}\nBetter luck next time!")
          return return_result[1]
        else:
          await wrong_command(channel)
          return

      # Prints out, or modifies XP
      case 'XP':
        if len(command) == 1:
          printable = printer.printxp(char)
          xp_til_next = 240 * char.level - 100
          printable += f"LV {char.level}, {char.xp}/{xp_til_next}"
          if reply:
            await channel.send(printable)
        elif len(command) == 2:
          try:
            xp_change = int(command[1])
            printable = modify.modxp(char, xp_change)
            await save_char(char)
            if reply:
              await channel.send(f"{printer.printxp(char)}{printable}")
          except:
            await wrong_command(channel)
            return
        else:
          await wrong_command(channel)
          return
        return char.xp

      # Prints out current level and XP
      case 'LEVEL': 
        if len(command) == 1:
          printable = printer.printxp(char)
          xp_til_next = 240 * char.level - 100
          printable += f"LV {char.level}, {char.xp}/{xp_til_next}"
          if reply:
            await channel.send(printable)
        if len(command) == 3 and command[1] == "SET":
          printable = f"LV{char.level}, {char.xp}/{240*char.level-100} -> "\
          f"**LV{command[2]}**, **0/{240*int(command[2])-100}**"
          old_level = char.level
          char.level = int(command[2])
          char.xp = 0
          modify.restat(char)
          if old_level != char.level:
            char.hp = char.max_hp
          await save_char(char)
          if reply:
            await channel.send(f"{printer.printxp(char)}{printable}")
        else:
          await wrong_command(channel)
          return
        return char.level

      # Prints out, or modifies legendary bonuses
      case 'LEGEND':
        printable = ""
        if len(command) == 1:
          printable = printer.printleg(char)
        elif len(command) == 3:
          try:
            printable = modify.modleg(char, command[1], int(command[2]))
            await save_char(char)
          except:
            await wrong_command(channel)
            return
        else:
          await wrong_command(channel)
          return
        if reply:
          await channel.send(printable)

      # Prints out, adds, or removes talismans
      case 'TAL':
        printable = ""
        if len(command) == 1:
          printable = printer.printtal(char)
          if reply:
            await channel.send(printable)
        else:
          action = command[1]
          if action == 'ADD':
            try:
              tal_desc = ""
              if '\n' in msg:
                tal_desc = msg.split('\n', 1)[1]
              # handing multi-word names
              tal_name = original_command.pop(2)
              command.pop(2)
              while (len(original_command) >= 3 and 
                     original_command[2].upper() not in modify.stat_to_int and 
                    not tal_desc.startswith(original_command[2])):
                tal_name += f" {original_command.pop(2)}"
                command.pop(2)

              # handling stat modifications
              tal_stat = []
              tal_mod = []
              for i in range(len(command)):
                if command[i] in modify.stat_to_int:
                  tal_stat.append(command[i])
                  tal_mod.append(int(command[i+1]))

              tal = [tal_name, tal_stat, tal_mod, tal_desc]

              printable = modify.modtal(char, action, tal)
            except:
              await wrong_command(channel)
              return
          # Removing a talisman
          elif action == 'RM':
            try:
              command.pop(0)
              command.pop(0)
              command = " ".join(command)
              printable = modify.modtal(char, action, command)
            except:
              await wrong_command(channel)
              return
          else:
            await wrong_command(channel)
            return
          await save_char(char)
          if reply:
            await channel.send(printable)

      # Prints out, adds, or removes afflictions
      case 'AFF':
        printable = ""
        if len(command) == 1:
          printable = printer.printaff(char)
          
        else:
          action = command[1]
          if action == 'ADD':
            try:
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
            except:
              await wrong_message(channel)
              return

          elif action == 'RM':
            try:
              printable = modify.modaff(char, action, command[2])
            except:
              await wrong_message(channel)
              return

          else:
            await wrong_message(channel)
            return
          await save_char(char)
        if reply:
          await channel.send(printable)

      # Registers a new character if one does not exist
      case 'REGISTER':
        if id in db:
          await channel.send("You already have a character!")
          return
        elif len(command) == 1:
          await channel.send("You need to input a name!\n "\
          "e.g. 9..register Felix")
          return
        elif len(command) == 2:
          new_name = command[1]
          if new_name in db["name2id"]:
            await channel.send(f"Name \"{new_name}\" already taken!\n")
            return
          new_char = Character(new_name.capitalize(), 1, 0)
          new_char.id = id
          modify.restat(new_char)
          db["name2id"][new_name] = id
          db["id2name"][id] = new_name
          db["checkbook"][new_name.capitalize()] = 13
          await update_rep()
          db[id] = char_to_list(new_char)
          char_cache[id] = new_char
          if reply:
            await channel.send("New character registered!\n"\
            f"Welcome to the Magic Casino, {new_name.capitalize()}!", 
                          )
        elif len(command) > 2:
          command = command.pop(0)
          new_char = modify.makechar(command)

      # Unregisters an existing character.
      case 'UNREGISTER':
        if len(command) == 1:
          db.pop(id)
          rm_char = char_cache.pop(id)
          if reply:
            await channel.send(f"Character unregistered: {rm_char.name}")

      # Ticks forward certain effects like bleeding
      case 'TICK':
        if len(command) == 1:
          printable = modify.tick(char)
          await save_char(char)
          if reply:
            await channel.send(printable)

      # Prints out a list of admins (WIP)
      case 'ADMIN':
        if len(command) == 1:
          printable = "Current Admins:\n"
          for member_id in db['ADMINS']:
            member = await client.fetch_user(int(member_id))
            printable += f"{member.display_name}\t"
          if reply:
            await channel.send(printable)

      # Takes in a user ID to output the tul commands to copy them
      case 'CLONE':
        if len(command) == 2:
          clone_id = int(command[1])
          clone = await client.fetch_user(int(clone_id))
          clone_name = clone.display_name
          clone_avatar = str(clone.avatar)
          await channel.send(
            f"`tul!register '{clone_name}' text>>{clone_name}`"
          )
          await channel.send(
            f"`tul!avatar '{clone_name}' {clone_avatar}`"
          )

      # Prints out, or modifies reputation.
      case 'REP':
        if len(command) == 1:
          try:
            printable = f"Current Rep for {char.name}: "\
            f"{db['checkbook'][char.name]}\n"
            if char.rep <= 0:
              printable += "**DEADBEAT**"
          except:
            return
        elif len(command) == 2:
          printable = f"Rep for {char.name}: {db['checkbook'][char.name]} -> "
          db['checkbook'][char.name] += int(command[1])
          printable += f"**{db['checkbook'][char.name]}**\n"
          if db['checkbook'][char.name] <= 0:
            printable += "**DEADBEAT**"
          await update_rep()

        elif len(command) == 3 and command[1] == 'SET':
          printable = f"Rep for {char.name}: {db['checkbook'][char.name]} -> "
          db['checkbook'][char.name] = int(command[2])
          printable += f"**{db['checkbook'][char.name]}**\n"
          if db['checkbook'][char.name] <= 0:
            printable += "**DEADBEAT**"
          await update_rep()
        if reply:
          await channel.send(printable)
        return db['checkbook'][char.name]

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
                await channel.send("​")
              msg = await channel.send(printable)
              not_first = True
              cur_char.update_message.append((channel.id, msg.id))
              if cur_id not in db['linked_csh']:
                db['linked_csh'][cur_id] = []
              db['linked_csh'][cur_id].append((channel.id, msg.id))
              await save_char(cur_char)
        elif len(command) == 2 and command[1] == 'RESET':
          for cur_char in db["linked_csh"]:
            db['linked_csh'][cur_char] = []
          await channel.send("Update Messages reset.")
        elif len(command) == 3 and command[1] == 'ADD':
          print(f"Add case entered, adding {command[2]}")
          cur_id = db["name2id"][command[2]]
          cur_char = find_char(cur_id)
          if cur_char:
            printable = ":link: "
            printable += "\n".join(printer.printchar(cur_char))
            msg = await channel.send(printable)
            cur_char.update_message.append((channel.id, msg.id))
            if cur_id not in db['linked_csh']:
              db['linked_csh'][cur_id] = []
            db['linked_csh'][cur_id].append((channel.id, msg.id))
            await save_char(cur_char)

      # Shows the data stored in the database.
      case 'DB':
        if len(command) == 1:
          printable = ""
          for key in db.keys():
            printable += f"{key}\t"
          await channel.send(printable, suppress_embeds=True)
        elif len(command) == 2:
          key = command[1].lower()
          if key in db:
            printable = db[key]
            await channel.send(printable, suppress_embeds=True)

      # Sends someone a DM via Nine.
      case 'DM':
        if len(command) > 1:
          user = await client.fetch_user(int(id))
          original_command.pop(0)
          printable = " ".join(original_command)
          await user.send(content=printable)

      case 'CAST':
        if len(command) == 2:
          printable = ""
          for i in range(len(spells.spell_root)):
            if command[1] == spells.spell_root[i]:
              printable += f"{message.author.display_name} is casting "\
              f"{spells.spell_name[i]}!\n\"{spells.spell_incantation[i]}\""
              break
          await channel.send(printable)

      case 'PURGE':
        if len(command) == 1:
          await channel.send("How many messages would you like to purge?\n", 
                    )
        elif len(command) == 2:
          try:
            limit = int(command[1])
            await channel.purge(limit=limit, check=is_me, bulk=False)
          except:
            await wrong_command(channel)

      case 'LOCATION':
        # await channel.send(db['location_msg'])
        printable = printer.printlocation(db['locations'], db['id2name'])
        await channel.send(printable)

      case 'CLONE_SERVER':
        print("Entered clone_server case.\n")
        clone = client.get_guild(1244818345157726349)
        casino = client.get_guild(797104015304294401)
        for cat in casino.categories:
          if cat.id == 927012133143728179 or cat.id == 797194987288002620:
            continue

          if cat.name == "Training Scaffolds":
            continue
          if cat.name == "Hegemopolis":
            continue
          if cat.name == "Stone Dungeon":
            continue
          if cat.name == "The Hub":
            continue
          if cat.name == "Upper Platforms":
            continue
          if cat.name in ["Family Camps", "Red Hell", "The Ranch", "Marcel Base", 
                         "The Snake Pit", "Snace Lodging"]:
            continue
          if cat.name == "The Islands":
            for channel in cat.channels:
              if channel.name == "island-6":
                cchannel = await clone.create_text_channel(channel.name)
                cur_date = (2020, 1, 1)
                async for message in channel.history(limit=99999, oldest_first = True):
                  msg_time = message.created_at
                  msg_date = (msg_time.year, msg_time.month, msg_time.day)
                  if msg_date != cur_date:
                    cur_date = msg_date
                    await cchannel.send(f"{cur_date}\n")
                  await cchannel.send(f"{message.author.name}: {message.content}\n")
                  for attachment in message.attachments:
                    await cchannel.send(attachment.url)

            continue
          ccat = await clone.create_category(cat.name)
          print(f"Reading category {cat.name}.\n")
          for channel in cat.channels:
            print(f"Reading channel {channel.name}.\n")
            cchannel = await ccat.create_text_channel(channel.name)
            cur_date = (2020, 1, 1)
            async for message in channel.history(limit=99999, oldest_first = True):
              try:
                msg_time = message.created_at
                msg_date = (msg_time.year, msg_time.month, msg_time.day)
                if msg_date != cur_date:
                  cur_date = msg_date
                  await cchannel.send(f"{cur_date}\n")
                await cchannel.send(f"{message.author.name}: {message.content}\n")
                for attachment in message.attachments:
                  await cchannel.send(attachment.url)
              except:
                continue

      case 'CHECKBOOK':
        if len(command) == 1:
          printable = printer.printcheck(db['checkbook'])
          await channel.send(f"{printable}")
        elif len(command) == 2 and command[1].isdigit():
          pass

      case 'PRINT':
        if len(command) == 1:
          await channel.send("What would you like to print?")
        elif len(command) != 1:
          print(msg)
          printable = msg.split("9..print ", 1)[1]
          if reply:
            await channel.send(printable)
          
      case 'MACRO':
        macros = {}
        try:
          macros = db['macros'][id]
        except:
          pass
          
        # Getting a list of all macros
        if len(command) == 1:
          printable = ""
          if len(macros) == 0:
            await channel.send(f"{char.name} doesn't have any macros!")
            return
          printable += f"{char.name}'s current macros:\n"
          for macro in macros:
            printable += f"9..{macro.lower()}\n"
          await channel.send(printable)
        
        # Getting info on a macro.
        elif len(command) == 2 and command[1] in macros:
          printable = f"**9..{command[1].lower()}:** \n```\n"
          for macro_command in macros[command[1]]:
            printable += f"{macro_command}\n"
          printable += "\n```"
          await channel.send(printable)

        elif len(command) >= 3:
          # Removing a macro
          if command[1] == "RM":
            if command[2] not in macros:
              await channel.send(f"Couldn't find macro 9..{command[2].lower()}!")
              return
            macros.pop(command[2])
            await channel.send(f"Macro `9..{command[2].lower()}` removed!")

          # Sharing a macro with someone else
          elif command[1] == "SHARE":
            try:
              macros = db['macros'][original_id]
              macro_name = command[2]
              if macro_name in macros:
                if id not in db['macros']:
                  db['macros'][id] = {}
                db['macros'][id][macro_name] = macros[macro_name]
                await channel.send(f"Macro `9..{macro_name.lower()}` shared "\
                                   f"with {db['id2name'][id].capitalize()}!")
            except:
              await channel.send("You don't have any macros to share!")
              return

        # Adding a macro
          elif command[1] == 'ADD':
            macro_commands = msg.split("\n- ")
            base_command = macro_commands.pop(0).split()[2]
            for i in range(len(macro_commands)):
              while i < len(macro_commands) and macro_commands[i].startswith("- "):
                macro_commands[i-1] = "\n".join(
                  (macro_commands[i-1], macro_commands.pop(i)))
            macros[base_command.upper()] = macro_commands
            db['macros'][id] = macros
            await channel.send(f"Added macro:  **9..{base_command}**")

      case 'CC':
        if len(command) == 1:
          printable = printer.printallcounter(char)
          if reply:
            await channel.send(printable)
        elif len(command) == 2:
          c_name = original_command[1]
          if c_name not in char.counter:
            await channel.send(f"Custom counter not found!")
            return
          result = printer.printcounter(c_name, char.counter[c_name])
          printable = result[0]
          if reply:
            await channel.send(printable)
          return result[1]
        elif len(command) >= 3:
          if command[1] == 'ADD':
            original_command.pop(0)
            original_command.pop(0)
            printable = modify.addcounter(char, original_command)
            await save_char(char)
            if reply:
              await channel.send(printable)
          elif command[1] == 'RM':
            c_name = original_command[2]
            char.counter.pop(c_name)
            await save_char(char)
            if reply:
              await channel.send(f"Removed custom counter!\n**{c_name}**")
          else:
            try:
              c_name = original_command[1]
              printable = modify.modcounter(char, c_name, int(command[2]))
              await save_char(char)
              result = printer.printcounter(c_name, char.counter[c_name])
              printable = result[0] + "\n" + printable
              if reply:
                await channel.send(printable)
              return result[1]
            except:
              await wrong_command(channel)
              return

      case 'LIST':
        printable = ""
        if len(command) == 1:
          printable = printer.printlist(list)

      case 'HERE':
        GM = await client.fetch_user(GM_ID)
        if len(command) == 1:
          db['locations'][id] = channel.jump_url
          if db['sess'][0]:
            channel_id, message_id, gm_channel_id, gm_msg_id = db['sess'][2]
            sess_channel = client.get_channel(channel_id)
            sess_msg = await sess_channel.fetch_message(message_id)
            gm_channel = await client.fetch_channel(gm_channel_id)
            gm_msg = await gm_channel.fetch_message(gm_msg_id)
            name = db['id2name'][id].capitalize()
            if id not in db['sess'][3]:
              db['sess'][3].append(id)
              db['sess'][4].append(int(time()))
              await GM.send(f"{name} joined the session in {channel.jump_url}!", \
                           suppress_embeds=True)
              await channel.send("You've joined the session, have fun!")
              printable = sess_msg.content
              printable += f"\n{name} - {channel.jump_url}"
              await sess_msg.edit(content=printable, suppress=True)
              await gm_msg.edit(content=printable, suppress=True)
              return
            else:
              printable = sess_msg.content
              to_find = f"{name} - .*"
              to_replace = f"{name} - {channel.jump_url}"
              printable = re.sub(to_find, to_replace, printable, 1)
              await sess_msg.edit(content=printable, suppress=True)
              await gm_msg.edit(content=printable, suppress=True)
              await channel.send("Location set!")
              return
          else:
            await channel.send("Location set!")
            return
              
      case 'SESSION':
        # [is_on, start_time, session_message, [player_ids], [last_replied]]
        printable = ""
        GM = await client.fetch_user(GM_ID)
        in_session = db['sess'][0]
        if len(command) == 1:
          if in_session:
            printable = f"Current session started at <t:{db['sess'][1]}:t>"
          else:
            printable = "Casino is not currently in sesseion."
          await channel.send(printable)
        elif len(command) == 2:
          if command[1] == 'OPEN':
            if not in_session:
              db['sess'][0] = True
              db['sess'][1] = int(time())
              await channel.send("## THE MAGIC CASINO IS NOW OPEN!!!")
              await channel.send(printer.printlocation(db['locations'], \
                                                       db['id2name']))
              sent_msg = await channel.send("**Current Players:** \n")
              await GM.send("Casino is now in session!")
              gm_msg = await GM.send("**Current Players:** \n")
              await sent_msg.pin()
              db['sess'][2] = (sent_msg.channel.id, sent_msg.id, \
                               gm_msg.channel.id, gm_msg.id)
              return
            else:
              await channel.send("Casino is already in session!")
          elif command[1] == 'CLOSE':
            if in_session:
              db['sess'][0] = False
              db['sess'][3] = []
              db['sess'][4] = []
              await GM.send("Casino is now closed!")
              await channel.send("## THE MAGIC CASINO IS NOW CLOSED!")
              await channel.send(printer.printlocation(db['locations'], \
                 db['id2name']))
              channel_id, message_id, gm_channel_id, gm_msg_id = db['sess'][2]
              sess_channel = client.get_channel(channel_id)
              gm_channel = client.get_channel(gm_channel_id)
              try:
                sess_msg = await sess_channel.fetch_message(message_id)
                gm_msg = await gm_channel.fetch_message(gm_msg_id)
                await sess_msg.unpin()
                edit_msg = sess_msg.content
                edit_msg += f"\n***This session is now over.***"
                await sess_msg.edit(content=edit_msg, suppress=True)
                await gm_msg.edit(content=edit_msg, suppress=True)
              except:
                print("Failed to unpin session message.")
            else:
              await channel.send("Casino is not currently in session!")

        elif len(command) == 3 and command[1] == 'RM':
          try:
            rm_id = db['name2id'][command[2]]
            for i in range(len(db['sess'][3])):
              if db['sess'][3][i] == rm_id:
                db['sess'][3].pop(i)
                db['sess'][4].pop(i)
                channel_id, message_id, gm_channel_id, gm_msg_id = db['sess'][2]
                sess_channel = client.get_channel(channel_id)
                gm_channel = client.get_channel(gm_channel_id)
                try:
                  sess_msg = await sess_channel.fetch_message(message_id)
                  gm_msg = await gm_channel.fetch_message(gm_msg_id)
                  edit_msg = "**Current Players:** \n"
                  for p_id in db['sess'][3]:
                    edit_msg += f"{db['id2name'][p_id].capitalize()} - "\
                    f"{db['locations'][p_id]}\n"
                  await sess_msg.edit(content=edit_msg, suppress=True)
                  await gm_msg.edit(content=edit_msg, suppress=True)
                  await channel.send(f"{db['id2name'][rm_id].capitalize()} "\
                                     "removed from session.")
                except:
                  print("Something went wrong!")
                break
            else:
              await channel.send(f"{db['id2name'][rm_id].capitalize()} "\
                                 "is not in the session!")
          except:
            await wrong_command(channel)
        else:
          await wrong_command(channel)
        return 

      case 'TYPING':
        if len(command) == 2:
          await channel.send("Nine is now typing...")
          casino = client.get_guild(797104015304294401)
          for tc in casino.text_channels:
            if tc.id == int(command[1]):
              await tc.typing()
              
      case _:
        # macros = {}
        # try:
        #   macros = db['macros'][id]
        # except:
        #   pass
        # if command[0] in macros:
        #   for macro_cmd in macros[command[0]]:
        #     await parse_command(id, channel, requester, macro_cmd)
        # else:
        await wrong_command(channel)



  else:
    await channel.send("You don't have a character yet! "\
                               "Make one with `9..register`, or check out "\
                               "`9..help` for more info!")

# RUN ONE TIME COMMANDS HERE



############################

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('9..help'))

  # one time on-start commands here:
  
  # archive = client.get_guild(1241883869549170748)
  # casino = client.get_guild(797104015304294401)
  # for cat in casino.text_channels:
  #   if cat.name == "plot-spot":
  #     await cat.send("Rep is the currency in The Magic Casino! Also don't you think this guy kinda looks like me? He even runs a comic shop too!")
  
  print(f'We have logged in as {client.user}')
  

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

    case 'MiscCross':
      await msg.delete()
      

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  id = str(message.author.id)
  channel = message.channel
  requester = (message.author.display_name, str(message.author.display_avatar))
  original_msg = message.content
  msg = original_msg.upper()

  # Checks for dropped players.
  GM = await client.fetch_user(GM_ID)
  session = db['sess']
  if session[0]:
    for i in range(len(session[4])):
      if (int(time()) - session[4][i]) >= 600:
        db['sess'][4][i] = int(time())
        player_id = session[3][i]
        player_location = db['locations'][player_id]
        await GM.send(f"It's been a while since you've messaged "\
                f"{db['id2name'][str(player_id)].capitalize()}. Did you drop them?")

  # Saves the message in an archive server.
  archive = client.get_guild(ARCHIVE_ID)
  if message.guild.id != 1241883869549170748:
    if channel.type == discord.ChannelType.text:
      has_channel = False
      for archive_channel in archive.text_channels:
        if str(archive_channel) == str(channel):
          has_channel = True
          break
      if not has_channel:
        await archive.create_text_channel(str(channel),
                      category= await archive.fetch_channel(1241894024105951263))
      for archive_channel in archive.text_channels:
        if archive_channel.name == channel.name:
          await archive_channel.send(f"{message.author.name}: {message.content}\n")
          for attachment in message.attachments:
            await archive_channel.send(attachment.url)
    elif channel.type == discord.ChannelType.private:
      has_channel = False
      for archive_channel in archive.text_channels:
        if str(archive_channel) == message.author.name:
          has_channel = True
          break
      if not has_channel:
        await archive.create_text_channel(message.author.name,
                      category=await archive.fetch_channel(1241893920896450662))
      for archive_channel in archive.text_channels:
        if str(archive_channel) == message.author.name:
          await archive_channel.send(f"{message.author.name}: {message.content}")
          for attachment in message.attachments:
            await archive_channel.send(attachment.url)

  # Checks if it's a response from Felix to a player
  if db['sess'][0] and message.author.id == 531288319859097601:
    player_ids = db['sess'][3]
    for i in range(len(player_ids)):
      if db['locations'][player_ids[i]] == channel.jump_url:
        db['sess'][4][i] = int(time())
        
  # Natural language responses.
  if "HEY NINE" in msg or "HI NINE" in msg or "HELLO NINE" in msg:
    await channel.send(random.choice(printer.greetings_back))

  if ("I LOVE" in msg or "ILY" in msg) and "NINE" in msg:
    if id == names['MIKEY']:
      await channel.send("I love you too Mikey!")
    else:
      await channel.send(random.choice(printer.affection_back))

  if ("THANKS" in msg or "THANK YOU" in msg) and "NINE" in msg:
    await channel.send("You're welcome!")

  if "TELL" in msg and "JOKE" in msg and "NINE" in msg:
    response = requests.get('https://v2.jokeapi.dev/joke/Pun')
    json_data = response.json()
    if json_data["type"] == "single":
      await channel.send(json_data["joke"])
    elif json_data['type'] == 'twopart':
      await channel.send(json_data['setup'])
      sleep(2)
      await channel.send(json_data['delivery'])

  if msg.startswith("**__WHERE EVERYONE IS__**"):
    db["location_msg"] = original_msg

  # Location tracking module
  if len(message.channel_mentions) and message.reference and \
  (id == "531288319859097601" or id == "262320046653702145"):
    location = message.channel_mentions[0]
    reply_msg = await channel.fetch_message(message.reference.message_id)
    reply_author_id = str(reply_msg.author.id)
    db['locations'][reply_author_id] = location.jump_url
    await location.send(f"<@{reply_author_id}> arrives here...")
    if db['sess'][0]:
      channel_id, message_id = db['sess'][2]
      sess_channel = client.get_channel(channel_id)
      sess_msg = await sess_channel.fetch_message(message_id)
      name = (db['id2name'][reply_author_id]).capitalize()
      if id in db['sess'][3]:
        printable = sess_msg.content
        to_find = f"{name} - .*"
        to_replace = f"{name} - {location.jump_url}"
        printable = re.sub(to_find, to_replace, printable, 1)
        await sess_msg.edit(content=printable, suppress=True)
        return

  # Most methods of Ninebot starts with 9..
  if msg.startswith('9..'):
    await parse_command(id, channel, requester, original_msg)
    
my_secret = os.environ['TOKEN']
client.run(my_secret)