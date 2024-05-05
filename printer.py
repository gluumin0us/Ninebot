from character import Character
import discord


def printchar(char: Character):
  # Takes in a Character object
  # Returns a string that prints out a character's info
  printable = ""
  printable += (f"__{char.name}: LV{char.level}, "
                f"{char.xp}/{240 * char.level - 100}__\n")
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

  if base == 1:
    printable += "Nat 1 :(\n"
  
  if base == 20:
    printable += "**NATURAL 20!**"
    
  return printable

def printhelp(cmd: str, requester):
  printable = ""
  if cmd == "MAIN":
    req_name, req_avatar = requester
    embed = discord.Embed(title="-Help-",
      description="Hello! I'm Nine, your Magic Casino character manager!\n"\
                "To call on me, start your message with `9..`\n\n"\
                "If you want specific details on a command, \n"\
                "please do `9..help <command>`\n"\
                "e.g. `9..help hp` will give you information on the hp command.\n\n"\
                "Adding `-t <name>` at the end of any command will make the "\
                "command target another player.\n"\
                "e.g. `9..char -t jack` will show Jack's character instead "\
                "of your own.",
      colour=0xff6600)

    embed.set_author(name=req_name, icon_url=req_avatar)

    embed.add_field(name="\n", value="\n", inline=False)

    embed.add_field(name="Command",
      value="**9..help**\n\n**9..char**\n\n**9..hp**\n\n"\
          "**9..thp**\n\n**9..roll**\n\n**9..xp**\n\n**9..level**",
      inline=True)

    embed.add_field(name="Description",
      value="Gives you information on me, or a specific command.\n\n"\
            "Prints out your character stats.\n\n"\
            "Prints out, or modifies, your HP.\n\n"\
            "Prints out, or modifies, your temp HP specifically.\n\n"\
            "Rolls a d20, and can optionally add your stats.\n\n"\
            "Prints out, or modifies, your XP.\n\n"\
            "Prints out your current level and XP.",
      inline=True)
    return embed

  if cmd == "HELP":
    printable += "**<9..help>**\n"
    printable += "This command will bring up helpful information, "
    printable += "either about my commands in general, or on one specific command.\n"
    printable += "To get information on a specific command, "
    printable += "do `9..help <command>`.\n"
    printable += "e.g. `9..help hp` will bring up information on the HP command.\n"

  if cmd == "CHAR":
    printable += "**<9..char>**\n" \
    "This command will show you your character information and stats " \
    "within the magic casino, including your name, level, experience, " \
    "stats, talismans, and HP.\n" \
    "For an example of what that might look like, check #all-levels .\n"
    
  if cmd == "HP":
    printable += "**<9..hp>**\n" \
    "This command will show you your current and max HP as well as any temp " \
    "HP if you run it without arguments." \
    "If you run the command with a number, " \
    "your HP will be modified by that number.\n" \
    "e.g. `9..hp -12` will make you take 12 damage, " \
    "and `9..hp +5` will heal you by 5.\n" \
    "Any damage you take will deduct from your temp HP pool first, " \
    "but you won't be able to heal your temp HP.\n" \
    "You HP can't go below 0 or go above your max HP.\n" \

  if cmd == "THP":
    printable = "**<9..thp>**\n" \
    "This command will show you your current temp HP " \
    "if you run it without arguments.\n" \
    "If you run the command with a number, " \
    "your temp HP will be modified by that number.\n" \
    "e.g. `9..thp +20` will give you 20 extra temp HP, " \
    "and `9..thp -8` will take away 8 temp HP.\n" \
    "Your temp HP can't go below 0.\n" \

  if cmd == "ROLL":
    printable = "**<9..roll>**\n" \
    "This command will roll a d20 and give you the results" \
    "if you run it without arguments.\n" \
    "If you run the command with a stat, it will add the corresponding " \
    "stat to your result. It will also roll a legendary roll for you " \
    "automatically when you get a natural 20.\n" \
    "e.g. `9..roll dex` will return a random number between 1~20 with your" \
    "dexterity modifier added.\n" 
  
  return printable


def test_embed(requester):
  req_name, req_avatar = requester
  embed = discord.Embed(title="-Help-",
    description="Hello! I'm Nine, your Magic Casino character manager!\n"\
                "To call on me, start your message with `9..`\n\n"\
                "If you want specific details on a command, \n"\
                "please do `9..help <command>`\n"\
                "e.g. `9..help hp` will give you information on the hp command.\n\n"\
                "Adding `-t <name>` at the end of any command will make the "\
                "command target another player.\n"\
                "e.g. `9..char -t jack` will show Jack's character instead "\
                "of your own."
                ,
    colour=0xff6600)

  embed.set_author(name=req_name, icon_url=str(req_avatar))

  embed.add_field(name="\n", value="\n", inline=False)

  embed.add_field(name="Command",
value="**9..help**\n\n**9..char**\n\n**9..hp**\n\n"\
      "**9..thp**\n\n**9..roll**\n\n**9..xp**\n\n**9..level**",
  inline=True)
  
  embed.add_field(name="Description",
  value="Gives you information on me, or a specific command.\n\n"\
        "Prints out your character stats.\n\n"\
        "Prints out, or modifies, your HP.\n\n"\
        "Prints out, or modifies, your temp HP specifically.\n\n"\
        "Rolls a d20, and can optionally add your stats.\n\n"\
        "Prints out, or modifies, your XP.\n\n"\
        "Prints out your current level and XP.",
  inline=True)
  return embed