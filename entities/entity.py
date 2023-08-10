from abc import ABC
from typing import List, Union

from PIL import Image


class Entity(ABC):
	"""
	This class is an abstract class, it needs to be implemented.

	Author:
		Aioniostheos
		Fierperle
	"""

	def __init__(self, x: int, y: int, width: int, height: int, speedx: int, speedy: int, texture_path: str = None):
		"""
		Creates a new Entity with the specified position, dimension, speed and texture.
		Position and dimension is then used to create an accurate hitbox for this entity.

		Arguments:
			x (int): the x coordinate of the entity.
			y (int): the y coordinate of the entity.
			width (int): the width of the entity.
			height (int): the height of the entity.
			speedx (int): the speed of the entity, among x coordinates.
			speedy (int): the speed of the entity, among y coordinates.
			texture_path (str): Optional - the path to the texture of the entity.
		"""

		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__speedx = speedx
		self.__speedy = speedy
		self.__texture_path = texture_path

		self.__for_destruction = False
		self.id = None
		self.image = None
		self.world = None

	def destroy(self) -> None:
		"""
		Prepares entity for destruction.
		"""

		self.__for_destruction = True

	def get_hitbox(self) -> List[int]:
		"""
		Returns the extremities of the hitbox.

		Returns:
			hitbox (List[int]): the list containing the coordinates of the top-left corner and the bottom_right corner
								of the hitbox.
		"""

		return [
			int(self.__x - self.__width / 2),
			int(self.__y - self.__height / 2),
			int(self.__x + self.__width / 2),
			int(self.__y + self.__height / 2)
		]

	def get_pos(self) -> tuple[int, int]:
		"""
		Returns the current position of this entity.

		Returns:
			x, y (int, int): the x and y coordinates of this entity.
		"""

		return self.__x, self.__y

	def get_speed(self) -> tuple[int, int]:
		"""
		Returns:
			speedx, speedy (int, int): the speed of this entity among x and y coordinates.
		"""

		return self.__speedx, self.__speedy

	def get_texture(self) -> Union[Image.Image, None]:
		"""
		Returns:
			the texture of this entity.
		"""

		if self.__texture_path is None:
			return None
		else:
			return Image.open(self.__texture_path)

	def get_width(self) -> int:
		"""
		Returns:
			the width of this entity.
		"""

		return self.__width

	def handle_collision(self, target, speed_modifier: float = 1.0) -> bool:
		"""
		Handles the collision with the specified entity. This method must be implemented.

		Arguments:
			target (Entity): the targeted entity with which this entity collides.
			speed_modifier (float): Optional - the speed modifier applied by multiplication.

		Returns:
			True if the collision has been handled ; False otherwise.
		"""

		raise NotImplementedError("This method should be implemented.")

	def move(self, speed_modifier: float = 1.0) -> None:
		"""
		Modifies the position of this entity according to the speed of this entity and to the specified speed modifier.

		Arguments:
			speed_modifier (float): Optional - the speed modifier applied by multiplication.
		"""

		action = False
		[will_hit, entity] = self.world.will_hit(self, speed_modifier)
		if will_hit:
			action = self.handle_collision(entity, speed_modifier)
		if not action:
			self.__x += int(speed_modifier * self.__speedx)
			self.__y += int(speed_modifier * self.__speedy)

	def set_id(self, display_id) -> None:
		"""
		Sets the id of this entity.

		Arguments:
			display_id: the id of this entity.
		"""

		self.id = display_id

	def set_world(self, world) -> None:
		"""
		Sets the world of this entity.

		Arguments:
			world (World): the world of this entity.
		"""

		self.world = world

	def should_be_destroyed(self) -> bool:
		"""
		Returns:
			True if this entity should be destroyed ; False otherwise.
		"""

		return self.__for_destruction

	def stick_to(self, target, speed_modifier: float) -> None:
		"""
		Sticks this entity to the specified entity.

		Arguments:
			target (Entity): the targeted entity to stick to.
			speed_modifier (int): the speed modifier applied by multiplication.
		"""

		hitbox = target.get_hitbox()

		# right wall
		if speed_modifier > 0:
			self.__x = int(hitbox[0] - self.get_width() / 2)

		# left wall
		else:
			self.__x = int(hitbox[2] + self.get_width() / 2)

	def will_hit(self, target, speed_modifier: float = 1.0) -> bool:
		"""
		Arguments:
			target (Entity): the targeted entity with which we check the forecast collision.
			speed_modifier (float): Optional - the speed modifier applied by multiplication.

		Returns:
			True if this entity will collide with the target ; False otherwise.
		"""

		hitbox = target.get_hitbox()
		return (
				(self.__y + (speed_modifier * self.__speedy) - self.__height / 2) < hitbox[3] and
				(self.__y + (speed_modifier * self.__speedy) + self.__height / 2) > hitbox[1] and
				(self.__x + (speed_modifier * self.__speedx) - self.__width / 2) < hitbox[2] and
				(self.__x + (speed_modifier * self.__speedx) + self.__width / 2) > hitbox[0]
		)

	@classmethod
	def set_pos(cls, entity, x: int, y: int) -> None:
		"""
		Sets the position of this entity.

		Arguments:
			entity (Entity): the entity concerned by these changes.
			x (int): the x coordinate of this entity.
			y (int): the y coordinate of this entity.
		"""

		entity.__x = x
		entity.__y = y

	@classmethod
	def set_speed(cls, entity, speedx: int, speedy: int) -> None:
		"""
		Sets the speed of this entity.

		Arguments:
			entity (Entity): the entity concerned by these changes.
			speedx (int): the speed of this entity among x coordinates.
			speedy (int): the speed of this entity among y coordinates.
		"""

		entity.__speedx = speedx
		entity.__speedy = speedy
