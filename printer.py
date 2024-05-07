from character import Character
import discord

num_to_stat = ["Strength", "Dexterity", "Charisma", 
   "Intelligence", "Attack", "Willpower", "Luck"]

def printchar(char: Character):
  # Takes in a Character object
  # Returns a string that prints out a character's info
  printable = ""
  printable += (f"__{char.name}: LV{char.level}, "
                f"{char.xp}/{240 * char.level - 100}__\n")
  leg_mark = ["", "", "", "", "", "", ""]
  tal_mark = ["", "", "", "", "", "", ""]
  for i in range(len(char.tal)):
    cur_tal = char.tal[i]
    tal_mark[cur_tal[1]] += f"(TAL{i+1} +{cur_tal[2]})"
  for i in range(len(char.legendary)):
    for j in range(char.legendary[i]):
      leg_mark[i] += '+'
  for i in range(7):
    printable += (f"{leg_mark[i]}{num_to_stat[i]} - {char.stat[i]} {tal_mark[i]}\n")
    
  for i in range(len(char.tal)):
    printable += (f"*TAL{i+1} - {char.tal[i][0]}*\n")
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
        result += char.stat[0]
        printable += "Strength "
      case "DEX":
        result += char.stat[1]
        printable += "Dexterity "
      case "CHA":
        result += char.stat[2]
        printable += "Charisma "
      case "INT":
        result += char.stat[3]
        printable += "Intelligence "
      case "ATT":
        result += char.stat[4]
        printable += "Attack "
      case "WILL":
        result += char.stat[5]
        printable += "Willpower "
      case "LUCK":
        result += char.stat[6]
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
          "**9..thp**\n\n**9..roll**\n\n**9..xp**\n\n"\
          "**9..level**\n\n**9..legend**\n\n",
      inline=True)

      embed.add_field(name="Description",
      value="Gives you information on me, or a specific command.\n\n"\
            "Prints out your character stats.\n\n"\
            "Prints out, or modifies, your HP.\n\n"\
            "Prints out, or modifies, your temp HP specifically.\n\n"\
            "Rolls a d20, and can optionally add your stats.\n\n"\
            "Prints out, or modifies, your XP.\n\n"\
            "Prints out your current level and XP.\n\n"\
            "Prints out, or modifies, your legendary bonuses.\n\n",
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

    case "LEGEND":
      embed = discord.Embed(title="9..legend",
      description="This command will show you your legendary "\
                "bonuses for each of your stats "\
                "if you run it without arguments.\n\n"\
                "If you run the command with a stat and a number, "\
                "it will add the number to the stat's legendary bonus.\n\n "\
                "e.g. `9..legend dex +1` would give you one legendary bonus "\
                "for your dexterity stat.",
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

def printtal(char: Character):
  printable = ""
  if len(char.tal) == 0:
    return "You don't have any talismans!\n"
  for i in range(len(char.tal)):
    cur_tal = char.tal[i]
    printable += f"**TAL{i+1} - {cur_tal[0]}**\n"\
    f"+{cur_tal[2]} {num_to_stat[cur_tal[1]]}\n"
    if cur_tal[3] != "":
      printable += f"*{cur_tal[3]}*\n"
    printable += "\n"

  return printable