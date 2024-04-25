import json

class Node:
    def __init__(self, id, label=None, color=None, shape="dot", size=None, cid=None):
        self.id = id
        self.label = label or str(id)
        self.color = color
        self.shape = shape
        self.size = size
        self.cid = cid

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "color": self.color,
            "shape": self.shape,
            "size": self.size,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"Node({self.id}, \'{self.label}\', \'{self.color}\', \'{self.shape}\', {self.size}, {self.cid})"