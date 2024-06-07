from character import Character
from printer import printRoman
import re
import math

int_to_stat = ["Strength", "Dexterity", "Charisma", 
               "Intelligence", "Attack", "Willpower", "Luck"]
stat_to_int = {"STR": 0, "DEX": 1, "CHA": 2, "INT": 3, 
               "ATT": 4, "WILL": 5, "LUCK": 6}


def restat(char: Character):
  for i in range(7):
    char.stat[i] = 2 + char.level + char.legendary[i] + char.mod[i]
    if char.hp <= 15:
      char.stat[i] -= 2
  for i in char.tal:
    for j in range(len(i[1])):
      char.stat[i[1][j]] += i[2][j]
  for i in char.aff:
    for j in range(len(i[2])):
      char.stat[i[2][j]] += i[3][j]
  char.max_hp = 40 + char.level * 5

def modhp(char: Character, hp_change: int) -> str:
  printable = ""
  thp_blocked = False
  old_thp = 0
  if char.thp > 0 and hp_change < 0:
    old_thp = char.thp
    if char.thp < -hp_change:
      hp_change += char.thp
      char.thp = 0
      printable += f"THP - {old_thp} -> **0**\n"
    elif char.thp >= -hp_change:
      char.thp += hp_change
      printable += f"THP - {old_thp} -> **{char.thp}**\n"
      thp_blocked = True
  if thp_blocked:
    hp_percent = math.floor((char.hp / char.max_hp) * 16)
    printable += "⧼"
    for i in range(16):
      if i < hp_percent:
        printable += "█"
      else:
        printable += "░"
    printable += "⧽"
    for i in range(math.ceil(char.thp / 10)):
      printable += "❱"
    printable += f"\n**HP - {char.hp}/{char.max_hp}** "
    if char.thp > 0:
      printable += f"❰**{char.thp}**❱"
  if not thp_blocked:
    old_hp = char.hp
    char.hp += hp_change
    if char.hp > char.max_hp:
      char.hp = char.max_hp
    elif char.hp < 0:
      char.hp = 0
    hp_percent = math.floor((char.hp / char.max_hp) * 16)
    old_hp_percent = math.floor((old_hp / char.max_hp) * 16)
    printable += "⧼"
    for i in range(16):
      if i < hp_percent:
        if i < old_hp_percent:
          printable += "▓"
        else:
          printable += "█"
      elif i < old_hp_percent:
        printable += "▒"
      else:
        printable += "░"
    printable += "⧽"
    for i in range(math.ceil(char.thp / 10)):
      printable += "❱"
    printable += f"\nHP - {old_hp}/{char.max_hp} "
    if old_thp > 0:
      printable += f"❬{old_thp}❭ "
    printable += f"-> **{char.hp}/{char.max_hp}** "
    if char.hp == 0:
      printable += f"\n**{char.name.upper()} IS BLEEDING OUT.**"
    elif old_hp == 0:
      printable += f"\n{char.name} is no longer bleeding out."
    elif char.hp <= 15:
      printable += f"\n**{char.name.upper()} IS IN CRITICAL HP.**"
    elif old_hp <= 15:
      printable += f"\n{char.name} is no longer in critical hp."
    restat(char)
  return printable

xp_total = [0, 140, 520, 1140, 2000, 3100, 4440, 6020, 7840, 9900]

def modxp(char: Character, xp_change: int) -> str:
  if not isinstance(xp_change, int):
    return "You're using the command incorrectly - "\
    "check `9..help xp` for more details."
  printable = ""
  old_level = char.level
  old_xp = char.xp
  old_total_xp = xp_total[old_level - 1] + char.xp
  new_total_xp = old_total_xp + xp_change
  for i in range(1, 10):
    if new_total_xp >= 9900:
      char.level = 10
      char.xp = new_total_xp - 9900
    if new_total_xp < xp_total[i]:
      char.level = i
      char.xp = new_total_xp - xp_total[i-1]
      break
  restat(char)
  if old_level < char.level:
    printable += "**Level Up!**\n"
    char.max_hp = 40 + char.level * 5
    char.hp = char.max_hp
  elif old_level > char.level:
    printable += "Level Down!\n"
    char.max_hp = 40 + char.level * 5
    char.hp = char.max_hp
  printable += f"LV{old_level}, {old_xp}/{240 * old_level - 100} -> "
  if char.level != 10:
    printable += f"**LV{char.level}, {char.xp}/{240 * char.level - 100}**\n"
  elif char.level == 10:
    printable += f"**LV{char.level}, MAX LEVEL**\n"
  return printable

def modleg(char: Character, stat: str, leg_change: int) -> str:
  printable = ""
  match stat:
    case 'STR':
      old_str = char.legendary[0]
      char.legendary[0] += leg_change
      printable += f"Strength: +{old_str} -> **+{char.legendary[0]}**"

    case 'DEX':
      old_dex = char.legendary[1]
      char.legendary[1] += leg_change
      printable += f"Dexterity: +{old_dex} -> **+{char.legendary[1]}**"

    case 'CHA':
      old_cha = char.legendary[2]
      char.legendary[2] += leg_change
      printable += f"Charisma: +{old_cha} -> **+{char.legendary[2]}**"

    case 'INT':
      old_int = char.legendary[3]
      char.legendary[3] += leg_change
      printable += f"Intelligence: +{old_int} -> **+{char.legendary[3]}**"

    case 'ATT':
      old_att = char.legendary[4]
      char.legendary[4] += leg_change
      printable += f"Attack: +{old_att} -> **+{char.legendary[4]}**"

    case 'WILL':
      old_wil = char.legendary[5]
      char.legendary[5] += leg_change
      printable += f"Willpower: +{old_wil} -> **+{char.legendary[5]}**"

    case 'LUCK':
      old_luc = char.legendary[6]
      char.legendary[6] += leg_change
      printable += f"Luck: +{old_luc} -> **+{char.legendary[6]}**"

    case _:
      printable += "I don't think you're quite using the command correctly. "
      printable += "Refer to `9..help legend` for more details."

  restat(char)
  return printable

