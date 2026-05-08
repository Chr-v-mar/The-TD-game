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

    def shoot(self, enemy):
        if enemy and enemy.health > 0:
            result = enemy.take_damage(self.damage)
            print(result)
        else:
            print("No valid target")

    def select_target(self, enemies):
        target = None
        for enemy in enemies:
            if enemy.health > 0:
                target = enemy
                break
        return target