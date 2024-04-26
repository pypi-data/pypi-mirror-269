"""
Module for creating a button.

Displays a button on the screen.
"""


from pgpyui import *


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
        
        self.__rectangle: pygame.Rect = pygame.Rect(*position, *size)
        self.__function: Callable[[], None] = function

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
