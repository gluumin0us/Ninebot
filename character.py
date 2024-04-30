class Character:
  def __init__(self, name: str, level: int, xp: int):
    self.name = name
    self.level = level
    self.xp = xp
    self.xp_til_next = 240 * self.level - 100
    self.max_hp = 40 + self.level * 5
    self.hp = self.max_hp
    self.thp = 0
    self.mod = [0, 0, 0, 0, 0, 0, 0]
    self.legendary = [0, 0, 0, 0, 0, 0, 0]
    self.stats = [2 + self.level + self.legendary[0] + self.mod[0],
                  2 + self.level + self.legendary[1] + self.mod[1],
                  2 + self.level + self.legendary[2] + self.mod[2],
                  2 + self.level + self.legendary[3] + self.mod[3],
                  2 + self.level + self.legendary[4] + self.mod[4],
                  2 + self.level + self.legendary[5] + self.mod[5],
                  2 + self.level + self.legendary[6] + self.mod[6]]
    self.tal = []
    self.effect = []
    self.ss = ""
    self.pt = ["", "", "", ""]

  def talisman(self, name: str, stat: int, stat_amount: int):
    self.tal.append(name)
    self.mod[stat] += stat_amount