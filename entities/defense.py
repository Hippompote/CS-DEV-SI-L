from .immovableentity import ImmovableEntity
from PIL import Image


class Defense(ImmovableEntity):
    """
    An extended ImmovableEntity that protects the player from aliens.
    This entities can be destroyed by aliens (collision or projectiles).

    Author:
        Aioniostheos
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Creates a defense at the specified coordinates.

        Arguments:
            x (int): the x coordinate.
            y (int): the y coordinate.
        """

        self.__lives = 5
        self.__texture_path = "./assets/defense.png"
        super().__init__(x=x, y=y, width=56, height=18, texture_path="./assets/defense.png")

    def damage(self) -> None:
        """
        Damages this defense.
        """
        self.__lives -= 1
        self.__texture_path = "./assets/defense_damage_" + str(self.get_lives()) + ".png"
        if self.get_lives() <= 0:
            self.destroy()

    def get_lives(self) -> int:
        """
        Returns:
             the number of lives of this defense.
        """
        return self.__lives

    def get_texture(self) -> Image.Image | None:
        """
        Returns:
            texture (Image): the texture of this entity.
        """

        if self.__texture_path is None:
            return None
        else:
            return Image.open(self.__texture_path)
