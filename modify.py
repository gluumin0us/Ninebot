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

def modxp(char: Character, xp_change: int):
  printable = ""
  #TODO
  return printable