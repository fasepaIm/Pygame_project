import pygame

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 190, 58)
        
    def text_print(self, screen, x, y, message, font_type):
        text = font_type.render(message, True, (0, 0, 0))
        screen.blit(text, (x + 10, y + 10))

    def draw(self, screen, x, y, message, font, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0]:
                if action == quit:
                    pygame.quit()
                    quit()
                else:
                    pygame.time.delay(300)
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        self.text_print(screen, x, y, message, font)
