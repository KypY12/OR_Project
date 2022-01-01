class Graph:

    def __init__(self):

        self.number_of_nodes = 0
        self.edges = []
        self.nodes_weights = []

    def from_file(self, file_path, sep=' '):

        edges_str = []
        nodes_str = []
        with open(file_path, "r") as file:
            line = file.readline()

            while line:
                if line.startswith("e"):
                    edges_str.append(line)
                elif line.startswith("n"):
                    nodes_str.append(line)
                line = file.readline()

        self.number_of_nodes = len(nodes_str)

        self.edges = [list() for _ in range(self.number_of_nodes)]
        self.nodes_weights = [0 for _ in range(self.number_of_nodes)]

        for edges in edges_str:
            tokens = edges.split(sep)
            left = int(tokens[1]) - 1
            right = int(tokens[2]) - 1

            self.edges[left] += [right]
            self.edges[right] += [left]

        for node in nodes_str:
            tokens = node.split(sep)
            node = int(tokens[1]) - 1
            weight = int(tokens[2])

            self.nodes_weights[node] = weight

        return self

    def from_params(self, edges, nodes_weights):
        self.edges, self.nodes_weights = edges, nodes_weights

    def get_neighbours(self, node):
        return self.edges[node]


