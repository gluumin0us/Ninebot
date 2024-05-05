from character import Character


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
  char.restat()
  if old_level < char.level:
    printable += "**Level Up!**\n"
    char.max_hp = 40 + char.level * 5
    char.hp = char.max_hp
  elif old_level > char.level:
    printable += "Level Down!\n"
    char.max_hp = 40 + char.level * 5
    char.hp = char.max_hp
  printable += f"Level - LV{old_level}, {old_xp}/{240 * old_level - 100} -> "
  printable += f"**LV{char.level}, {char.xp}/{240 * char.level - 100}**\n"
  return printable