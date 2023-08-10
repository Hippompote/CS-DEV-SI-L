import tkinter as tk
from typing import List

from PIL import ImageTk, Image

from entities.entity import Entity
from util.queue import Queue


class Client:
    """
    This class is the main display class of the game.
    All graphical methods should be defined here and called inside a game. No functional methods should be defined here.
    There should be only one instance of this class per game.

    Author:
        Aioniostheos
        Fierperle
    """

    def __init__(self, canvas: tk.Canvas, background: Image.Image) -> None:
        """
        Creates a client with the specified width and height.
        
        Arguments:
            canvas (Canvas): the client's canvas.
            background (Image): the background image.
        """

        self.player = None
        self.__canvas = canvas
        self.__background = ImageTk.PhotoImage(background)
        self.__canvas.create_image(0, 0, image=self.__background, anchor="nw")

    def add_entity(self, entity: Entity) -> None:
        """
        Add an entity to the client and sets its id.

        Arguments:
            entity (Entity): the entity to add.
        """

        if entity.get_texture() is not None:
            self.draw_entity(entity)

        from entities.player import Player
        if isinstance(entity, Player):
            if self.player is not None:
                raise Exception("There can only be one player per game.")
            self.player = entity

    def draw_entity(self, entity: Entity) -> None:
        """
        Draw an entity on the client.

        Arguments:
            entity (Entity): the entity to draw.
        """

        if entity.get_texture() is not None:
            entity.image = ImageTk.PhotoImage(entity.get_texture())
            entity.set_id(self.__canvas.create_image(entity.get_pos()[0], entity.get_pos()[1], image=entity.image))
            self.__canvas.pack()

    def update(self, entities: List[Entity], waiting_for_destruction: Queue = None) -> None:
        """
        Update entities displayed on the client.
        If an entity is marked for destruction, it is removed from the canvas.
        This method first clears the canvas, then redraws all entities that should be rendered.
        As the canvas is updated fast enough, Python does not lose references for the images and ids.

        Arguments:
            entities (List[Entity]): the list of entities to update.
            waiting_for_destruction (Queue): Optional - the queue of entities waiting to be destroyed.
        """

        self.__canvas.delete("all")
        self.__canvas.create_image(0, 0, image=self.__background, anchor="nw")

        for entity in entities:
            if not entity.should_be_destroyed():
                if entity.get_texture() is not None:
                    self.draw_entity(entity)
            else:
                # this makes sure that the references for the image and the id are deleted.
                entity.image = None
                entity.set_id(None)

        if waiting_for_destruction is not None:
            while not waiting_for_destruction.is_empty():
                entity = waiting_for_destruction.dequeue()

                # this makes sure that the references for the image and the id are deleted.
                entity.image = None
                entity.set_id(None)

        self.__canvas.pack()
