import enum

class IteratorMode(enum.Enum):
    BARE = 0
    FILTER = 1
    TRANSFORMER = 2

class LinqGenerator:

    def __init__(self, collection, mode, criterion = None):
        self.collection = collection

        if mode == IteratorMode.BARE:
            self.gen = self.__bare_gen
        elif mode == IteratorMode.FILTER:
            self.gen = self.__filter_gen
        elif mode == IteratorMode.TRANSFORMER:
            self.gen = self.__transform_gen
        else:
            raise ValueError("Only BARE={}, FILTER={} and TRANSFORMER={} are supported"\
                                "for mode parameter".format(IteratorMode.BARE, IteratorMode.FILTER, IteratorMode.TRANSFORMER))

        self.criterion = criterion

    def __iter__(self):
        return self.gen()

    def __bare_gen(self):
        for val in self.collection:
            yield val

    def __filter_gen(self):
        for val in self.collection:
            if self.criterion(val):
                yield val

    def __transform_gen(self):
        for val in self.collection:
            yield self.criterion(val)

    def where(self, filter_criterion):
        return LinqGenerator(self.gen(), IteratorMode.FILTER, criterion = filter_criterion)

    def select(self, transform_criterion):
        return LinqGenerator(self.gen(), IteratorMode.TRANSFORMER, criterion = transform_criterion)

    def group_by(self, key_selector):
        return LinqGroupByGen(self.gen(), key_selector)

    def count(self):
        return len(self.collection)

    def sum(self, selector):
        return sum(selector(item) for item in self.collection)

    @staticmethod
    def new(collection):
        return LinqGenerator(collection, IteratorMode.BARE)

class LinqGroupByGen:
    def __init__(self, collection, key_selector):
        self.collection = {}

        for row in self.collection:
            key = key_selector(row)

            try:
                self.collection[key].append(row)
            except KeyError:
                self.collection[key] = [row]

    def gen(self):
        for key in self.collection.keys():
            yield key

    def items(self):
        return self.collection.items()

    def __getitem__(self, key):
        return LinqGenerator(self.collection[key], IteratorMode.BARE)

    def __iter__(self):
        return self.gen()

    @staticmethod
    def new(collection, key_selector):
        return LinqGroupByGen(collection, key_selector)