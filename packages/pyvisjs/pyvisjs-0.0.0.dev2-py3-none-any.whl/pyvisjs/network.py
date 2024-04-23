from .utils import open_file, save_file
from .node import Node
from .edge import Edge
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict

class Network:

    def __init__(self, name="Network", data:Dict = {"nodes": [], "edges": []}, width="600px", height="400px"):
        self.name = name
        self.width = width
        self.height = height
        self.data = data
        self.env = Environment(
            loader=FileSystemLoader("pyvisjs/templates"),
            autoescape=select_autoescape()
        )

    def __repr__(self):
        return f"Network(\'{self.name}\', \'{self.width}\', \'{self.height}\')"
    
    def add_node(self, node_id):
        self.data["nodes"].append(Node(node_id))

    def add_edge(self, from_id, to_id):
        self.data["edges"].append(Edge(from_id, to_id))

    def show(self, file_name):
        self.render_template(open_in_browser=True, output_filename=file_name)

    def render_template(self, open_in_browser=False, save_to_output=False, output_filename="default.html", template_filename="basic.html") -> str:
        html_output = self.env \
            .get_template(template_filename) \
            .render(
                width=self.width,
                height=self.height,
                data=self.data
            )

        if save_to_output or open_in_browser:
            file_path = save_file(output_filename, html_output)

        if open_in_browser:
            open_file(file_path)

        return html_output
        
