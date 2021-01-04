import csv

import csv_linq_cell_trims as trims

class HeaderCollection:
    def __init__(self, header):
        self.header = header
        self.header_map = {hdr : i for i, hdr in enumerate(header)}

    def from_id(self, id):
        return self.header[id]

    def from_hdr(self, hdr):
        return self.header_map[hdr]

class WhereGen:
    def __init__(self, collection, header, row_num, criterion):
        self.collection = collection
        self.header = header
        self.row_num = row_num
        self.criterion = criterion

    def where(self, row, criterion):
        try:
            row = self.header.from_hdr(row)
        except KeyError:
            pass

        return WhereGen(self, self.header, row, criterion)

    def get_header(self):
        return self.collection.get_header()

    def __next__(self):
        try:
            for row in self.collection:
                if not row:
                    raise StopIteration
                if self.criterion(row[self.row_num]):
                    return row
        except StopIteration:
            raise
        except TypeError:
            raise StopIteration

    def __iter__(self):
        return self


class CsvLinq:
    def __init__(self, path, *cell_strips, delimiter=",", decimal_separator="."):
        self.decimal_separator = decimal_separator

        if len(cell_strips) == 0:
            trim_pipe = trims.TrimPipeline(trims.StripWhitespaces(), trims.RemoveChars('"'))
        else:
            trim_pipe = trims.TrimPipeline(*cell_strips)

        with open(path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)

            self.header = HeaderCollection(list(map(trim_pipe, next(reader))))
            self.lines = [list(map(trim_pipe, line)) for line in reader if line]
            self.len = len(self.lines)

    def get_header(self):
        return self.header

    def where(self, row, criterion):
        try:
            row = self.header.from_hdr(row)
        except KeyError:
            pass

        return WhereGen(iter(self), self.header, row, criterion)

    def __iter__(self):
        return CsvLinq.CsvLinqIterator(self)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        return self.lines[idx]

    class CsvLinqIterator:
        def __init__(self, csv):
            self.csv = csv
            self.index = 0
            self.len = len(csv)

        def __iter__(self):
            if self.index == self.len:
                raise StopIteration
            return self

        def __next__(self):

            if self.index < self.len:
                result = self.csv[self.index]
                self.index += 1

                return result

            raise StopIteration


from pathlib import Path

csv_path = Path(r"D:\Arbeit\CsvLinq\Tests\cities.csv")

l = CsvLinq(csv_path)
for r in l.where("LatD", lambda x : x == "42"):

    print(r)