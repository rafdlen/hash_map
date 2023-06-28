# Description: HashMap implementation with Open Addressing and quadratic probing written in Python

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Inserts a key-value pair into the hash map.

        Params:
            - The key to be inserted.
            - The value associated with the key.

        Returns: None
        """

        if self.table_load() >= 0.5:
            new_cap = 2 * self._capacity
            self.resize_table(new_cap)

        hash_code = self._hash_function(key)
        initial_index = hash_code % self._capacity

        if self._buckets[initial_index] is None or self._buckets[initial_index].is_tombstone:
            self._buckets.set_at_index(initial_index, HashEntry(key, value))
            self._size += 1
        else:
            j = 0
            ind = initial_index
            while True:
                if self._buckets[ind] is None or self._buckets[ind].is_tombstone:
                    self._buckets.set_at_index(ind, HashEntry(key, value))
                    self._size += 1
                    return
                elif self._buckets[ind].key == key:
                    self._buckets[ind].value = value
                    return

                j += 1
                ind = (initial_index + j ** 2) % self._capacity

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table.

        Params: None

        Returns: The load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        Params: None

        Returns: The number of empty buckets.
        """
        empty_buckets = 0
        for bucket in range(self._capacity):
            if self._buckets[bucket] is None:
                empty_buckets += 1

        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to the given new capacity.

        Params: The new capacity.

        Returns: None
        """
        old_cap = self._capacity

        temp = self._buckets

        if new_capacity < self._size:
            return

        if self._is_prime(new_capacity) is False:
            self._capacity = self._next_prime(new_capacity)
        else:
            self._capacity = new_capacity

        self._buckets = DynamicArray()

        for bucket in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

        for hash_entry in range(old_cap):
            h_entry = temp[hash_entry]
            if h_entry is not None and h_entry.is_tombstone is False:
                self.put(h_entry.key, h_entry.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the specified key.

        Params: The key from the map.

        Returns: The value associated with the key, or None if the key is not found.
        """
        for table_key in range(self._capacity):
            if self._buckets[table_key] is not None:
                if self._buckets[table_key].key == key and self._buckets[table_key].is_tombstone is False:
                    return self._buckets[table_key].value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the specified key is in the hash map

        Params: The key to check for.

        Returns: True if the key is found in the hash table, False otherwise.
        """
        for entry in range(self._capacity):
            if self._buckets[entry] is not None:
                if self._buckets[entry].key == key and self._buckets[entry].is_tombstone is False:
                    return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the key-value pair associated with the specified key.

        Params: The key to be removed.

        Returns: None
        """
        for entry in range(self._capacity):
            if self._buckets[entry] is not None:
                if self._buckets[entry].key == key and self._buckets[entry].is_tombstone is False:
                    self._buckets[entry].is_tombstone = True
                    self._size -= 1

    def clear(self) -> None:
        """
        Clears the hash table.

        Params: None

        Returns: None
        """
        self._buckets = DynamicArray()
        self._size = 0

        for bucket in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of all key-value pairs in the hash table.

        Params: None

        Returns: A dynamic array containing tuples of key-value pairs.
        """
        da = DynamicArray()

        for entry in range(self._capacity):
            if self._buckets[entry] is not None and self._buckets[entry].is_tombstone is False:
                da.append((self._buckets[entry].key, self._buckets[entry].value))

        return da

    def __iter__(self):
        """
        Returns an iterator object for iterating over the hash map.

        Params: None

        Returns: The iterator object.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Returns the next key-value pair in the hash map during iteration.

        Params: None

        Returns: The next key-value pair.
        """
        try:
            while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone is True:
                self._index = self._index + 1

            value = self._buckets[self._index]

            self._index = self._index + 1

            return value

        except DynamicArrayException:
            raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
