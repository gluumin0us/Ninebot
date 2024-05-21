from character import Character
import discord
import re
from random import randint

int_to_stat = ["Strength", "Dexterity", "Charisma", 
   "Intelligence", "Attack", "Willpower", "Luck"]
stat_to_int = {"STR": 0, "DEX": 1, "CHA": 2, "INT": 3, 
   "ATT": 4, "WILL": 5, "LUCK": 6}

def printRoman(number):
  num = [1, 4, 5, 9, 10, 40, 50, 90,
        100, 400, 500, 900, 1000]
  sym = ["I", "IV", "V", "IX", "X", "XL",
        "L", "XC", "C", "CD", "D", "CM", "M"]
  i = 12
  printable = ""

  while number:
      div = number // num[i]
      number %= num[i]

      while div:
          printable += sym[i]
          div -= 1
      i -= 1
  return printable

greetings_back = ["Hello!", "Hi!", "Good to see you!", "Howdy!"]
affection_back = ["I'm honored?", "Uhm... who are you again?", 
                  "I'm glad?", "Uh- Thanks!", "Thank you?"]

def printchar(char: Character):
  # Takes in a Character object
  # Returns a string that prints out a character's info
  printable = []
  printable_name = f"__{char.name}: LV{char.level}, "
  if char.level != 10:
    printable_name += f"{char.xp}/{240 * char.level - 100}__"
  else:
    printable_name += "**MAX LEVEL**"
  printable.append(printable_name)

  leg_mark = ["", "", "", "", "", "", ""]
  tal_mark = ["", "", "", "", "", "", ""]
  debuff_mark = [0, 0, 0, 0, 0, 0, 0]
  
  if char.hp <= 15:
    printable.append("**CRITICAL (-2 ALL)**")
    for i in range(len(debuff_mark)):
      debuff_mark[i] -= 2
  
  for i in char.aff:
    printable.append(f"**{i[0]} {i[1]}**")
  

  for i in range(len(char.tal)):
    cur_tal = char.tal[i]
    for j in range(len(cur_tal[1])):
      tal_mark[cur_tal[1][j]] += f"(TAL{i+1} "
      if cur_tal[2][j] > 0:
        tal_mark[cur_tal[1][j]] += '+'
      tal_mark[cur_tal[1][j]] += f"{cur_tal[2][j]}) "
  for i in range(len(char.legendary)):
    for j in range(char.legendary[i]):
      leg_mark[i] += '+'
  for aff in char.aff:
    for i in range(len(aff[2])):
      debuff_mark[aff[2][i]] += aff[3][i]
      
  for i in range(7):
    printable_stat = f"{leg_mark[i]}{int_to_stat[i]} - "\
                     f"{char.stat[i]} {tal_mark[i]} "
    if debuff_mark[i] != 0:
      printable_stat += f"({str(debuff_mark[i])})"
    printable.append(printable_stat)

  for i in range(len(char.tal)):
    printable.append(f"*TAL{i+1} - {char.tal[i][0]}*")
  printable.append(f"HP - {char.hp}/{char.max_hp}")
  if char.thp > 0:
    printable.append(f"THP - {char.thp}")

  return printable


