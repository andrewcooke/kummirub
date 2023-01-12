from typing import Set


class ImmutableSet(Set):

    def __init__(self, entries):
        self.__set = frozenset(entries)

    def add(self, entry):
        entries = set(self.__set)
        entries.add(entry)
        return ImmutableSet(entries)

    def __contains__(self, entry):
        return entry in self.__set

    def __iter__(self):
        yield from self.__set

    def __eq__(self, other):
        return isinstance(other, ImmutableSet) and other.__set == self.__set

    def __len__(self):
        return len(self.__set)
