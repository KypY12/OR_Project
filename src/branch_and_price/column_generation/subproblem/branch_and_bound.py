class BranchAndBound:

    def __init__(self, pi_vals, weight, subgraph):

        self.weight = weight

        self.nodes_indices = dict()
        self.nodes = subgraph["nodes"]
        self.neighbourhoods = {self.nodes[index]: subgraph["neighbourhoods"][index] for index in range(len(self.nodes))}

        self.pi_vals = {self.nodes[index]: pi_vals[index] for index in range(len(pi_vals))}

    def __sum_of_pis__(self, indep_set):

        return sum([self.pi_vals[node] for node in indep_set])

    def __first_pruning_rule_check__(self, S, F, X):

        for x in X:
            if self.pi_vals[x] >= self.__sum_of_pis__((set(S) | set(F)) & set(self.neighbourhoods[x])):
                return True

        return False

    def __weighted_clique_cover_construction_heuristic__(self, LB, F):

        wcc_nodes_lists = []
        wcc_weights = []

        weight_sorted_nodes = sorted(self.nodes, key=lambda t: self.pi_vals[t])




        pass

    def __second_pruning_rule_check__(self):

        weighted_clique_cover = self.__weighted_clique_cover_construction_heuristic__()

        return weighted_clique_cover, False

    def __first_branching_rule__(self):

        pass

    def __second_branching_rule__(self):

        pass

    def __third_branching_rule__(self):

        pass

    def __find_branch_vertices__(self):

        pass

    def execute(self):

        S = []
        F = list(self.nodes)
        X = []

        # S = current set
        # F = free vertices
        # X = excluded vertices
        bnb_stack = [{"S": S,
                      "F": F,
                      "X": X}]

        best_so_far = []

        while len(bnb_stack) > 0:

            current_sets = bnb_stack.pop()

            # First pruning rules
            if len(current_sets["F"]) > 0 and not self.__first_pruning_rule_check__():

                weighted_clique_cover, is_rule_checked = self.__second_pruning_rule_check__()

                if not is_rule_checked:
                    branch_vertices = self.__find_branch_vertices__()
                    #
                    #
                    # BRANCHING LOOP
                    #
                    pass

                pass
