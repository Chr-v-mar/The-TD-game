from dataclasses import dataclass
from itertools import pairwise
import math

@dataclass
class Position:
    x: float = 0
    y: float = 0

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"


class Entity:
    def __init__(self):
        pass


class Enemy:
    
    def __init__(self):
        self._line_segment = ""
        self._line_progress = 0
        self._position = (0,0)
        self._V = 0
        self._Hp = 100
        
    def progress_line(self):
        self._line_progress += self._V/D*dt
        
    def progress_segment(self):
        if self._line_progress >= 1:
            if self._line_segment.IsEnd() == True:
                Base.take_damage(self._Hp)
            #else:
                #increment segment by 1
                
    def take_damage(self,Damage):
        self._Hp -= Damage
        
    @property   
    def is_dead(self):
        if self._Hp <= 0:
            return True
        return False
    
    
    
class Base:
    def __init__(self):
        self._Health = 250
        
    def take_damage(self, damage):
        self._Health -= damage
        
    @property
    def is_gameover(self):
        if self._Health <= 0:
            return True
        return False
            

    


class Tower:
    
    def __init__(self):
        self._Cost = 0
        self._Upgrade_Cost = 0
        self._Sell_Price = 0
        self._Damage = 0
        self._Range = 0 #Rad of circle
        self._Firerate = 0
        self._Position = Position
        self._ObscureDetection = False
        self._ArmourPierce = False
        self._Level = 0
        self._Max_Level = False
    """    
    def __init__(self, Cost, Damage, Range, Firerate, Postition: tuple[int,int], Base_Obs=False, Base_AP=False):
        self._Cost = Cost
        self._Sell_Price = Cost//2
        self._Damage = Damage
        self._Range = Range #Rad of circle
        self._Firerate = Firerate
        self._Position = Position
        self._ObscureDetection = Base_Obs
        self._ArmourPierce = Base_AP
        self._Level = 0
        
    All of this is a previous iteration.
    """    
    def calculate_range_circle(self):
        circle = (self._Range**2)*math.pi
        
    def select_target(self):
        pass
        
    @property
    def recalculate_sell_value(self):

        self._Sell_Price = (self._Cost)//2
        
    def Upgrade_Tower(self):
        if not self._Max_Level:
            if Game.currentcash >= self._Upgrade_Cost:
                Game.currentcash -= self._Upgrade_Cost
                self.Level_up((self._Level) + 1)
        
    def Level_up(self):
        pass
    
class placeholder1(Tower):
    
    def __init__(self):
        self._TowerType = "placeholder1" #-please rename this later!!!#
        self._Cost = 250
        self._Upgrade_Cost = 300
        self._Sell_Price = 250//2
        self._Damage = 50
        self._Range = 15 #Rad of circle
        self._Firerate = 0.4
        self._ObscureDetection = False
        self._ArmourPierce = False

                    
    def Level_up(self,level):
        """

        Parameters
        ----------
        level

        Returns
        -------

        """
        self._Level = level
        match level:
            
            case 1:
                self._Damage += 50
                self._Upgrade_Cost = 600
                
            case 2:
                self._Damage += 100
                self._Range += 2
                self._Upgrade_Cost = 900
                
            case 3:
                self._Range += 2
                self._Firerate -= 0.2
                self._Max_Level = True


class Game:
    def __init__(self):
        self.tracks = []
        self.enemies = []
        self.currentcash = 0
        self.wave = 0
        self.payout = False
        self._WaveCash = 100

    def add_enemy(self, enemy: Enemy):
        self.enemies.append(enemy)
        if enemy.path not in self.tracks:
            self.tracks.append(enemy.path)

    def progress(self, delta_time):
        for enemy in self.enemies:
            enemy.progress(delta_time)
            
    def progress_wave(self):
        self.wave += 1
        self.payout = False
        
    @property
    def wave_payout(self):
        if self.payout == False:
            self.currentcash += self._WaveCash
            self.payout = True
    
    
    def increment_Wave_Cash(self):
        self._WaveCash = self._WaveCash*(1.25**self.wave)

    def print_enemy_positions(self):
        for i, enemy in enumerate(self.enemies):
            print(f'Enemy {i} at {enemy.position};', end=' ')
        print()

    def set_up(self):
        game_path = Path([Position(0, 0),
                          Position(50, 0),
                          Position(50, 50),
                          Position(100, 100),
                          ])
        self.add_enemy(Enemy(game_path, speed=20))
        self.add_enemy(Enemy(game_path, line=1, speed=100))