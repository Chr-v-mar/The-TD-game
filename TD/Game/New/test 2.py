import pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18, bold=True)
running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
   fps_text = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
   screen.fill((0, 0, 0))
   screen.blit(fps_text, (10, 10))
   pygame.display.flip()
   clock.tick(60)
pygame.quit()