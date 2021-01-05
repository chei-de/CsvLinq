class LinqGenerator:
    BARE = 0
    FILTER = 1
    TRANSFORMER = 2

    def __init__(self, collection, mode, criterion = None):
        self.collection = collection

        if mode == LinqGenerator.BARE:
            self.gen = self.__bare_gen
        elif mode == LinqGenerator.FILTER:
            self.gen = self.__filter_gen
        elif mode == LinqGenerator.TRANSFORMER:
            self.gen = self.__transform_gen
        else:
            raise ValueError("Only BARE={}, FILTER={} and TRANSFORMER={} are supported"\
                                "for mode parameter".format(LinqGenerator.BARE, LinqGenerator.FILTER, LinqGenerator.TRANSFORMER))

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
        return LinqGenerator(self.gen(), LinqGenerator.FILTER, criterion = filter_criterion)

    def select(self, transform_criterion):
        return LinqGenerator(self.gen(), LinqGenerator.TRANSFORMER, criterion = transform_criterion)

    @staticmethod
    def new(collection):
        return LinqGenerator(collection, LinqGenerator.BARE)

class LinqGroupByGen:
    pass