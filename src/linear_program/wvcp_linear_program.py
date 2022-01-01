import numpy as np


class WVCPLinearProgram:

    def __init__(self, graph, indep_sets):

        self.graph = graph

        # The independent sets from the RMP (Restricted Master Problem).
        # They correspond to the variables of the LP (in this order).
        self.indep_sets = indep_sets

        # The coefficients of the variables in the objective function (in the same order as in indep_set).
        # These coefficients are actually indep_sets' costs (the highest weight in each indep set).
        self.c = self.__assign_c__(graph, indep_sets)

        # The constraints variables (one constraint for each node in the graph, so A has always nodes_count rows).
        self.A = self.__assign_A__(graph, indep_sets)
        # b is always constant (because there is always the same number of nodes in the graph).
        self.b = np.array([1 for _ in range(graph.number_of_nodes)])

    def __assign_c__(self, graph, indep_sets):

        def get_max_weight(indep_set):
            max_weight = 0

            for node in indep_set:
                current_weight = graph.nodes_weights[node]

                if current_weight > max_weight:
                    max_weight = current_weight

            return max_weight

        return np.array([get_max_weight(indep_set) for indep_set in indep_sets])

    def __assign_A__(self, graph, indep_sets):

        return np.array(
            [[1 if node in indep_set else 0 for indep_set in indep_sets] for node in range(graph.number_of_nodes)])
