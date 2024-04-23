class Node:
    def __init__(self, id, properties=None):
        self.id = id
        self.properties = properties if properties else {}

class Edge:
    def __init__(self, start_node, end_node, relation, properties=None):
        self.start_node = start_node
        self.end_node = end_node
        self.relation = relation
        self.properties = properties if properties else {}

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, id, properties=None):
        if id not in self.nodes:
            self.nodes[id] = Node(id, properties)

    def add_edge(self, start_node, end_node, relation, properties=None):
        if start_node in self.nodes and end_node in self.nodes:
            new_edge = Edge(start_node, end_node, relation, properties)
            self.edges.append(new_edge)
