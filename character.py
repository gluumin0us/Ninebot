class Character:
  def __init__(self, name: str, level: int, xp: int):
    self.name = name
    self.level = level
    self.xp = xp
    self.max_hp = 40 + self.level * 5
    self.hp = self.max_hp
    self.thp = 0
    self.mod = [0, 0, 0, 0, 0, 0, 0]
    self.legendary = [0, 0, 0, 0, 0, 0, 0]
    self.str = 2 + self.level
    self.dex = 2 + self.level
    self.cha = 2 + self.level
    self.int = 2 + self.level
    self.att = 2 + self.level
    self.wil = 2 + self.level
    self.luc = 2 + self.level
    self.tal = []
    self.effect = []
    self.ss = ""
    self.pt = ["", "", "", ""]
    self.id = ""

  def talisman(self, name: str, stat: int, stat_amount: int):
    self.tal.append(name)
    self.mod[stat] += stat_amount

  def restat(self):
    self.str = 2 + self.level + self.legendary[0] + self.mod[0]
    self.dex = 2 + self.level + self.legendary[1] + self.mod[1]
    self.cha = 2 + self.level + self.legendary[2] + self.mod[2]
    self.int = 2 + self.level + self.legendary[3] + self.mod[3]
    self.att = 2 + self.level + self.legendary[4] + self.mod[4]
    self.wil = 2 + self.level + self.legendary[5] + self.mod[5]
    self.luc = 2 + self.level + self.legendary[6] + self.mod[6]