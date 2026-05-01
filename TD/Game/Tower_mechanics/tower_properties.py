class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        return f"{self.name} took {damage} damage"



class Tower(object):
    def __init__(self, tower_name, damage):
        self.tower_name = tower_name
        self.damage = damage

    def shoot(self,enemy_name):
        enemy_name.take_damage(self.damage)

    def select_target(self):
        target = None