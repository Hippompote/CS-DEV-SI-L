from typing import TypeVar

T = TypeVar('T')


class Queue:
    """
    A queue is a first-in-first-out (FIFO) data structure.
    This implementation uses a Python list as underlying storage.

    Author:
        Aioniostheos
    """

    def __init__(self) -> None:
        """
        Creates a new empty queue.
        """

        self.__queue = []

    def __iter__(self) -> iter:
        """
        Returns:
             an iterator over the items in the queue.
        """

        return self.__queue.__reversed__()

    def __len__(self) -> int:
        """
        Returns:
            the size of the queue.
        """

        return self.size()

    def __contains__(self, item) -> bool:
        """
        Arguments:
            item (T): the item to check.

        Returns:
            True if the item is in the queue ; False otherwise.
        """

        return item in self.__queue

    def clear(self) -> None:
        """
        Clears the queue.
        """

        self.__queue.clear()

    def dequeue(self) -> T | None:
        """
        Dequeues the front item of the queue.

        Returns:
            the front item ; None if the queue is empty.
        """

        if self.is_empty():
            return None
        else:
            return self.__queue.pop(0)

    def enqueue(self, item: T) -> None:
        """
        Enqueues the specified item.

        Arguments:
            item (T): the item to enqueue.
        """

        self.__queue.append(item)

    def get_priority(self, item: T) -> int | None:
        """
        Returns the priority of the specified item.

        Arguments:
            item (T): the item to get the priority of.

        Returns:
            the priority of the item ; None if the item is not in the queue.
        """

        if item in self.__queue:
            return self.__queue.index(item)
        else:
            return None

    def is_empty(self) -> bool:
        """
        Returns:
            True if the queue is empty ; False otherwise.
        """

        return self.size() == 0

    def peek(self) -> T | None:
        """
        Peeks the front item of the queue.

        Returns:
            the front item ; None if the queue is empty.
        """

        if self.is_empty():
            return None
        else:
            return self.__queue[0]

    def priority_enqueue(self, item: T, priority: int) -> None:
        """
        Enqueues the specified item with the specified priority.

        Arguments:
            item (T): the item to enqueue.
            priority (int): the priority of the item.
                            A priority of 0 means that the item will be the first to be dequeued.
        """

        self.__queue.insert(priority, item)

    def size(self) -> int:
        """
        Returns:
            the size of the queue.
        """

        return len(self.__queue)
