import random
from tkinter import Canvas
from typing import Callable

from PIL import Image

from entities.entity import Entity
from util.queue import Queue
from util.stack import Stack
from .client import Client


class World:
    """
    This class is the main functional class of the game.
    All functional methods should be defined here and called inside a game.
    There should be only one instance of this class per game.

    Author:
        Aioniostheos
    """

    def __init__(self, canvas: Canvas, background: Image.Image) -> None:
        """
        Creates a new world.
        Initializes a new client with the specified canvas.

        Arguments:
            canvas (Canvas): the canvas where entities are displayed.
            background (Image): the background image.
        """

        self.entities = []
        self.waiting_for_destruction = Queue()

        self.client = Client(canvas, background)
        self.__end_game = None
        self.__alien_shoot_cooldown = 0

    def add_entity(self, entity: Entity) -> None:
        """
        Adds an entity to the world and on client-side.

        Arguments:
            entity (Entity): the entity to add.
        """

        self.entities.append(entity)
        entity.set_world(self)
        self.client.add_entity(entity)

    def should_end_game(self) -> tuple[bool, str] | tuple[bool, None]:
        """
        Returns:
            True if the game should end, False otherwise.
        """

        return self.__end_game is not None, self.__end_game

    def update(self) -> None:
        """
        Updates the world.
        This method contains only functional elements. It should not contain any graphical elements.
        """

        from entities.alien import Alien
        from entities.player import Player
        from entities.projectile import Projectile

        if self.__alien_shoot_cooldown > 0:
            self.__alien_shoot_cooldown -= 100

        aliens = Stack()
        for entity in self.entities:
            if entity.should_be_destroyed():
                if isinstance(entity, Player):
                    self.__end_game = "lose"
                if entity.id is not None:
                    self.waiting_for_destruction.enqueue(entity)
                self.entities.remove(entity)
            else:
                if isinstance(entity, Projectile):
                    entity.move()
                elif isinstance(entity, Alien):
                    entity.move(1 + self.client.player.get_score() // 100)
                    aliens.push(entity)

        if aliens.is_empty():
            self.__end_game = "win"
        else:
            while not aliens.is_empty():
                alien = aliens.pop()
                if random.choice([True, False]) and self.__alien_shoot_cooldown == 0:
                    alien.shoot()
                    self.__alien_shoot_cooldown = 2000
                    break

    def update_client(self) -> None:
        """
        Updates the client.
        This method contains only graphical elements. It should not contain any functional elements.
        """

        self.client.update(self.entities, self.waiting_for_destruction)
        self.waiting_for_destruction.clear()

    def will_hit(self, entity: Entity, speed_modifier: float = 1.0) -> tuple[bool, Entity] | tuple[bool, None]:
        """
        Returns whether the specified entity will collide with an entity.

        Arguments:
            entity (Entity): the entity which we check the forecast collision.
            speed_modifier (float): Optional - the speed modifier applied by multiplication.

        Returns:
            True if this entity will collide, the entity with which this entity collides ; otherwise False, None.
        """

        for other_entity in self.entities:
            if other_entity is not entity and entity.will_hit(other_entity, speed_modifier):
                return True, other_entity
        return False, None

    @staticmethod
    def alien_collision_event(func: callable) -> Callable:
        def wrapper(*args, **kwargs):
            source = args[0]
            target = args[1]

            from entities.alien import Alien
            from entities.immovableentity import ImmovableEntity
            from entities.defense import Defense
            if isinstance(target, ImmovableEntity) and not isinstance(target, Defense):
                for entity in source.world.entities:
                    if isinstance(entity, Alien):
                        entity.reverse_speed()
                        entity.move_down()
            return func(*args, **kwargs)
        return wrapper
