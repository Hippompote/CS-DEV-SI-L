from .entity import Entity


class Player(Entity):
    """
    An extended version of Entity.
    It is the player of the game.
    
    Author:
        Aioniostheos
        Fierperle
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Creates a player at the specified coordinates.

        Arguments:
            x (int): the player x coordinate.
            y (int): the player y coordinate.
        """

        super().__init__(x=x, y=y, width=60, height=61, speedx=10, speedy=0, texture_path="./assets/player.png")
        self.__lives = 3
        self.__score = 0

    def get_lives(self) -> int:
        """
        Returns:
            the number of lives of the player.
        """

        return self.__lives

    def get_score(self) -> int:
        """
        Returns:
            the score of the player.
        """

        return self.__score

    def increase_score(self, amount: int) -> None:
        """
        Increases the score of the player by the specified amount.

        Arguments:
            amount (int): the amount to add to the score.
        """

        self.__score += amount

    def lose_life(self) -> None:
        """
        Removes one life from the player.
        If the player has no more lives, it is destroyed.
        """

        self.__lives -= 1
        if self.get_lives() <= 0:
            self.destroy()

    def shoot(self) -> None:
        """
        Shoots a projectile.
        """

        from .projectile import Projectile
        projectile = Projectile(x=self.get_pos()[0], y_origin=self.get_pos()[1] - 30, source=self, speed=-50)
        self.world.add_entity(projectile)
        projectile.move()

    def handle_collision(self, target: Entity, speed_modifier: float = 1) -> bool:
        """
        Handles the collision between the player and the target.
        When the player collides with a wall, he snaps to it.

        Arguments:
            target (Entity): the target of the collision.
            speed_modifier (float): Optional - the speed modifier of the collision.

        Returns:
            True if the collision has been handled ; False otherwise.
        """

        from .immovableentity import ImmovableEntity
        if isinstance(target, ImmovableEntity):
            Entity.stick_to(self, target, speed_modifier)
            return True

        return False
