class IndependentSetsInitializer:

    def __init__(self, graph):
        self.graph = graph

    def simple_assignation(self):

        indep_sets = []

        visited = [0 for _ in range(self.graph.number_of_nodes)]
        print(visited)

        for node in range(self.graph.number_of_nodes):

            if visited[node] == 0:
                visited[node] = 1

                current_indep_set = [node]

                for other in range(node + 1, self.graph.number_of_nodes):

                    if visited[other] == 0:
                        is_feasible = True

                        for current in current_indep_set:
                            if other in self.graph.neighbourhoods[current]:
                                is_feasible = False
                                break

                        if is_feasible:
                            current_indep_set += [other]
                            visited[other] = 1

                indep_sets += [current_indep_set]

        return indep_sets
