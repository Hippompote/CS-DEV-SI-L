from world.world import World
from .entity import Entity


class Alien(Entity):
    """
    An extended version of Entity.
    It is the aliens of the game.

    Author:
        Aioniostheos
        Fierperle
    """

    def __init__(self, x: int, y: int, speedx: int = 2) -> None:
        """
        Creates an Alien at the specified coordinates.

        Arguments:
            x (int): the alien x coordinate.
            y (int): the alien y coordinate.
            speedx (int): Optional - the speed of the aliens movements in pixel per tick.
        """
        super().__init__(
            x=x, y=y,
            width=62, height=43,
            speedx=speedx, speedy=0,
            texture_path="./assets/alien_type_1.png"
        )
        self.__down_increment = 10

    def move_down(self) -> None:
        """
        Moves the alien down.
        """

        Entity.set_pos(self, self.get_pos()[0], self.get_pos()[1] + self.__down_increment)

    def reverse_speed(self) -> None:
        """
        Reverses the speed value to make the alien move backward.
        """

        Entity.set_speed(self, -self.get_speed()[0], -self.get_speed()[1])

    def shoot(self) -> None:
        """
        Makes the alien shoot a projectile.
        """

        from .projectile import Projectile
        self.world.add_entity(Projectile(x=self.get_pos()[0], y_origin=self.get_pos()[1] + 30, source=self, speed=10))

    @World.alien_collision_event
    def handle_collision(self, target: Entity, speed_modifier: float = 1.0) -> bool:
        """
        Handles the collision with the specified entity.
        If the target is an immovable wall, it reverses the speed and move down by his increment. This also triggers the
        world alien collision event.
        If the target is a defense, it damages the defense and is destroyed.
        If the target is a player, the player loses a life and the alien is destroyed.

        Arguments:
            target (Entity): the targeted entity with which this entity collides.
            speed_modifier (float): Optional - the speed modifier applied by multiplication.

        Returns:
            True if the collision has been handled ; False otherwise.
        """

        from .defense import Defense
        from .immovableentity import ImmovableEntity
        from .player import Player
        if isinstance(target, Defense):
            target.damage()
            self.destroy()
            return True
        elif isinstance(target, ImmovableEntity):
            return True
        elif isinstance(target, Player):
            target.lose_life()
            self.destroy()
            return True

        return False
