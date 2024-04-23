from pyvisjs import Network

# Create a Network instance
net = Network()

# Add nodes and edges
net.add_node(1)
net.add_node(2)
net.add_edge(1, 2)

# Display the network
net.show("example.html")