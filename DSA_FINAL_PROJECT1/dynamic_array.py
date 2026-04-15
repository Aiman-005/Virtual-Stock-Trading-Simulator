import ctypes


class DynamicArray:
    """
    Manual Dynamic Array Implementation
    - Uses ctypes for low-level memory management
    - No Python built-in list allowed
    """
    
    def __init__(self):
        self._size = 0              # Number of elements
        self._capacity = 1          # Allocated capacity
        self._array = self._make_array(self._capacity)
    
    def __len__(self):
        """Return number of elements"""
        return self._size
    
    def __getitem__(self, index):
        """Get item at index - O(1)"""
        if not 0 <= index < self._size:
            raise IndexError("Index out of bounds")
        return self._array[index]
    
    def __setitem__(self, index, value):
        """Set item at index - O(1)"""
        if not 0 <= index < self._size:
            raise IndexError("Index out of bounds")
        self._array[index] = value
    
    def append(self, item):
        """Add item to end - O(1) amortized"""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)  # Double capacity
        
        self._array[self._size] = item
        self._size += 1
    
    def pop(self):
        """Remove and return last item - O(1)"""
        if self._size == 0:
            raise IndexError("Array is empty")
        
        item = self._array[self._size - 1]
        self._size -= 1
        
        # Shrink if too much wasted space
        if self._size < self._capacity // 4:
            self._resize(self._capacity // 2)
        
        return item
    
    def _resize(self, new_capacity):
        """Resize internal array - O(n)"""
        new_array = self._make_array(new_capacity)
        
        # Copy elements
        for i in range(self._size):
            new_array[i] = self._array[i]
        
        self._array = new_array
        self._capacity = new_capacity
    
    def _make_array(self, capacity):
        """Create new array with given capacity using ctypes"""
        return (capacity * ctypes.py_object)()
    
    def is_empty(self):
        """Check if array is empty"""
        return self._size == 0
    
    def clear(self):
        """Clear all elements"""
        self._size = 0
        self._capacity = 1
        self._array = self._make_array(self._capacity)