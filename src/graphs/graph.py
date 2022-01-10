from copy import deepcopy


class Graph:

    def __init__(self):

        self.number_of_nodes = 0

        self.neighbourhoods = []
        self.nodes_weights = []

        self.max_weight_subgraphs = dict()

        self.original_nodes = []

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

        self.original_nodes = [[x] for x in range(self.number_of_nodes)]

        self.neighbourhoods = [list() for _ in range(self.number_of_nodes)]
        self.nodes_weights = [0 for _ in range(self.number_of_nodes)]

        for edges in edges_str:
            tokens = edges.split(sep)

            tokens = [elem for elem in tokens if len(elem) > 0]

            left = int(tokens[1]) - 1
            right = int(tokens[2]) - 1

            if left != right:
                if right not in self.neighbourhoods[left]:
                    self.neighbourhoods[left] += [right]

                if left not in self.neighbourhoods[right]:
                    self.neighbourhoods[right] += [left]

        for node in nodes_str:
            tokens = node.split(sep)
            tokens = [elem for elem in tokens if len(elem) > 0]

            node = int(tokens[1]) - 1
            weight = int(tokens[2])

            self.nodes_weights[node] = weight

        return self

    def copy_from_graph(self, graph):
        self.number_of_nodes = graph.number_of_nodes

        self.neighbourhoods = deepcopy(graph.neighbourhoods)
        self.nodes_weights = deepcopy(graph.nodes_weights)

        self.max_weight_subgraphs = deepcopy(graph.max_weight_subgraphs)

        self.original_nodes = deepcopy(graph.original_nodes)

        return self

    def get_neighbours(self, node):
        return self.neighbourhoods[node]

    def subgraphs_by_max_weight(self):

        self.max_weight_subgraphs = dict()

        graph_weights = list(set(self.nodes_weights))

        for weight in graph_weights:

            # Get the nodes that have at most the current weight
            current_nodes = []
            for node, node_weight in enumerate(self.nodes_weights):
                if node_weight <= weight:
                    current_nodes.append(node)

            # Get the edges of the subgraph with nodes from 'current_nodes'
            current_neighbourhoods = dict()
            for node, node_neighbours in enumerate(self.neighbourhoods):
                if node in current_nodes:
                    current_neighbourhoods[node] = [neigh for neigh in node_neighbours if neigh in current_nodes]

            self.max_weight_subgraphs[weight] = {"nodes": current_nodes,
                                                 "neighbourhoods": current_neighbourhoods}

        return self.max_weight_subgraphs
