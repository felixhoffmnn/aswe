import abc
from typing import Any, Callable


class NodeObject(abc.ABC):
    """Abstract Node Class"""

    @abc.abstractmethod
    def notify(self, options: dict[Any, Any], callback: Callable[..., Any]) -> None:
        """Abstract Class Method to notify subsequent objects in responsibility chain."""
        raise NotImplementedError
