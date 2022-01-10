import numpy as np


class WVCPLinearProgram:

    def __init__(self, graph, indep_sets):

        self.graph = graph

        # The independent sets from the RMP (Restricted Master Problem).
        # They correspond to the variables of the LP (in this order).
        self.indep_sets = indep_sets

        # The coefficients of the variables in the objective function (in the same order as in indep_set).
        # These coefficients are actually indep_sets' costs (the highest weight in each indep set).
        self.c = self.__assign_c__()

        # The constraints variables (one constraint for each node in the graphs, so A has always nodes_count rows).
        self.A = self.__assign_A__()
        # b is always constant (because there is always the same number of nodes in the graphs).
        self.b = np.array([1 for _ in range(graph.number_of_nodes)])

    def __get_max_weight__(self, indep_set):
        max_weight = 0

        for node in indep_set:
            current_weight = self.graph.nodes_weights[node]

            if current_weight > max_weight:
                max_weight = current_weight

        return max_weight

    def __assign_c__(self):

        return np.array([self.__get_max_weight__(indep_set) for indep_set in self.indep_sets])

    def __assign_A__(self):

        return np.array([[1 if node in indep_set else 0 for indep_set in self.indep_sets]
                         for node in range(self.graph.number_of_nodes)])

    def __add_columns_to_c__(self, indep_sets):

        new_columns = np.array([self.__get_max_weight__(indep_set) for indep_set in indep_sets])
        self.c = np.concatenate([self.c, new_columns], axis=0)

    def __add_columns_to_A__(self, indep_sets):

        new_columns = np.array([[1 if node in indep_set else 0 for indep_set in indep_sets]
                                for node in range(self.graph.number_of_nodes)])
        self.A = np.concatenate([self.A, new_columns], axis=1)

    def add_columns(self, current_indep_sets):

        indep_sets = [indep_set for indep_set in current_indep_sets if indep_set not in self.indep_sets]

        if len(indep_sets) > 0:
            self.indep_sets += indep_sets
            self.__add_columns_to_A__(indep_sets)
            self.__add_columns_to_c__(indep_sets)

        else:
            current_indep_sets.clear()
