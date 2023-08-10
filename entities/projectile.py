from .entity import Entity


class Projectile(Entity):
    """
    An extended version of Entity that represents a projectile shoot by another entity.

    Author:
        Aioniostheos
        Fierperle
    """

    def __init__(self, x: int, y_origin: int, source: Entity, speed: int = 10) -> None:
        """
        Creates a projectile at the specified coordinates from the specified source and with the specified speed value.

        Arguments:
            x (int): the x coordinate.
            y_origin (int): the y coordinate.
            source (Entity) : the entity that shoots this projectile.
            speed (int) : Optional - the up or down speed value in pixel per tick.
        """

        from .player import Player
        super().__init__(
            x=x, y=y_origin,
            width=4, height=24,
            speedx=0, speedy=speed,
            texture_path="./assets/laser_ally.png" if isinstance(source, Player) else "./assets/laser_enemy.png"
        )
        self.__source = source

    def handle_collision(self, target: Entity, speed_modifier: float = 1) -> bool:
        """
        Handles the collision between this projectile and another entity.
        If the target is an alien and this projectile comes from an alien, it passes through.
        If the target is an alien and this projectile comes from a player, it damages the alien and is destroyed.
        If the target is a player and this projectile comes from an alien, it damages the player and is destroyed.
        If the target is a defense, it damages the defense and is destroyed.
        If the target is a projectile, it destroys both projectiles.
        If the target is the map border, it is destroyed.

        Arguments:
            target (Entity): the entity that this projectile collides with.
            speed_modifier (float): Optional - the speed modifier of the projectile.

        Returns:
            True if the collision has been handled ; False otherwise.
        """
        from .alien import Alien
        from .defense import Defense
        from .immovableentity import ImmovableEntity
        from .player import Player

        if isinstance(target, Alien):
            if isinstance(self.__source, Player):
                self.destroy()
                target.destroy()
                self.__source.increase_score(10)
                return True
        elif isinstance(target, Player):
            if isinstance(self.__source, Alien):
                target.lose_life()
                self.destroy()
                return True
        elif isinstance(target, Defense):
            target.damage()
            self.destroy()
            return True
        elif isinstance(target, Projectile) and not isinstance(target.__source, type(self.__source)):
            self.destroy()
            target.destroy()
            return True
        elif isinstance(target, ImmovableEntity):  # it cannot be a defense because it is already handled.
            self.destroy()
            return True

        return False
