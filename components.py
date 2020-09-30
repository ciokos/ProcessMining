class Place:
    def __init__(self, id):
        self.id = id
        self.tokens = 0


class Transition:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

