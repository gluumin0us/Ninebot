class Character:
  def __init__(self, name: str, level: int, xp: int):
    self.name = name
    self.level = level
    self.xp = xp
    self.xp_til_next = 240 * self.level - 100
    self.max_hp = 40 + self.level * 5
    self.hp = self.max_hp
    self.thp = 0
    self.str = 2 + self.level + self.legendary[0]
    self.dex = 2 + self.level + self.legendary[1]
    self.cha = 2 + self.level + self.legendary[2]
    self.int = 2 + self.level + self.legendary[3]
    self.att = 2 + self.level + self.legendary[4]
    self.wil = 2 + self.level + self.legendary[5]
    self.luc = 2 + self.level + self.legendary[6]
    self.tal = []
    self.effect = []
    self.ss = ""
    self.pt1 = ""
    self.pt2 = ""
    self.pt3 = ""
    self.pt4 = ""
    bonus = [0, 0, 0, 0, 0, 0, 0]
    self.mod = [[], [], [], [], [], [], [], [], []]
    self.legendary = bonus