def printroll(char: Character, base: int, stat: str):
  # Returns a string that prints out the results of a stat roll
  printable = ":game_die:  "
  result = base

  if re.search("^[0-9]+D[0-9]+$", stat):
    nums = re.split("D", stat)
    nums[0] = int(nums[0])
    nums[1] = int(nums[1])
    num_total = 0
    printable = f"Rolling {stat}... \n["
    for i in range(nums[0]):
      temp_result = randint(1, nums[1])
      if i != 0:
        printable += ", "
      printable += str(temp_result)
      num_total += temp_result
    printable += f"] = **{num_total}**\n"
    return printable
    
  elif stat.isdigit() or stat.startswith('+') or stat.startswith('-'):
    result += int(stat)
    printable += f"{stat} Custom "

  elif stat in stat_to_int:
    int_stat = stat_to_int[stat]
    result += char.stat[int_stat]
    printable += f"{int_to_stat[int_stat]} "

  else:
    printable = "I don't think you're quite using the command correctly. "\
    "Refer to 9..help roll for more details."
    return printable
    
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
                "of your own.\n\n"\
                "Some commands might have you input a stat. The respectives stats "\
                "are `str`, `dex`, `cha`, `int`, `att`, `will`, and `luck`.",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)

      embed.add_field(name="\n", value="\n", inline=False)

      embed.add_field(name="Commands",
      value="__**9..help**__\t"\
        "  Gives you information on me, or a specific command.\n"\
        "__**9..char**__\t"\
        "  Prints out your character stats.\n"\
        "__**9..hp**__\t"\
        "  Prints out, or modifies, your HP.\n"\
        "__**9..thp**__\t"\
        "  Prints out, or modifies, your temp HP specifically.\n"\
        "__**9..roll**__\t"\
        "  Rolls a d20, and can optionally add your stats.\n"\
        "__**9..xp**__\t"\
        "  Prints out, or modifies, your XP.\n"\
        "__**9..level**__\t"\
        "  Prints out, or sets your current level.\n"\
        "__**9..legend**__\t"\
        "  Prints out, or modifies, your legendary bonuses.\n"\
        "__**9..tal**__\t"\
        "  Prints out, adds, or removes talismans.\n"\
        "__**9..aff**__\t"\
        "  Prints out, adds, or removes afflictions.\n"\
        "__**9..register**__\t"\
        "  Registers yourself a character if you don't have one.\n"\
        "__**9..tick**__\t"\
        "  Advances any persistent effects such as bleeding.\n"\
        "__**9..rep**__\t"\
        "  Prints out, or modifies, your rep count.\n",
        inline=False)

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
                  "as well as your xp if you run it without arguments.\n\n"\
                  "If you run the command as `9..level set <number>`, it'll "\
                  "set your level to that number with no extra xp.\n"\
                  "e.g.  `9..level set 5` will make you level 5 with 0 xp.\n",
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

    case "TAL":
      embed = discord.Embed(title="9..tal",
      description="This command will show you your talismans, their "\
                  "stat modifications, and their descriptions if you "\
                  "run it without arguments.\n\n"\
                  "To add a talisman to your character, do the following:\n"\
                  "`9..tal add <name> <the stat it modifies> "\
                  "<how much it modifies the stat> <optional description>`\n"\
                  "e.g. `9..tal add Cloak of Shadows dex +1` "\
                  "will give you a talisman called Clock of Shadows that increases "\
                  "your dexterity by 1.\n\n"\
                  "Your talisman can also have multiple stat modifications.\n"\
                  "e.g. `9..tal add Jeweled Necklace cha +1 luck +2 An enchanted "\
                  "necklace made of gems and gold.` will give you a talisman that "\
                  "enhances your charisma by 1 and your luck by 2, with a short "\
                  "description to boot.\n\n"
                  "To remove a talisman, do `9..tal rm <talisman number>`.\n"\
                  "e.g. `9..tal rm 1` will remove your TAL1.\n\n"\
                  "tip: f you have a longer description, it's ok to put it "\
                  "on a separate line, like this: \n"\
                  "```\n9..tal add Solstice Heart str +2 will +4\n"\
                  "The parts of this artificial heart are forged out of pure "\
                  "solstice steel, and carefully constructed by "\
                  "a clan of master craftsman over the span of 2 weeks. "\
                  "Some say that this heart can pump pure traxon through "\
                  "a person's veins.\n```",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "AFF":
      embed = discord.Embed(title="9..aff",
        description="This command will show you your current "\
              "afflictions, which stats they're impacting, and their descriptions"\
              "if you run it without arguments.\n\n"\
              "To add an affliction to your character, do the following: \n"\
              "`9..aff add <name> <tier> <the stat it modifies> "\
              "<how much it modifies the stat> <optional description>`\n"\
              "e.g. `9..tal add poisoned 2 str -3` "\
              "will give you the affliction 'poisoned II' "\
              "that decreases your strength by 3.\n\n"\
              "Your affliction can also affect multiple stats at once.\n"\
              "e.g. `9..aff add Delusional cha -1 will -2 A powerful curse "\
              "that blends together one's dreams and reality.` "\
              "will give you an affliction that "\
              "decreases your charisma by one and willpower by 2, with a short "\
              "description to boot. Note that you don't have to specify a tier.\n\n"
              "To remove an affliction, do `9..aff rm <affliction name>`.\n"\
              "e.g. `9..aff rm hobbled` will remove your Hobbled status.\n\n"\
              "Take note that the afflictions command will only take single "\
              "word names, so make sure to hyphenate any two-or-more-word "\
              "afflictions.\n",
        colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "REGISTER":
      embed = discord.Embed(title="9..register",
        description="This command will register a new character for you "\
                    "if one does not exist already in the database.\n\n"\
                    "Run this command with a single word for your name, "\
                    "like this: `9..register Felix`.\n\n"\
                    "Newly registered characters will always start at lv1.\n",
        colour=0xff6600)
  
      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "TICK":
      embed = discord.Embed(title="9..tick",
        description="This command will tick forward any persistent "\
                    "tickable effects by one round. Right now, the only "\
                    "such effect is bleeding, "\
                    "but there may be more in the future.\n",
        colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "REP":
      embed = discord.Embed(title="9..rep",
        description="This command will show you how much rep you currently have "\
                  "if you run it without arguments.\n\n"\
                  "If you run the command with a number, your rep will be "\
                  "modified by that number.\n"\
                  "e.g.  `9..rep +8` will make you gain 8 rep.\n",
        colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case _:
      embed = discord.Embed(title="Command not found",
        description=f"I don't recognize 9..{cmd.lower()} as one of my commands...",
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
  # tal = [name, stat, mod_amount, desc]
  printable = ""
  if len(char.tal) == 0:
    return "You don't have any talismans!\n"
  for i in range(len(char.tal)):
    cur_tal = char.tal[i]
    printable += f"**TAL{i+1} - {cur_tal[0]}**\n"
    for i in range(len(cur_tal[2])):
      if cur_tal[2][i] > 0:
        printable += '+'
      printable += f"{cur_tal[2][i]} {int_to_stat[cur_tal[1][i]]}\t"
    printable += "\n"
    if cur_tal[3] != "":
      printable += f"*{cur_tal[3]}*\n"
    printable += "\n"

  return printable

def printaff(char: Character):
  # aff = [name, tier, stat, mod_amount, desc]
  printable = ""
  if len(char.aff) == 0:
    return "You don't have any afflictions!\n"
  for i in range(len(char.aff)):
    cur_aff = char.aff[i]
    printable += f"**{cur_aff[0]} {cur_aff[1]}**\n"
    for i in range(len(cur_aff[2])):
      printable += f"{cur_aff[3][i]} {int_to_stat[cur_aff[2][i]]}\t"
    if len(cur_aff[2]) != 0:
      printable += "\n"
    if cur_aff[4] != "":
      printable += f"*{cur_aff[4]}*\n"
    printable += "\n"

  return printable