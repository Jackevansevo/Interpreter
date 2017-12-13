from attr import attrs, attrib
from collections import namedtuple
from operator import attrgetter

Param = namedtuple('Param', ['type', 'name'])


@attrs
class Node:
    tok = attrib()

    @property
    def is_constant(self):
        return self.tok.isdigit()

    @property
    def is_leaf(self):
        return not any([self.lhs, self.rhs])

    @property
    def is_func(self):
        return self.tok == 'D'

    @property
    def return_type(self):
        if self.is_func:
            return self.lhs.lhs.tok

    @property
    def func_params(self):
        if not self.lhs.rhs.rhs:
            return []
        signature = self.lhs.rhs.rhs
        leaf_nodes = filter(attrgetter('is_leaf'), iter(signature))
        param_nodes = [leaf.tok for leaf in leaf_nodes]
        return [Param(*p) for p in zip(param_nodes[::2], param_nodes[1::2])]

    @property
    def func_args(self):
        if self.tok == ",":
            yield from self.lhs.func_args
            yield from self.rhs.func_args
        else:
            yield self

    def __iter__(self):
        yield self
        if self.lhs:
            yield from self.lhs
        if self.rhs:
            yield from self.rhs
