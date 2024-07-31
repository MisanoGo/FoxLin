import bisect
from functools import wraps
from typing import Any

from .base import BaseColumn, Any

def check_index_range(method):
    """Decorator to check if an index is within the valid range."""
    @wraps(method)
    def wrapper(self, index: int, *args, **kwargs):
        # Check if the index is out of range for the data list
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range.")  # Raise an error if out of range
        return method(self, index, *args, **kwargs)  # Call the original method if index is valid
    return wrapper

class ConcreteColumn(BaseColumn):
    def __init__(self, default: Any = None):
        super().__init__(default)
        self.sorted_data = []  # List to maintain a sorted version of the data

    def insert(self, value: Any) -> int:
        index = bisect.bisect_right(self.sorted_data, value)  # Insert value into sorted_data and maintain sorted order
        self.sorted_data.insert(index, value)
        self.data.append(self.sorted_data.index(value))                              # Store the index in the data list (which is now a list of indices)
        return index

    @check_index_range  
    def delete(self, index: int) -> Any:
        value = self.sorted_data.pop(self.data[index])  # Remove from sorted_data using the index
        self.data.remove(index)                         # Remove index from the data list
        return value                                    # Return the deleted value

    @check_index_range  
    def update(self, index: int, value: Any) -> None:
        old_index = self.data[index]                # Get the old index
        old_value = self.sorted_data[old_index]     # Get old value
        # Update sorted_data
        self.sorted_data.remove(old_value)          # Remove old value from sorted
        # Insert new value in sorted order
        bisect.insort(self.sorted_data, value)  
        new_index = self.sorted_data.index(value)   # Get new index of the inserted value
        self.data[index] = new_index                # Update the index in the data list

    @check_index_range  
    def get(self, index: int) -> Any:
        # Use the index stored in data to get the actual value from sorted_data
        return self.sorted_data[self.data[index]]  # Return the value from sorted_data

    def __lt__(self, value: Any) -> bool:
        return all(self.sorted_data[item] < value for item in self.data)

    def __le__(self, value: Any) -> bool:
        return all(self.sorted_data[item] <= value for item in self.data)

    def __gt__(self, value: Any) -> bool:
        return all(self.sorted_data[item] > value for item in self.data)

    def __ge__(self, value: Any) -> bool:
        return all(self.sorted_data[item] >= value for item in self.data)

    def __ne__(self, value: Any) -> bool:
        return any(self.sorted_data[item] != value for item in self.data)

    def __eq__(self, value: Any) -> bool:
        return any(self.sorted_data[item] == value for item in self.data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(Data Indices: {self.data}, Sorted: {self.sorted_data})"
    
    
    
    
