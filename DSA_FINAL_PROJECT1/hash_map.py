from dynamic_array import DynamicArray


class HashNode:
    """Node for storing key-value pairs in hash map"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None  # For chaining (collision handling)


class HashMap:
    """
    through using Separate Chaining
    - No built-in dictionary used
    - Uses DynamicArray for buckets
    - Handles collisions with linked lists
    """
    
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(None)
    
    def _hash(self, key):
        """Hash function to convert key to bucket index"""
        # Use Python's built-in hash but modulo to get index
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """Insert or update key-value pair - O(1) average"""
        index = self._hash(key)
        head = self.buckets[index]
        
        # Check if key already exists (update)
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        
        # Key doesn't exist, insert new node at beginning
        new_node = HashNode(key, value)
        new_node.next = head
        self.buckets[index] = new_node
        self.size += 1
        
        # Check load factor and resize if needed
        if self.size / self.capacity > 0.75:
            self._resize()
    
    def get(self, key, default=None):
        """Get value by key - O(1) average"""
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        return default
    
    def __getitem__(self, key):
        """Access using map[key] syntax"""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value
    
    def __setitem__(self, key, value):
        """Set using map[key] = value syntax"""
        self.put(key, value)
    
    def contains(self, key):
        """Check if key exists - O(1) average"""
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return True
            current = current.next
        
        return False
    
    def remove(self, key):
        """Remove key-value pair - O(1) average"""
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        
        return False
    
    def keys(self):
        """Return all keys as DynamicArray"""
        result = DynamicArray()
        for i in range(len(self.buckets)):
            current = self.buckets[i]
            while current:
                result.append(current.key)
                current = current.next
        return result
    
    def values(self):
        """Return all values as DynamicArray"""
        result = DynamicArray()
        for i in range(len(self.buckets)):
            current = self.buckets[i]
            while current:
                result.append(current.value)
                current = current.next
        return result
    
    def items(self):
        """Return all key-value pairs as DynamicArray of tuples"""
        result = DynamicArray()
        for i in range(len(self.buckets)):
            current = self.buckets[i]
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result
    
    def _resize(self):
        """Resize hash map when load factor is too high - O(n)"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        
        # Create new buckets
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        
        # Rehash all entries
        for i in range(len(old_buckets)):
            current = old_buckets[i]
            while current:
                self.put(current.key, current.value)
                current = current.next
        
        # Adjust size (put() increments it)
        # Size was counted during puts, so divide by 2
        self.size = self.size // 2
    
    def is_empty(self):
        """Check if hash map is empty"""
        return self.size == 0
    
    def __len__(self):
        """Return number of key-value pairs"""
        return self.size
    
    def clear(self):
        """Clear all entries"""
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0
    
    def setdefault(self, key, default=None):
        """Get value or set default if key doesn't exist"""
        if self.contains(key):
            return self.get(key)
        else:
            self.put(key, default)
            return default