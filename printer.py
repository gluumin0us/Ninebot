from character import Character
import discord
import re
from random import randint
import math

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
    if debuff_mark[i] > 0:
      printable_stat += f"(+{str(debuff_mark[i])})"
    elif debuff_mark[i] < 0:
      printable_stat += f"({str(debuff_mark[i])})"
    printable.append(printable_stat)

  for i in range(len(char.tal)):
    printable.append(f"*TAL{i+1} - {char.tal[i][0]}*")
  printable.append(f"HP - {char.hp}/{char.max_hp}")
  if char.thp > 0:
    printable.append(f"THP - {char.thp}")
    
  for c_name in char.counter:
    counter = char.counter[c_name]
    if counter[-1] == 'FALSE':
      printable.append(printcounter(c_name, counter))

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
    return [printable, num_total]
    
  elif stat.isdigit() or stat.startswith('+') or stat.startswith('-'):
    result += int(stat)
    printable += f"{stat} Custom "

  elif stat in stat_to_int:
    int_stat = stat_to_int[stat]
    result += char.stat[int_stat]
    printable += f"{int_to_stat[int_stat]} "

  else:
    printable = "I don't think you're quite using the command correctly. "\
    "Refer to `9..help roll` for more details."
    return printable
    
  printable += f"Check: **-{result}+** :game_die:\n"

  if base == 1:
    printable += "Nat 1 :(\n"
  
  if base == 20:
    printable += "**NATURAL 20!**"
    
  return [printable, result]

