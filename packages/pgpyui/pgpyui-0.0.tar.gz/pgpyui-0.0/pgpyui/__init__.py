# pgpyui.
# Code example.
#   Button:
#       button.check_events(event: pygame.event.Event)  \
#       button.draw(window)                             / Update button
# 
#   TextArea:
#       TextArea.check_events(event: pygame.event.Event)  \
#       TextArea.draw(window)                             / Update TextArea


"""
pgpyui is an add-on module for pygame to create a user interface.
The creator is Memdved (Vilyukov Mikhail).
Mail - mixail.vilyukov@icloud.com
"""


import pygame
from typing import Callable


class TextArea:
    """
    A class for creating a Text Area.

    It is a multi-line control
    for editing plain text.

    :param position: Position of text area. Can be tuple[int, int].
    :param size: Size of Text Area box. can be tuple[unt, int].
    :param font_size: Size of font. Can be int.
    :param max_symbols: Max number of symbols. Can be int.
    :param is_enter: It is responsible for whether the enter button will work. Can be bool.
    :param font: The name of the font. By default, Comic Sans. Can be str.

    :return: None.
    """
    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            font_size: int,
            max_symbols: int,
            is_enter: bool = True,
            font: str = "Comic Sans MS"
        ) -> None:

        self.__rectangle: pygame.Rect = pygame.Rect(*position, *size)

        self.__bg_color: pygame.Color = pygame.Color("white")
        self.__font_size: int = font_size
        self.__font: pygame.font.Font = pygame.font.SysFont(font, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color("black")
        self.__texts: list[str] = list()
        self.__texts_surfaces: list[pygame.Surface] = list()
        self.__texts.append('')
        self.__texts_surfaces.append(self.__font.render('', True, self.__font_color))

        self.__max_symbols: int = max_symbols

        self.__is_enter: bool = is_enter

        self.__register: bool = False

    def __add_symbol(self, symbol: str) -> None:
        summa = 0
        for text in self.__texts:
            summa += len(text)

        if symbol == 'backspace':
            summa -= 1

        if summa < self.__max_symbols:
            if symbol == 'backspace':
                self.__texts[-1] = self.__texts[-1][:-1]
                self.__texts_surfaces[-1] = self.__font.render(self.__texts[-1], True, self.__font_color)

            elif symbol != '\n':
                self.__texts[-1] += symbol
                self.__texts_surfaces[-1] = self.__font.render(self.__texts[-1], True, self.__font_color)
            else:
                self.__texts.append('')
                self.__texts_surfaces.append(self.__font.render('', True, self.__font_color))

    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, self.__bg_color, self.__rectangle)

        index: int
        for index in range(len(self.__texts_surfaces)):
            window.blit(
                self.__texts_surfaces[index],
                (
                    self.__rectangle.left,
                    self.__rectangle.top + self.__font_size * index
                )
            )
    
    def check_events(self, event: pygame.event.Event) -> None:
        try:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.__is_enter:
                        self.__add_symbol('\n')
                elif event.key == pygame.K_BACKSPACE:
                    self.__add_symbol('backspace')
                elif event.key == pygame.K_CAPSLOCK:
                    self.__register = not(self.__register)
                else:
                    if self.__register:
                        self.__add_symbol(chr(event.key).upper())
                    else:
                        self.__add_symbol(chr(event.key))
        except ValueError:
            pass
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.__register = True
            if keys[pygame.K_1]:
                self.__add_symbol('backspace')
                self.__add_symbol("!")
            elif keys[pygame.K_2]:
                self.__add_symbol('backspace')
                self.__add_symbol("@")
            elif keys[pygame.K_3]:
                self.__add_symbol('backspace')
                self.__add_symbol("#")
            elif keys[pygame.K_4]:
                self.__add_symbol('backspace')
                self.__add_symbol("$")
            elif keys[pygame.K_5]:
                self.__add_symbol('backspace')
                self.__add_symbol("%")
            elif keys[pygame.K_6]:
                self.__add_symbol('backspace')
                self.__add_symbol("^")
            elif keys[pygame.K_7]:
                self.__add_symbol('backspace')
                self.__add_symbol("&")
            elif keys[pygame.K_8]:
                self.__add_symbol('backspace')
                self.__add_symbol("*")
            elif keys[pygame.K_9]:
                self.__add_symbol('backspace')
                self.__add_symbol("(")
            elif keys[pygame.K_0]:
                self.__add_symbol('backspace')
                self.__add_symbol(")")
            elif keys[pygame.K_MINUS]:
                self.__add_symbol('backspace')
                self.__add_symbol("_")
            elif keys[pygame.K_EQUALS]:
                self.__add_symbol('backspace')
                self.__add_symbol("+")
            elif keys[pygame.K_SEMICOLON]:
                self.__add_symbol('backspace')
                self.__add_symbol(":")
            elif keys[pygame.K_SLASH]:
                self.__add_symbol('backspace')
                self.__add_symbol("?")
        else:
            self.__register = False



class Button:
    """
    A class to create a button.

    Displays a button.
    Can Be Object Button

    :param position: Position. Can be tuple.
    :param size: Size. Can be tuple.
    :param text: Text on button. Can be str.
    :param function: A function that is performed after a button is pressed. Can be Func() -> None
    :param sprite: Sprite for costum button. Can be str and is a full reference to the sprite.

    :return: None
    """
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        function: Callable[[], None],
        sprite: str = ""
    ) -> None:
        # Базовые поля кнопки.
        self.__rectangle: pygame.Rect = pygame.Rect(*position, *size)
        self.__function: Callable[[], None] = function

        # Всякие доп. настройки.
        self.__bg_color: pygame.Color = pygame.Color("gray")
        self.__text_surface: pygame.Surface = pygame.font.SysFont("Comic Sans MS", size[1] // 4).render(
            text, True, pygame.Color("white")
        )

        self.__is_sprite: bool = False
        self.__sprite: pygame.image
        if sprite != "":
            self.__sprite = pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), size)
            self.__is_sprite = True
        

        self.__text_rectangle: pygame.Rect = self.__text_surface.get_rect(
            center=(
                position[0] + size[0] // 2,
                position[1] + size[1] // 2
            )
        )
    
    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__check_click(pygame.mouse.get_pos())

    def __check_click(self, mouse_position: tuple[int, int]) -> None:
        if self.__rectangle.collidepoint(mouse_position):
            self.__function()

    def draw(self, window: pygame.Surface) -> None:
        if self.__is_sprite:
            window.blit(self.__sprite, (self.__rectangle.x, self.__rectangle.y))
        else:
            pygame.draw.rect(window, self.__bg_color, self.__rectangle)
            window.blit(self.__text_surface, self.__text_rectangle)


if __name__ == "__main__":
    print("Hello!")
