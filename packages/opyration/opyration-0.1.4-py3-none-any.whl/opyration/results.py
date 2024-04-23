from collections import deque


class Lookup(dict):
    def __init__(self, data: dict):
        super().__init__(data)
        self._data = data

    def __getattr__(self, key: str):
        value = self._data.get(key)
        if isinstance(value, dict):
            return Lookup(value)
        return value

    def __getitem__(self, key: str):
        return self._data.get(key)

    def __setitem__(self, key: str, value):
        self._data[key] = value
    
    def __delitem__(self, key: str):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __dict__(self):
        return self._data


class Results(object):
    def __init__(self, data: list):
        self.__data = data
        self.__queue = deque(data)
        self.__count = 0

    def __bool__(self):
        return bool(self.__queue)

    def data(self):
        return self.__data

    def next(self):
        try: return Lookup(self.__queue[self.__count])
        except: return None
        finally: self.__count += 1

    def pop(self):
        try: datum = self.__queue.popleft()
        except IndexError: return None
        else: return Lookup(dict(datum))

    def reset(self, index: int = 0):
        self.__count = index

    def row(self, n: int):
        if n < 1: n = 1
        try: return Lookup(dict(self.__queue[n - 1]))
        except: return None

    def rows(self, n: int):
        if n > len(self.__queue): n = len(self.__queue)
        return [self.pop() for _ in range(n)]
