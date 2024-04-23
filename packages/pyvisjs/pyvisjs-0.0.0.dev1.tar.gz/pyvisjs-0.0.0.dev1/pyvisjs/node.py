class Node:
    def __init__(self, id, label, cid=None):
        self.id = id
        self.label = label
        self.cid = cid

    def __repr__(self):
        return f"Node({self.id}, \'{self.label}\', {self.cid})"