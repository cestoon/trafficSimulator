import pygame
from src.trafficSimulator import Simulation, TURN_LEFT, TURN_RIGHT, turn_road


class Button():
    def __init__(self, x, y, plus_image, plus_scale):
        width = plus_image.get_width()
        height = plus_image.get_height()
        self.plus_image = pygame.transform.scale(plus_image, (int(width * plus_scale), int(height * plus_scale)))
        self.plus_rect = self.plus_image.get_rect()
        self.plus_rect.topleft = (x, y)
        self.plus_clicked = False
        self.sim = Simulation()

    def draw(self, surface, sim, text_font):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.plus_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.plus_clicked == False:
                self.plus_clicked = True
                action = True
                print('unbalance traffic')

        if pygame.mouse.get_pressed()[0] == 0:
            self.plus_clicked = False


        # draw button on screen
        surface.blit(self.plus_image, (self.plus_rect.x, self.plus_rect.y))

        return action
