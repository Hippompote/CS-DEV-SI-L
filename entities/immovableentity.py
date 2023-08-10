from .entity import Entity


class ImmovableEntity(Entity):
    """
    An ImmovableEntity is an Entity that cannot move and has no speed.

    Author:
        Aioniostheos
        Fierperle
    """

    def __init__(self, x: int, y: int, width: int, height: int, texture_path: str = None) -> None:
        """
        Creates an ImmovableEntity.

        Arguments:
            x (int): the x coordinate of the entity.
            y (int): the y coordinate of the entity.
            width (int): the width of the entity.
            height (int): the height of the entity.
            texture_path (str): Optional - the path to the texture of the entity.
        """

        super().__init__(x=x, y=y, width=width, height=height, speedx=0, speedy=0, texture_path=texture_path)

    def handle_collision(self, target, speed_modifier: float = 1.0) -> bool:
        """
        Immovable entities (except for defenses) do not handle collisions.
        The entity colliding with them will handle it.

        Arguments:
            target (Entity): the entity that collided with this entity.
            speed_modifier (float): Optional - the speed modifier of the entity that collided with this entity.

        Returns:
            True if the collision has been handled ; False otherwise.
        """
        return False
