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
    self.stat = [0, 0, 0, 0, 0, 0, 0]
    self.tal = []
    self.aff = []
    self.ss = ""
    self.pt = ["", "", "", ""]
    self.id = ""