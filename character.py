import discord

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
    self.stat = [0, 0, 0, 0, 0, 0, 0]
    self.tal = []
    self.aff = []
    self.rep = 0
    self.pt = ["", "", "", ""]
    self.id = ""
    self.update_message = []

