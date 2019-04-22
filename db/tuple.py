class Tuple:
    def __init__(self, primary_key, attributes, values, split_abutes=True):
        self._data = []
        self._primary_key = primary_key

        if split_abutes:
            for value in values:
                self._data.append(value['value'])
        else:
            self._data = values

    def get_primary_key(self):
        return self._primary_key

    def get_value_for_index(self, i):
        return self._data[i]

    def _get_data(self):
        return self._data

    def merge(self, new_tuple):
        abutes = {}
        new_data = self._data + new_tuple._get_data()
        return Tuple(self._primary_key, abutes, new_data, False)

    def _print_str(self):
        s = ""
        for d in self._data:
            if d is None:
                s += "? "
                # print("? ", end='')
            else:
                s += str(d) + " "
                # print(str(d) + " ", end='')
        return s

    def print(self):
        print(self._print_str())

    def get_primary_key(self):
        return self._primary_key

    def __lt__(self, other):
        return self._primary_key < other.get_primary_key()

    def __le__(self, other):
        return self._primary_key <= other.get_primary_key()

    def __eq__(self, other):
        return self._primary_key == other.get_primary_key()

    def __ne__(self, other):
        return self._primary_key != other.get_primary_key()

    def __gt__(self, other):
        return self._primary_key > other.get_primary_key()

    def __ge__(self, other):
        return self._primary_key >= other.get_primary_key()

    def __str__(self):
        return "(" + str(self._primary_key) + ": " + self._print_str() + ")"