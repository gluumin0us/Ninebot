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
  printable = ":game_die:  "
  result = base
  if stat.isdigit() or stat.startswith('+') or stat.startswith('-'):
    result += int(stat)
    printable = f"{stat} Custom "
  else:
    match stat:
      case "STR":
        result += char.str
        printable += "Strength "
      case "DEX":
        result += char.dex
        printable += "Dexterity "
      case "CHA":
        result += char.cha
        printable += "Charisma "
      case "INT":
        result += char.int
        printable += "Intelligence "
      case "ATT":
        result += char.att
        printable += "Attack "
      case "WILL":
        result += char.wil
        printable += "Willpower "
      case "LUCK":
        result += char.luc
        printable += "Luck "
  printable += f"Check: **-{result}+** :game_die:\n"

  if base == 1:
    printable += "Nat 1 :(\n"
  
  if base == 20:
    printable += "**NATURAL 20!**"
    
  return printable

def printhelp(cmd: str, requester):
  req_name, req_avatar = requester
  match cmd: 
    case "MAIN":
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

    case "HELP":
      embed = discord.Embed(title="9..help",
      description="This command will bring up helpful information, "\
                  "either about my commands in general, or one command"\
                  " in particular. "\
                  "To get information on a specific command, "\
                  "do `9..help <command>`.\n\n"\
                  "e.g. `9..help hp` will bring up information on the HP command.",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "CHAR":
      embed = discord.Embed(title="9..char",
      description="This command will show you your character "\
                  "information and stats within the magic casino, "\
                  "including your name, level, experience, stats, "\
                  "talismans, and HP.\n"\
                  "For an example of what that might look like, check #all-levels .",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed
    
    case "HP":
      embed = discord.Embed(title="9..hp",
      description="This command will show you your current "\
                  "and max HP as well as any temp "\
                  "HP if you run it without arguments. \n\n" \
                  "If you run the command with a number, " \
                  "your HP will be modified by that number.\n" \
                  "e.g. `9..hp -12` will make you take 12 damage, " \
                  "and `9..hp +5` will heal you by 5.\n\n" \
                  "Any damage you take will deduct from your temp HP pool first, " \
                  "but you won't be able to heal your temp HP.\n\n" \
                  "You HP can't go below 0 or go above your max HP.\n",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "THP":
      embed = discord.Embed(title="9..thp",
      description="This command will show you your current temp HP " \
                  "if you run it without arguments. \n\n" \
                  "If you run the command with a number, " \
                  "your temp HP will be modified by that number.\n" \
                  "e.g. `9..thp +20` will give you 20 extra temp HP, " \
                  "and `9..thp -8` will take away 8 temp HP.\n\n" \
                  "Your temp HP can't go below 0.\n",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "ROLL":
      embed = discord.Embed(title="<9..roll>",
      description="This command will roll a d20 and give you the results" \
                  "if you run it without arguments.\n\n" \
                  "If you run the command with a stat, "\
                  "it will add the corresponding " \
                  "stat to your result. "\
                  "It will also roll a legendary roll for you " \
                  "automatically when you get a natural 20.\n" \
                  "e.g. `9..roll dex` will return a random number "\
                  "between 1~20 with your" \
                  "dexterity modifier added.\n\n" \
                  "You can also roll with a custom bonus "\
                  "by running the command with a number.\n" \
                  "e.g. `9..roll +4` will return a d20 dice roll with +4 added.\n",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "XP":
      embed = discord.Embed(title="9..xp",
      description="This command will show you your current xp "\
                  "and the xp needed for your next level up "\
                  "if you run it without arguments.\n\n"\
                  "If you run the command with a number, "\
                  "it will add the number to your current xp, "\
                  "automatically levelling up/down and "\
                  "modifying your stats as needed.\n\n"\
                  "e.g. `9..xp +200` would let you gain 200 xp.",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "LEVEL":
      embed = discord.Embed(title="9..level",
      description="This command will show you your current level "\
                  "as well as your xp. It's a pretty simple command.",
      colour=0xff6600)
    
      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed


def printleg(char: Character):
  printable = f"{char.name}'s Legendary bonuses: \n"
  printable += f"Strength: +{char.legendary[0]}\n"
  printable += f"Dexterity: +{char.legendary[1]}\n"
  printable += f"Charisma: +{char.legendary[2]}\n"
  printable += f"Intelligence: +{char.legendary[3]}\n"
  printable += f"Attack: +{char.legendary[4]}\n"
  printable += f"Willpower: +{char.legendary[5]}\n"
  printable += f"Luck: +{char.legendary[6]}\n"
  return printable