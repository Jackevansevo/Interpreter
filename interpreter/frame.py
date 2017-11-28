from collections import ChainMap


class Frame:

    def __init__(self, _bindings, parent):
        self._bindings = _bindings
        self.parent = parent

        # Override bound variables in parent frames
        if self.parent:
            for frame in self.parent:
                current, new = _bindings.items(), frame._bindings
                frame._bindings.update({k: v for k, v in current if k in new})

    def get(self, value):
        return self.bindings.get(value)

    @property
    def bindings(self):
        return ChainMap(*(frame._bindings for frame in iter(self)))

    def __iter__(self):
        yield self
        if self.parent:
            yield from self.parent

    def __getitem__(self, key):
        return self.bindings[key]

    def __setitem__(self, key, val):
        self._bindings[key] = val
        if self.parent:
            for frame in self.parent:
                if key in frame._bindings:
                    frame._bindings[key] = val

    def __str__(self):
        return f'{self._bindings}'

    def __repr__(self):
        return f'{self._bindings}->{repr(self.parent)}'
