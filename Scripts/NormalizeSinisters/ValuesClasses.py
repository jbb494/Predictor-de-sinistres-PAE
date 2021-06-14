from typing import Dict, List
import numpy as np
import numpy.typing as npt


class Column:
    values: npt.ArrayLike

    def __init__(self, values: List[int]):
        self.values = values

    # def __iadd__(self, other):
    #     self.values = np.append(self.values, other.values)
    #     return self.values


class Month:
    columns: List[Column]

    def __init__(self):
        self.columns = list()

    def __iadd__(self, other):
        col = Column(other)
        self.columns = self.columns.append(col)
        return self.columns


class PostalCodes:
    months: Dict[str, Month]

    def __init__(self):
        self.months = dict()

    def __getattribute__(self, month):
        if month not in self.months:
            self.months[month] = Month()
        return self.months[month]


class ValuesClass:
    postal_codes: Dict[str, PostalCodes]

    def __init__(self):
        self.postal_codes = dict()

    def __getattribute__(self, cp):
        if cp not in self.postal_codes:
            self.postal_codes[cp] = PostalCodes()
        return self.postal_codes[cp]
