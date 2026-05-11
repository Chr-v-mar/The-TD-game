import tower_do

class Enemy:
    def __init__(self, name, health, position):
        self.name = name
        self.health = health
        self.enemy_position = position

    def take_damage(self, damage):
        self.health -= damage
        return f"{self.name} took {damage} damage"




class Tower(object):
    def __init__(self, tower_name, damage, range):
        self.tower_name = tower_name
        self.damage = damage
        self.stunned = False
        self.range = range

    def shoot(self, enemy):
        if not self.stunned:
            if enemy and enemy.health > 0:
                result = enemy.take_damage(self.damage)
                print(result)
            else:
                print("No valid target")
        else:
            return "Tower is currently stunned."

    def select_target(self, enemies):
        target = None
        for enemy in enemies:
            if enemy.health > 0:
                target = enemy
                break
        return target

    def check_range(self, enemy_cd):
        if abs(enemy_cd[0]) < self.range and abs(enemy_cd[1]) < self.range:
            pass #breadth first search






zombie = Enemy("Zombie", 100, (100,100))