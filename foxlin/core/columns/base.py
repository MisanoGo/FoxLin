from abc import ABC, abstractmethod
from typing import Any, List

class BaseColumn(ABC):
    """
    An abstract base class for implementing various data structure algorithms.

    This class provides a template for creating different data structures
    with common operations such as insertion, deletion, and retrieval.

    Attributes:
        data (List[Any]): A list to store the elements of the data structure.
        default (Any): The default value to be used when no value is provided.
    """

    def __init__(self, default: Any = None):
        """
        Initialize the BaseColumn.

        Args:
            default (Any, optional): The default value to be used when no value is provided.
                Defaults to None.
        """
        self.data = []
        self.default = default

    @abstractmethod
    def insert(self, value: Any) -> int:
        """Insert a value into the data structure."""
        pass

    @abstractmethod
    def delete(self, index: int) -> Any:
        """Delete an element from the data structure at the specified index."""
        pass

    @abstractmethod
    def update(self, index: int, value: Any) -> None:
        """Update the value at the specified index in the data structure."""
        pass

    @abstractmethod
    def get(self, index: int) -> Any:
        """Retrieve the value at the specified index in the data structure."""
        pass

    @abstractmethod
    def __lt__(self, value: Any) -> bool:
        """Check if all elements in the data structure are less than a given value."""
        pass

    @abstractmethod
    def __le__(self, value: Any) -> bool:
        """Check if all elements in the data structure are less than or equal to a given value."""
        pass

    @abstractmethod
    def __gt__(self, value: Any) -> bool:
        """Check if all elements in the data structure are greater than a given value."""
        pass

    @abstractmethod
    def __ge__(self, value: Any) -> bool:
        """Check if all elements in the data structure are greater than or equal to a given value."""
        pass

    @abstractmethod
    def __ne__(self, value: Any) -> bool:
        """Check if any element in the data structure is not equal to a given value."""
        pass

    # @abstractmethod
    # def __eq__(self, value: Any) -> bool:
    #     """Check if any element in the data structure is equal to a given value."""
    #     pass

    def __len__(self) -> int:
        """Get the number of elements in the data structure."""
        return len(self.data)

    def __iter__(self):
        """Return an iterator for the data structure."""
        return iter(self.data)

    def __repr__(self) -> str:
        """Return a string representation of the data structure."""
        return f"{self.__class__.__name__}({self.data})"

    def __contains__(self, item: Any) -> bool:
        """Check if an item is present in the data structure."""
        return item in self.data

    def __eq__(self, other: Any) -> bool:
        """Check if this data structure is equal to another object."""
        if isinstance(other, BaseColumn):
            return self.data == other.data
        return False
