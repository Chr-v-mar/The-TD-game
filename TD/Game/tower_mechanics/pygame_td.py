import pygame

background_colour = (255,255,255)
red = (255,0,0)
(width, height) = (1500, 750)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TD game')
screen.fill(background_colour)
pos = (0, 0)
circle_list = []

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
          print('left')
          pos = pygame.mouse.get_pos()
          print(pos)
          circle_list.append(pos)


    pos = pygame.mouse.get_pos()
    screen.fill(background_colour)
    for x,y in circle_list:
        pygame.draw.circle(screen, red, (x, y), 10)
    pygame.draw.circle(screen, red,(pos[0],pos[1]),10)

    pygame.display.flip()