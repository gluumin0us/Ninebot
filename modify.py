from character import Character

int_to_stat = ["Strength", "Dexterity", "Charisma", 
               "Intelligence", "Attack", "Willpower", "Luck"]
stat_to_int = {"STR": 0, "DEX": 1, "CHA": 2, "INT": 3, 
               "ATT": 4, "WILL": 5, "LUCK": 6}


def restat(char: Character):
  for i in range(7):
    char.stat[i] = 2 + char.level + char.legendary[i] + char.mod[i]
  for i in char.tal:
    for j in range(len(i[1])):
      char.stat[i[1][j]] += i[2][j]

def modhp(char: Character, hp_change: int):
  printable = ""
  thp_blocked = False
  if char.thp > 0 and hp_change < 0:
    old_thp = char.thp
    if char.thp < -hp_change:
      hp_change += char.thp
      char.thp = 0
      printable += f"THP - {old_thp} -> **0**\n"
    elif char.thp >= -hp_change:
      char.thp += hp_change
      printable += f"THP - {old_thp} -> **{char.thp}**"
      thp_blocked = True
  if not thp_blocked:
    old_hp = char.hp
    char.hp += hp_change
    if char.hp > char.max_hp:
      char.hp = char.max_hp
    elif char.hp < 0:
      char.hp = 0
    printable += f"HP - {old_hp}/{char.max_hp} -> **{char.hp}/{char.max_hp}**\n"
    if char.hp == 0:
      printable += f"\n**{char.name.upper()} IS BLEEDING OUT.**"
    elif old_hp == 0:
      printable += f"\n{char.name} is no longer bleeding out."
    elif char.hp <= 15:
      printable += f"\n**{char.name.upper()} IS IN CRITICAL HP.**"
    elif old_hp <= 15:
      printable += f"\n{char.name} is no longer in critical hp."
  return printable

xp_total = [0, 140, 520, 1140, 2000, 3100, 4440, 6020, 7840, 9900]

def modxp(char: Character, xp_change: int):
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
  printable += f"Level - LV{old_level}, {old_xp}/{240 * old_level - 100} -> "
  if char.level != 10:
    printable += f"**LV{char.level}, {char.xp}/{240 * char.level - 100}**\n"
  elif char.level == 10:
    printable += f"**LV{char.level}, MAX LEVEL**\n"
  return printable

def modleg(char: Character, stat: str, leg_change: int):
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

  restat(char)

  return printable

def modtal(char: Character, action: str, tal):
  printable = ""
  match action:
    case 'ADD':
      for i in range(len(tal[1])):
        tal[1][i] = stat_to_int[tal[1][i]]
      char.tal.append(tal)
      printable += "Talisman added!\n"\
      f"*TAL{len(char.tal)} - {tal[0]}*\n"
    case 'RM':
      removed_tal = char.tal.pop(tal - 1)
      printable += "Talisman removed!\n"\
      f"*TAL{tal} - {removed_tal[0]}*\n"
  restat(char)
  return printable