import json
import pygame
from pprint import pprint
from random import randint
FPS = 60
clock = pygame.time.Clock()
#map1 = "Berebav2.json"
background_colour = (155,255,200)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
(width, height) = (1500, 750)
x = 400
y = 400
width1 = 50
height1 = 200
rect = pygame.Rect(x,y,width1,height1)
points1 = [(000, 200), (400, 100), (400,200), (000,300)]
points2 = [(400, 200), (400, 100), (700,400), (600,400)]
points3 = [(700, 400), (600, 400), (900,550),(1100,600),  (1000,550)]
points4 = [(1100, 600), (1000, 550), (1500,550), (1500,600)]


pointdict = {1: (points1,1), 2: (points2,2), 3: (points3,3), 4: (points4,4)}
pointpriority = 0

line1 = ((100,250), (300,250), 3)
#pointrand = [(randint(100,750), randint(100,750)), (randint(100,750), randint(100,750)), (randint(100,1500),randint(100,1500)), (randint(100,1500),(randint(100,1500)))]

#path = {"One": [200, 400, 50, 50], "Two": [300, 500, 50, 50]}
#with open("Berebav2.json", "w") as write_file:
    #json.dump(path, write_file)

#with open(map1,"r") as map_data:
    #data = json.load(map_data)
    #map_data.close()
    #pprint(data)
    

running = True

pygame.init()
pygame.display.set_caption('TD game')
screen = pygame.display.set_mode([width, height])
screen.fill(background_colour)
while running:
    dt = clock.tick(FPS)/1000 
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    screen.fill("gold")
    #pygame.draw.rect(screen, "red", rect)
    #pygame.draw.polygon(screen, "orange", points1)
    #pygame.draw.polygon(screen, "blue", points2)
    #pygame.draw.polygon(screen, "brown", points3)
    #pygame.draw.polygon(screen, "purple", points4)
    #pygame.draw.polygon(screen, "green", pointrand)
    pygame.draw.line(screen, "red",(000,250), (300,250), 20)
    pygame.draw.circle(screen,"red",(300,250),10)
    pygame.draw.line(screen, "red",(300,250), (600,650), 20)
    pygame.draw.circle(screen,"red",(600,650),8)
    pygame.draw.line(screen, "red",(600,650), (1500,750), 20)
    pygame.display.flip()
    
    
pygame.quit()
