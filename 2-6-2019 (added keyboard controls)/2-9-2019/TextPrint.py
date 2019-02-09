import pygame
import CF

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, CF.BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def print_red(self, screen, textString):
        textBitmap = self.font.render(textString, True, CF.RED)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def print_green(self, screen, textString):
        textBitmap = self.font.render(textString, True, CF.GREEN)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
