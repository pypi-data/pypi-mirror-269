import json

class Edge:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def to_dict(self):
        return {
            "from": self.start,
            "to": self.end,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"Edge({self.start}, {self.end})"