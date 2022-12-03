import pygame


class Button():
    def __init__(self, x, y, plus_image, minus_image, plus_scale, minus_scale):
        width = plus_image.get_width()
        height = plus_image.get_height()
        self.plus_image = pygame.transform.scale(plus_image, (int(width * plus_scale), int(height * plus_scale)))
        self.plus_rect = self.plus_image.get_rect()
        self.plus_rect.topleft = (x+190, y)
        self.plus_clicked = False

        self.minus_image = pygame.transform.scale(minus_image, (int(width * minus_scale), int(height * minus_scale)))
        self.minus_rect = self.minus_image.get_rect()
        self.minus_rect.topleft = (x+210, y)
        self.minus_clicked = False

    def draw(self, surface, vehicle_pool, text_font):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.plus_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.plus_clicked == False:
                self.plus_clicked = True
                action = True
                vehicle_pool.v_max += 1
                vehicle_pool.v_realspeed = round(vehicle_pool.v_max * 5)
                # generator.v_max += 1
                print('increase 1')
                if vehicle_pool.v_max >= 7:
                    vehicle_pool.v_max = 7

        if pygame.mouse.get_pressed()[0] == 0:
            self.plus_clicked = False

        if self.minus_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.minus_clicked == False:
                self.minus_clicked = True
                action = True
                vehicle_pool.v_max -= 1
                vehicle_pool.v_realspeed = round(vehicle_pool.v_max * 5)
                print('decrease 1')
                if vehicle_pool.v_max <= 2:
                    vehicle_pool.v_max = 2

        if pygame.mouse.get_pressed()[0] == 0:
            self.minus_clicked = False

        # draw button on screen
        surface.blit(self.plus_image, (self.plus_rect.x, self.plus_rect.y))
        surface.blit(self.minus_image, (self.minus_rect.x, self.minus_rect.y))

        # To draw text
        text_fps = text_font.render(f'max_velocity={vehicle_pool.v_realspeed}km/h range[5˜40]', False, (0, 0, 0))
        surface.blit(text_fps, (self.plus_rect.x - 310, self.plus_rect.y))

        return action
