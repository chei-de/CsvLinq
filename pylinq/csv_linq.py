import csv

import csv_linq_cell_trims as trims
import linq_gen as lg

class HeaderCollection:
    def __init__(self, header):
        self.header = header
        self.header_map = {hdr : i for i, hdr in enumerate(header)}

    def from_id(self, id):
        return self.header[id]

    def from_hdr(self, hdr):
        return self.header_map[hdr]

    def from_hdr_best_bet(self, hdr):
        result = [i for i, val in enumerate(self.header) if hdr.lower() in val.lower()]

        if len(result) == 0:
            raise ValueError("No Header found that is similar to {}".format(hdr))

        return result[0]

    def __str__(self):
        return ", ".join(self.header)

class CsvLinq:
    def __init__(self, csv_file, *cell_strips, delimiter=",", decimal_separator="."):
        self.decimal_separator = decimal_separator

        if len(cell_strips) == 0:
            trim_pipe = trims.TrimPipeline(trims.StripWhitespaces(), trims.RemoveChars('"'))
        else:
            trim_pipe = trims.TrimPipeline(*cell_strips)

        reader = csv.reader(csv_file, delimiter=delimiter)

        self.header = HeaderCollection(list(map(trim_pipe, next(reader))))
        self.lines = [list(map(trim_pipe, line)) for line in reader if line]
        self.len = len(self.lines)

    def get_header(self):
        return self.header

    def __iter__(self):
        for line in self.lines:
            yield line

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        return self.lines[idx]

# from pathlib import Path
# csv_path = Path(r"D:\Arbeit\CsvLinq\Tests\cities.csv")

# l = CsvLinq(csv_path)
# headerset = l.get_header()

# for r in lg.LinqGenerator.new(l).\
#             where(lambda x: x[headerset.from_hdr("LatD")] == "41").\
#             where(lambda x: int(x[headerset.from_hdr("LatM")]) > 40):
#     print(r) 