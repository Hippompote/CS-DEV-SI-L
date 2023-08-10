from typing import TypeVar

T = TypeVar('T')


class Stack:
    """
    A stack is a last-in-first-out (LIFO) data structure.
    This implementation uses a Python list as underlying storage.

    Author:
        Aioniostheos
    """

    def __init__(self) -> None:
        """
        Creates a new empty stack.
        """

        self.__stack = []

    def __iter__(self) -> iter:
        """
        Returns:
             an iterator over the items in the stack.
        """

        return self.__stack.__iter__()

    def __len__(self) -> int:
        """
        Returns:
            the size of the stack.
        """

        return self.size()

    def __contains__(self, item) -> bool:
        """
        Arguments:
            item: the item to search for.

        Returns:
            True if the item is in the stack ; False otherwise.
        """

        return item in self.__stack

    def clear(self) -> None:
        """
        Clears the stack.
        """

        self.__stack.clear()

    def is_empty(self) -> bool:
        """
        Returns:
            True if the stack is empty ; False otherwise.
        """

        return self.size() == 0

    def peek(self) -> T | None:
        """
        Peeks the top item of the stack.

        Returns:
            the top item ; None if the stack is empty.
        """

        if self.is_empty():
            return None
        else:
            return self.__stack[-1]

    def pop(self) -> T | None:
        """
        Pops an item from the stack.

        Returns:
            the popped item ; None if the stack is empty.
        """

        if self.is_empty():
            return None
        else:
            return self.__stack.pop()

    def push(self, item) -> None:
        """
        Pushes an item to the stack.

        Arguments:
            item: the item to push.
        """

        self.__stack.append(item)

    def size(self) -> int:
        """
        Returns:
            the size of the stack.
        """

        return len(self.__stack)