def printhelp(cmd: str, requester) -> discord.Embed():
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
                "Adding `-s` at the end of most commands will make it not "\
                "print out a message, which might be helpful if you don't want to "\
                "clutter up a chat or want more control over your macros.\n\n"\
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
        "  Prints out, or modifies, your rep count.\n"\
        "__**9..cc**__\t"\
        "  Prints out, adds, removes, or modifies, a custom counter.\n"\
        "__**9..macro**__\t"\
        "  Prints out, adds, removes, or shares, a macro.\n"\
        "__**9..print**__\t"\
        "  Prints out a message in the current channel.\n",
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
                  "e.g. `9..roll +4` will return a d20 dice roll with +4 added.\n\n"\
                  "If you want to roll dice other than a d20, "\
                  "and/or if you want to roll multiple dice at once, just do "\
                  "`9..roll <amount of dice to roll>d<type of dice to roll>`.\n"\
                  "e.g. `9..roll 4d6` will roll 4 six-sided dice.\n",
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
                  "```9..tal add <name> <the stat it modifies> "\
                  "<how much it modifies the stat> \n"\
                  "<optional description (on a new line)>```\n"\
                  "e.g. `9..tal add Cloak of Shadows dex +1` "\
                  "will give you a talisman called Clock of Shadows that increases "\
                  "your dexterity by 1.\n\n"\
                  "Your talisman can also have multiple stat modifications.\n"\
                  "e.g. ```9..tal add Jeweled Necklace cha +1 luck +2\n"\
                  "An enchanted "\
                  "necklace made of gems and gold.``` "\
                  "will give you a talisman that "\
                  "enhances your charisma by 1 and your luck by 2, with a short "\
                  "description to boot.\n\n"
                  "To remove a talisman, do `9..tal rm <talisman number>`.\n"\
                  "e.g. `9..tal rm 1` will remove your TAL1.\n\n"\
                  "Note: Your talisman descriptions must be put "\
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

    case "CC":
      embed = discord.Embed(title="9..cc",
        description="This command will show all your current custom counters if you run it without arguments. A custom counter is where you can keep track of how many of something there are, whether it be how many arrows your have left or how many scaffold rooms you've explored. You can also print out a specific counter by doing `9..cc <name of the counter>`. \n\nIf you want to create a new counter, you can do so with `9..cc add <name of the counter (single word)> <arguments>`. \nIf you want to remove an existing counter, do `9..cc rm <name of the counter>`.\nIf you want to add or subtract value to a counter, do `9..cc <name of the counter> <number>`.\n\nArguments are different ways to customize your counter, you can have multiple arguments in any order. Here's a list: \n- `max <number>`: specifies the maximum value of the counter. IMPORTANT: This is a required argument, but if for some reason you've made a counter without specifing it, it defaults to 10.\n- `min <number>`: specifies the minimum value of the counter. Defaults to 0.\n- `val <number>`: specifies the starting value of the counter. Defaults to the max value. \n- `display <graphic>`: specifies if you want the counter to be displayed by graphics. Your options for graphics are: ✦star✧, ◈diamond◇, ◉circle◎, and ☒checkbox☐. If not specified, defaults to just printing out numbers. NOTE: not recommended for counters with a maximum higher than 20.\n- `milestone <array>`: if this option is specified, turns the counter into milestone style (think how your XP counter works), with each number in your milestone array being the next 'level-up' threshhold. Make sure your arrays don't have any spaces in them, like this: `[5,10,16,24,30]`, or else Nine will think it's multiple separate arguments.\n- `hidden <true/false>`: specifies if you want this counter to show up on your character sheet. If you specify true, then you won't be able to see it on your `9..char`, but everything else about it works the same. Defaults to false.\n\nCustom counters can be a bit confusing to make sense of at the start, so here are some examples of what a cc command might look like:\n```\n9..cc add Rations max 5 val 4 display circle hidden true\n```\nfor a custom counter called 'Rations' that has a maximum value of 5, current value of 4, each ration displayed as circles, and it doesn't show up on `9..char`:\nRations - ◉◉◉◉◎\n",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "MACRO":
      embed = discord.Embed(title="9..macro",
      description="This command lets you make macros. A macro, at its simplest, is one command that lets you call a bundle of one or more subcommands. It's quite powerful and lets you do a lot of things, but it's also hard to teach in a single help page. If you want to learn more (which I highly recommend), please just reach out to Simon (@gluumin0us), the author of this bot.\n\nThat being said, to see all the macros you have, do `9..macro`.\n\nTo view a specific macro and see its subcommands, do `9..macro <macro name>`.\n\nTo create a new macro, do: ```\n9..macro add <macro name (single word)>\n- <subcommand 1>\n- <subcommand 2>\n...\n```where each subcommand is another `9..` command that will be called by the macro.\n\nYou can have subcommands of a macro receive arguments from the macro call by putting `arg<number>` after them. For example, if you have the following macro: ```9..macro add roll_tracker\n- 9..cc add arg1 max 20 min 1 val 1```Calling `9..roll_tracker Dex` will make a custom counter named Dex, since the `9.cc` subcommand is taking in the first argument of the macro call as its name.\n\nYou can also take outputs from your subcommands by putting `-> <output variable name>` after the subcommand, and use the output as you would arguments in subsequent subcommands.\n\nTo actually call the macro, simply do `9..<macro name>`.\n",
      colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed

    case "PRINT":
      embed = discord.Embed(title="9..print",
      description="This command is quite simple. It prints out, in whichever chat you called this command in, whatever you put after the command.\n\nFor example, `9..print Hello World!` will have Nine say 'Hello World!'. \n\nThis is mainly intended to be used in macros.\n",
      colour=0xff6600)
    
      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed
  
    case _:
      embed = discord.Embed(title="Command not found",
        description=f"I don't recognize 9..{cmd.lower()} as one of my commands...",
        colour=0xff6600)

      embed.set_author(name=req_name, icon_url=req_avatar)
      return embed
      
def printleg(char: Character) -> str:
  printable = f"{char.name}'s Legendary bonuses: \n"
  printable += f"Strength: +{char.legendary[0]}\n"
  printable += f"Dexterity: +{char.legendary[1]}\n"
  printable += f"Charisma: +{char.legendary[2]}\n"
  printable += f"Intelligence: +{char.legendary[3]}\n"
  printable += f"Attack: +{char.legendary[4]}\n"
  printable += f"Willpower: +{char.legendary[5]}\n"
  printable += f"Luck: +{char.legendary[6]}\n"
  return printable

def printtal(char: Character) -> str:
  # tal = [name, stat, mod_amount, desc]
  printable = ""
  if len(char.tal) == 0:
    return "You don't have any talismans!\n"
  for i in range(len(char.tal)):
    cur_tal = char.tal[i]
    printable += f"**TAL{i+1} - {cur_tal[0]}**\n"
    if len(cur_tal[2]) > 0:
      for i in range(len(cur_tal[2])):
        if cur_tal[2][i] > 0:
          printable += '+'
        printable += f"{cur_tal[2][i]} {int_to_stat[cur_tal[1][i]]}\t"
      printable += "\n"
    if cur_tal[3] != "":
      printable += f"*{cur_tal[3]}*\n"
    printable += "\n"

  return printable

def printaff(char: Character) -> str:
  # aff = [name, tier, stat, mod_amount, desc]
  printable = ""
  if len(char.aff) == 0:
    return "You don't have any afflictions!\n"
  for i in range(len(char.aff)):
    cur_aff = char.aff[i]
    printable += f"**{cur_aff[0]} {cur_aff[1]}**\n"
    for i in range(len(cur_aff[2])):
      if cur_aff[3][i] > 0:
        printable += "+"
      printable += f"{cur_aff[3][i]} {int_to_stat[cur_aff[2][i]]}\t"
    if len(cur_aff[2]) != 0:
      printable += "\n"
    if cur_aff[4] != "":
      printable += f"*{cur_aff[4]}*\n"
    printable += "\n"

  return printable

def printcheck(checkbook: dict) -> str:
  printable = ""
  for name in checkbook:
    printable += f"{name}: {checkbook[name]}\n"
  return printable

def printhp(char: Character) -> str:
  printable = ""
  hp_percent = math.floor((char.hp / char.max_hp) * 16)
  printable += "⧼"
  for i in range(16):
    if i < hp_percent:
      printable += "▓"
    else:
      printable += "░"
  printable += "⧽"
  for i in range(math.ceil(char.thp / 10)):
    printable += "❱"
  printable += f"\nHP - {char.hp} / {char.max_hp}  "
  if char.thp > 0:
    printable += f"❬{char.thp}❭"
  return printable

def printxp(char: Character) -> str:
  printable = ""
  xp_til_next = 240 * char.level - 100
  xp_percent = math.floor((char.xp / xp_til_next) * 16)
  printable += f"{char.level} ⧼"
  for i in range(16):
    if i < xp_percent:
      printable += "▓"
    else:
      printable += "░"
  printable += f"⧽ {char.level + 1}\n"
  # printable += f"LV {char.level}, {char.xp}/{xp_til_next}"
  return printable
  pass

def printallcounter(char: Character) -> str:
  # Counter: name: [min, max, val, display, is_hidden]
  printable = ""
  if len(char.counter) == 0:
    printable = "You don't have any custom counters!"
  else:
    for c_name in char.counter:
      printable += printcounter(c_name, char.counter[c_name])[0]
      printable += "\n"
  return printable

def printcounter(c_name, c) -> str:
  # name: [min, max, val, display, milestone, is_hidden]
  display = {
    'STAR': ["✦", "✧"],
    'DIAMOND': ["◈", "◇"],
    'CIRCLE': ["◉", "◎"],
    'CHECKBOX': ["☒", "☐"]
  }
  printable = ""
  min = c[0]
  max = c[1]
  val = c[2]
  milestone = c[4]
  if milestone:
    if milestone[0] < min:
      return "Your milestone minimum is smaller than your counter minimum!"
    if milestone[-1] > max:
      return "Your miletone maximum is higher than your counter maximum!"
    if milestone[-1] < max:
      milestone.append(max)
    for i in range(len(milestone)):
      if milestone[i] == val:
        if val != max:
          printable += f"{c_name} - M{i+1}, 0/{milestone[i+1] - milestone[i]}\n"
        else:
          printable += f"{c_name} - M{i+1}, **MAX**\n"
        if c[3] in display:
          if val != max:
            printable += f"{i+1} "
            for j in range(milestone[i+1] - milestone[i]):
              printable += display[c[3]][1]
            printable += f" {i+2}"
          else:
            printable += f"{i} "
            for j in range(milestone[i] - milestone[i-1]):
              printable += display[c[3]][0]
            printable += f" {i+1}"
        return [printable, i+1]
      elif milestone[i] > val:
        if i > 0:
          min = milestone[i-1]
        printable += f"{c_name} - M{i}, "\
        f"{val - min}/{milestone[i] - min}\n"
        if c[3] in display:
          printable += f"{i} "
          for j in range(milestone[i] - min):
            if j < (val-min):
              printable += display[c[3]][0]
            else:
              printable += display[c[3]][1]
          printable += f" {i+1}"
        return [printable, i]
      
          

  printable = f"{c_name} - "
  if c[3] == 'NUM':
    printable += f"{val}/{max}"
  elif c[3] in display:
    for i in range(max):
      if i < val:
        printable += display[c[3]][0]
      else:
        printable += display[c[3]][1]
  else:
    printable += f"{val}/{max}\nDisplay option '{c[3].lower()}' not recognized."
  return [printable, val]

def printlist(list) -> str:
  pass