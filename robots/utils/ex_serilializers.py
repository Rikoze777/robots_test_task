import sys


class ReturnDict(dict):

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)

    def copy(self):
        return ReturnDict(self, serializer=self.serializer)

    def __repr__(self):
        return dict.__repr__(self)

    def __reduce__(self):
        return (dict, (dict(self),))

    if sys.version_info >= (3, 9):

        def __or__(self, other):
            if not isinstance(other, dict):
                return NotImplemented
            new = self.__class__(self, serializer=self.serializer)
            new.update(other)
            return new

        def __ror__(self, other):
            if not isinstance(other, dict):
                return NotImplemented
            new = self.__class__(other, serializer=self.serializer)
            new.update(self)
            return new


class ReturnList(list):

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return list.__repr__(self)

    def __reduce__(self):
        return (list, (list(self),))