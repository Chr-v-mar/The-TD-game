import pygame

background_colour = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
(width, height) = (1500, 750)


class GameGUI:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('TD game')
        self.screen = pygame.display.set_mode([width, height])
        self.screen.fill(background_colour)
        self.pos = (0, 0)
        self.circle_list = []
        self.running = True

    def main_loop(self):
        while self.running:
            self.handle_inputs()
            self.draw()

        pygame.quit()

    def handle_inputs(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if pygame.mouse.get_pressed()[0]:
            print('click')
            self.pos = pygame.mouse.get_pos()
            print(self.pos)
            self.circle_list.append(self.pos)

    def draw(self):
        self.draw_background()
        self.draw_towers()

        pygame.display.flip()

    def draw_background(self):
        self.screen.fill(background_colour)

    def draw_towers(self):
        self.pos = pygame.mouse.get_pos()
        for x, y in self.circle_list:
            pygame.draw.circle(self.screen, red, (x, y), 10)
        pygame.draw.circle(self.screen, blue, (self.pos[0], self.pos[1]), 10)



if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()

