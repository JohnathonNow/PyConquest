# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
import time
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def coordinates(screen, x, y):
  fontobject = pygame.font.SysFont("monospace", 15)
  pygame.draw.rect(screen, (0,0,0), (20,20,85,25), 0)
  pygame.draw.rect(screen, (255,255,255), (20,20,85,25), 1)
  drawText(screen, str(x) + ', ' + str(y), (255,255,255), (25,25,75,20), fontobject)
  #pygame.display.flip()

def message_box(screen, message):
  fontobject = pygame.font.SysFont("monospace", 15)
  pygame.draw.rect(screen, (0,0,0), (150,100,350,250), 0)
  pygame.draw.rect(screen, (255,255,255), (150,100,350,250), 3)
  drawText(screen, message, (255,255,255), (155,105,340,240), fontobject)
  drawText(screen, "Press ENTER to continue...", (255,255,255), (250,330,340,240), fontobject)
  pygame.display.flip()
  while 1:
    inkey = get_key()
    if inkey == K_RETURN:
      break

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.SysFont("monospace", 15)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + ''.join(current_string))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + ''.join(current_string))
  return ''.join(current_string)

def drawText(screen, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        if y + fontHeight > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        screen.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        text = text[i:]
 
    return text

def main():
  screen = pygame.display.set_mode((320,240))

if __name__ == '__main__': main()
