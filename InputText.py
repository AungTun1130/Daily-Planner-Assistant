import pygame
import types
import sys

class Button:
    def __init__(self, screen, text_color, color_highlight, color_default, x, y, radius=None, width=None,
                 height=None, mouse_pos=None):
        self.screen = screen
        self.color_highlight = color_highlight
        self.color_default = color_default
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.mouse_pos = mouse_pos
        self.text_color = text_color
        self.radius = radius

    def text_size(self, size):
        smallfont = pygame.font.SysFont('Corbel', size)
        self.text = smallfont.render(self.string, True, self.text_color)

    def create_rect_input_text(self):
        x = self.x
        y = self.y
        mouse_pos = self.mouse_pos
        width = self.width
        height = self.height
        screen = self.screen
        color_highlight = self.color_highlight
        color_default = self.color_default
        string = self.text

        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            pygame.draw.rect(screen, color_highlight, [x, y, width, height])

        else:
            pygame.draw.rect(screen, color_default, [x, y, width, height],2)

        # superimposing the text onto our button
        screen.blit(string, (x + width / 2 - string.get_width() / 2, y + height / 2 - string.get_height() / 2))

    def button_click(self):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(self.mouse_pos):
            return True
        else:
            return False