def modtal(char: Character, action: str, tal) -> str:
  printable = ""
  match action:
    case 'ADD':
      try:
        for i in range(len(tal[1])):
          tal[1][i] = stat_to_int[tal[1][i]]
        char.tal.append(tal)
        printable += "Talisman added!\n"\
        f"*TAL{len(char.tal)} - {tal[0]}*\n"
      except:
        printable += "Something went wrong. Did you type everything correctly?\n"
    case 'RM':
      if tal.isdigit():
        try:
          removed_tal = char.tal.pop(int(tal) - 1)
          printable += "Talisman removed!\n"\
          f"*TAL{tal} - {removed_tal[0]}*\n"
        except:
          printable += f"Failed to remove TAL{tal}. Are you sure it exists?\n"
      else:
        try:
          for i in range(len(char.tal)):
            if char.tal[i][0].upper() == tal:
              removed_tal = char.tal.pop(i)
              printable += "Talisman removed!\n"\
              f"*TAL{i+1} - {removed_tal[0]}*\n"
        except:
          printable += f"Failed to remove '{tal}'. Are you sure it exists?\n"
          
    case _:
      printable += "I don't think you're quite using the command correctly. "
      printable += "Refer to `9..help tal` for more details.\n"
      
  restat(char)
  return printable

def modaff(char: Character, action: str, aff) -> str:
  printable = ""
  match action:
    case 'ADD':
      aff[1] = printRoman(aff[1])
      for i in range(len(aff[2])):
        aff[2][i] = stat_to_int[aff[2][i]]
      for i in range(len(char.aff)):
        if aff[0] == char.aff[i][0]:
          char.aff[i] = aff
          printable += f"Affliction modified!\n**{aff[0]} {aff[1]}**"
          return printable
      char.aff.append(aff)
      printable += f"Affliction added!\n**{aff[0]} {aff[1]}**"
    case 'RM':
      for i in range(len(char.aff)):
        failed_remove = True
        if char.aff[i][0] == aff:
          removed_aff = char.aff.pop(i)
          printable += f"Affliction removed!\n**{removed_aff[0]} {removed_aff[1]}**"
          failed_remove = False
      if failed_remove:
        printable += f"I didn't find an affliction named {aff} to remove!\n"
    case _:
      printable += "I don't think you're quite using the command correctly. "
      printable += "Refer to `9..help modaff` for more details."
  restat(char)
  return printable

def tick(char: Character) -> str:
  printable = ""
  bleed_counter = {
    'I': -3,
    'II': -5,
    'III': -8,
    'IV': -13,
    'V': -21
  }
  for i in char.aff:
    if i[0] == 'BLEEDING':
      printable += f"**BLEEDING {i[1]}**\n"
      printable += modhp(char, bleed_counter[i[1]])
      break

  if printable == "":
    printable += "No tickable persistent effects found."
  return printable

def makechar(csh: list[str]) -> Character:
  if csh[0].search(":$"):
    char_name = csh[0].split(":", 1)[0]
    char_level = csh[2].split(",", 1)[0]
    char_xp = csh[3].split("/", 1)[0]
  pass

def addcounter(char, c_info) -> str:
  # name: [min, max, val, display, milestone, is_hidden]
  args = ['MIN', 'MAX', 'VAL', 'DISPLAY', 'MILESTONE', 'HIDDEN']
  counter = [0, 10, 10, 'NUM', None, 'FALSE']
  name = ""
  has_val = False
  while True:
    if len(c_info) == 0:
      return "You need at least a max value to make a counter!"
    if c_info[0].upper() not in args:
      name += c_info.pop(0)
    else:
      break
  for i in range(len(c_info)-1):
    info = c_info[i].upper()
    if info == "VAL":
      has_val = True
    for j in range(len(args)):
      if args[j] == info:
        counter[j] = c_info[i+1].upper()
  for i in range(3):
    counter[i] = int(counter[i])
  if counter[4]:
    counter[4] = eval(counter[4])
  if not has_val:
    counter[2] = counter[1]
  char.counter[name] = counter
  return f"Custom counter Added: **{name}**"

def modcounter(char: Character, c_name: str, mod_amount: int) -> str:
  # name: [min, max, val, display, is_hidden]
  if c_name not in char.counter:
    return f"Custom counter '{c_name}' not found!"
  counter = char.counter[c_name]
  old_val = counter[2]
  counter[2] += mod_amount
  if counter[2] > counter[1]:
    counter[2] = counter[1]
  elif counter[2] < counter[0]:
    counter[2] = counter[0]
  return f"{old_val}/{counter[1]} -> **{counter[2]}/{counter[1]}**"