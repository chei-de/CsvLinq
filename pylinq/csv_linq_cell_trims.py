class Identity:
    def __call__(self, inp):
        return inp

class StripWhitespaces:
    def __call__(self, inp):
        return inp.strip()

class RemoveChars:

    def __init__(self, *args):
        self.remove_chars = args

    def __call__(self, inp):
        for char in self.remove_chars:
            inp = inp.replace(char, '')

        return inp

class TrimPipeline:

    def __init__(self, *trimmer):
        self.trimmer = trimmer

    def __call__(self, inp):
        for trim in self.trimmer:
            inp = trim(inp)

        return inp



