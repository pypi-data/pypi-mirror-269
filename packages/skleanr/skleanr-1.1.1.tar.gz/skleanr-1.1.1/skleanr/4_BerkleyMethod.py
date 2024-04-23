import time

# Time server node index
TIME_SERVER_NODE = 0

# Time server offset in seconds
TIME_SERVER_OFFSET = 0

# Node class representing a node in the network
class Node:
    def __init__(self, id, offset):
        self.id = id
        self.offset = offset
        self.clock = time.time()  # Initialize the clock with the current time in seconds

    # Method to adjust the clock offset of the node
    def adjust_clock(self, offset):
        self.clock += offset

# Function to synchronize all nodes in the network
def synchronize_clocks(nodes):
    # Calculate the time of the time server node
    server_time = nodes[TIME_SERVER_NODE].clock + TIME_SERVER_OFFSET
    
    # Adjust offset to each node
    for node in nodes:
        if node.id != TIME_SERVER_NODE:
            node_time = node.clock + node.offset
            offset = server_time - node_time
            node.adjust_clock(offset)

# Main function
def main():
    # Create nodes in the network
    nodes = [
        Node(1, 10),  # Node 1 with 10 seconds offset
        Node(2, -5),  # Node 2 with -5 seconds offset
        Node(3, 20)   # Node 3 with 20 seconds offset
    ]

    # Print initial clock values of all nodes
    print("Before synchronization:")
    for node in nodes:
        print(f"Node {node.id} clock: {node.clock}")

    # Synchronize clocks of all nodes
    synchronize_clocks(nodes)

    # Print clock values of all nodes after synchronization
