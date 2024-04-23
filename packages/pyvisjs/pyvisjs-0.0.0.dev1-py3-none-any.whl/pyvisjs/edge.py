class Edge:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Edge({self.start}, {self.end})"