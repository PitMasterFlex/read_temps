#   Copyright 2016 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os

import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)


class LocalDisplay(object):

    def __init__(self, width=None, height=None, font_size=None):
        if width is None:
            width = 320
        if height is None:
            height = 240
        if font_size is None:
            font_size = 60
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.init()
        pygame.mouse.set_visible(False)
        self.lcd = pygame.display.set_mode((width, height))
        self.lcd.fill((0, 0, 0))
        self.font_big = pygame.font.Font(None, font_size)
        pygame.display.update()
        self.background = pygame.Surface(self.lcd.get_size())
        self.background = self.background.convert()
        self.background.fill(WHITE)

    @staticmethod
    def quit():
        """
        Ends the app.

        :return:
        """
        raise SystemExit

    def check_events(self):
        """
        Checks the event system for various events.

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.quit()

    def set_display_msg(self, msg):
        """
        Sets a provided message on the lcd screen.

        :param msg: String of the message you wish to display.
        :return:
        """
        screen = pygame.display.get_surface()
        screen.fill(pygame.Color("black"))
        text_surface = self.font_big.render(msg, True, WHITE)
        rect = text_surface.get_rect(center=(160, 120))
        self.lcd.blit(text_surface, rect)
        pygame.display.update()


if __name__ == "__main__":
    import time
    scr = LocalDisplay()
    c = 1
    try:
        while True:
            scr.check_events()
            scr.set_display_msg("Hello world: {}".format(c))
            time.sleep(2)
            c += 1
    except KeyboardInterrupt:
        print
        raise SystemExit
