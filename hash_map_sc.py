
from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Insert or update a key-value pair in the hash map.

        Params:
            Key to be inserted or updated.
            Value corresponding to the key.

        Return: None
        """
        if self.table_load() >= 1:
            new_cap = 2 * self._capacity
            self.resize_table(new_cap)

            hash_code = self._hash_function(key)
            da_index = hash_code % self._capacity
        else:
            hash_code = self._hash_function(key)
            da_index = hash_code % self._capacity

        for l_list in range(self._capacity):
            if self._buckets[l_list].contains(key) is not None:
                self._buckets[l_list].contains(key).value = value
                return

        self._size += 1
        self._buckets[da_index].insert(key, value)

    def empty_buckets(self) -> int:
        """
        Get the number of empty buckets in the hash map.

        Params: None

        Return: Number of empty buckets.
        """
        num_empty_buckets = 0
        for bucket_index in range(self._capacity):
            if self._buckets[bucket_index].length() == 0:
                num_empty_buckets += 1

        return num_empty_buckets

    def table_load(self) -> float:
        """
        Get the load factor of the hash map.

        Params: None

        Return: Load factor of the hash map.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clear the hash map..

        Params: None

        Return: None
        """
        self._buckets = DynamicArray()

        for l_list in range(self._capacity):
            self._buckets.append(LinkedList())
            self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to a new capacity.

        Params: New capacity for the hash table.

        Return: None
        """

        old_cap = self._capacity

        temp = self._buckets

        if new_capacity < 1:
            return

        if self._is_prime(new_capacity) is False:
            self._capacity = self._next_prime(new_capacity)
        else:
            self._capacity = new_capacity

        self._buckets = DynamicArray()

        for bucket in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

        for l_list in range(old_cap):
            it = temp[l_list].__iter__()

            for elem in it:
                self.put(elem.key, elem.value)

    def get(self, key: str):
        """
        Get the value associated with the given key.

        Params: Key to search for.

        Return: The value associated with the key, or None if the key is not found.
        """
        hash_code = self._hash_function(key)

        da_index = hash_code % self._capacity

        node = self._buckets[da_index].contains(key)

        if node is None:
            return
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Check if the hash map contains the given key.

        Params: Key to search for.

        Return: True if the key is found, False otherwise.
        """
        hash_code = self._hash_function(key)

        da_index = hash_code % self._capacity

        node = self._buckets[da_index].contains(key)

        if node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair with the given key from the hash map.

        Params: Key to be removed.

        Return: None
        """
        hash_code = self._hash_function(key)

        da_index = hash_code % self._capacity

        node = self._buckets[da_index].contains(key)

        if node:
            if node.key == key:
                self._buckets[da_index].remove(key)
                self._size -= 1
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Get a dynamic array of key-value pairs in the hash map.

        Params: None

        Return: Dynamic array containing key-value pairs.
        """
        ret_da = DynamicArray()

        for linked_list in range(self._capacity):
            iterator = self._buckets[linked_list].__iter__()
            for elem in iterator:
                ret_da.append((elem.key, elem.value))

        return ret_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Find the mode or modes and frequency in a given dynamic array.

    Params: Dynamic array

    Return: A tuple containing a dynamic array of mode or modes and the frequency.
    """

    h_map = HashMap(da.length(), hash_function_1)
    for i in range(da.length()):
        count = 1
        if not h_map.contains_key(da.get_at_index(i)):
            h_map.put(str(da.get_at_index(i)), count)

        elif h_map.contains_key(da.get_at_index(i)):
            count = h_map.get(da.get_at_index(i))
            count += 1
            h_map.put(str(da.get_at_index(i)), count)

    h_map_keys_vals_da = h_map.get_keys_and_values()

    mode_da = DynamicArray()

    freq = 0

    for i in range(h_map_keys_vals_da.length()):
        if h_map_keys_vals_da[i][1] > freq:
            freq = h_map_keys_vals_da[i][1]

    for i in range(h_map_keys_vals_da.length()):
        if h_map_keys_vals_da[i][1] == freq:
            mode_da.append(h_map_keys_vals_da[i][0])

    return mode_da, freq


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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
