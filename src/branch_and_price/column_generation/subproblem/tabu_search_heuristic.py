import random


class TabuSearchHeuristic:

    def __init__(self, pi_vals, subgraph, max_iterations=100, beta=1.1):
        self.pi_vals = pi_vals
        self.subgraf = subgraph
        self.max_iterations = max_iterations
        self.beta = beta

        self.tabu_list = []

    def __generate_random_maximal_indep_set__(self):
        nodes = self.subgraf["nodes"].copy()

        random.shuffle(nodes)

        indep_set = []

        for node in nodes:

            is_feasible = True
            for other in indep_set:
                if node in self.subgraf["neighbourhoods"][other]:
                    is_feasible = False
                    break

            if is_feasible:
                indep_set.append(node)

        return indep_set

    def __sum_of_pis__(self, indep_set):

        sum_of_pi_vals = 0
        for node in indep_set:
            sum_of_pi_vals += self.pi_vals[node]

        return sum_of_pi_vals



    def execute(self):

        current_indep_set = self.__generate_random_maximal_indep_set__()

        # TO DO : finish implementation
