from character import Character


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


def printroll(char: Character, base: int, stat: str):
  # Returns a string that prints out the results of a stat roll
  printable = ""
  result = base
  match stat:
    case "STR":
      result += char.str
      printable = "Strength "
    case "DEX":
      result += char.dex
      printable = "Dexterity "
    case "CHA":
      result += char.cha
      printable = "Charisma "
    case "INT":
      result += char.int
      printable = "Intelligence "
    case "ATT":
      result += char.att
      printable = "Attack "
    case "WILL":
      result += char.wil
      printable = "Willpower "
    case "LUCK":
      result += char.luc
      printable = "Luck "
  printable += f"Check: **-{result}+**\n"
  
  if base == 20:
    printable += "**NATURAL 20!**"
    
  return printable
