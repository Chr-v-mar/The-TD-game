class Tower:
    def __init__(self, range, damge, cooldown, firerate, cost):
        self.range = range
        self.damage = damge
        self.cooldown = cooldown
        self.firerate = firerate
        self.cost = cost
        self.properties = None
        self.prop_dict = {"Burn":(1,0.5), "Bleed":(4,2)}    #property dictionary for DOT eligibility
        self.cost_per_upgrade_rate = 0.7
        self.level = 1
        self.sell_return = cost//3
        self.targetting = ["first", "last", "strongest", "weakest"]
        self.target = self.targetting[0]

    def check_dot_eligible(self):
        if self.properties != None:
            self.Damage_Over_Time(self.prop_dict[self.properties][0], self.prop_dict[self.properties][1])

        else:
            return "No DOT"

    def cost_change(self):
        #return self.cost + self.cost **(self.cost_per_upgrade_rate * self.level)
        new_cost = self.cost* self.cost_per_upgrade_rate *(2.71828 ** (self.level * self.cost_per_upgrade_rate))
        self.sell_return = new_cost//1.5
        return new_cost

    def Damage_Over_Time(self, damage, duration):
        pass

    def target_priority_change(self,count):
        self.target = self.targetting[count % len(self.targetting)]


