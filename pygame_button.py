import pygame
import types
import sys


class Button:
    def __init__(self, screen=None, string="example", text_color=(0, 0, 0), color_highlight=(255, 255, 255),
                 color_default=(200, 200, 200), x=0, y=0, radius=None, width=None, height=None, mouse_pos=None):
        self.screen = screen
        self.color_highlight = color_highlight
        self.color_default = color_default
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.string = string
        self.mouse_pos = mouse_pos
        self.text_color = text_color
        self.radius = radius
        self.selected = False
        self.text = string

    def text_size(self, size):
        smallfont = pygame.font.SysFont('Corbel', size)
        self.string = smallfont.render(self.text, True, self.text_color)

    def set_screen(self,screen):
        self.screen = screen

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_Button_width(self, width):
        self.width = width

    def create_rect_btn(self):

        if not self.selected:
            if self.x <= self.mouse_pos[0] <= self.x + self.width and self.y <= self.mouse_pos[1] <= self.y + self.height:
                pygame.draw.rect(self.screen, self.color_highlight, [self.x, self.y, self.width, self.height])

            else:
                pygame.draw.rect(self.screen, self.color_default, [self.x, self.y, self.width, self.height])
        else:
            pygame.draw.rect(self.screen, (135, 206, 250), [self.x, self.y, self.width, self.height])

        # superimposing the text onto our button
        self.screen.blit(self.string, (self.x + self.width / 2 - self.string.get_width() / 2, self.y + self.height / 2 - self.string.get_height() / 2))

    def mouse_pos_update(self, mouse):
        self.mouse_pos = mouse

    def button_click(self):
        if self.x <= self.mouse_pos[0] <= self.x + self.width and self.y <= self.mouse_pos[1] <= self.y + self.height:
            self.selected = True
            return True
        else:
            self.selected = False
            return False

    def get_selected(self):
        return self.selected

    def set_selected(self,bool):
        self.selected = bool

    def get_name(self):
        return self.text