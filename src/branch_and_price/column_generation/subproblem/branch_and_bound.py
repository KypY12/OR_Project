import numpy as np


class BranchAndBound:

    def __init__(self, pi_vals, subgraph, weight, beta=1.1):

        self.weight = weight
        self.beta = beta

        self.nodes_indices = dict()
        self.nodes = subgraph["nodes"]
        self.neighbourhoods = subgraph["neighbourhoods"]

        self.pi_vals = pi_vals

        self.LB = -np.inf
        self.LB_S = []

    def __sum_of_pis__(self, indep_set):

        return sum([self.pi_vals[node] for node in indep_set])

    def __first_pruning_rule_check__(self, S, F, X):

        for x in X:
            if self.pi_vals[x] >= self.__sum_of_pis__((set(S) | set(F)) & set(self.neighbourhoods[x])):
                return True

        return False

    def __get_maximal_clique_for_node__(self, node, nodes_set):

        maximal_clique = [node]

        for current_node in nodes_set:

            is_feasible = True

            for clique_node in maximal_clique:
                if current_node not in self.neighbourhoods[clique_node]:
                    is_feasible = False
                    break

            if is_feasible:
                maximal_clique.append(current_node)

        return maximal_clique

    def __weighted_clique_cover_construction_heuristic__(self, S, F):

        wcc_nodes_lists = []
        wcc_weights = []
        wcc_weights_sum = 0

        not_visited = list(F)
        temp_pi_vals = list(self.pi_vals)

        stop_condition_term = self.LB - self.__sum_of_pis__(S)
        stop_condition = False

        while len(not_visited) > 0:

            v = min(not_visited, key=lambda t: temp_pi_vals[t])
            not_visited.remove(v)

            v_maximal_clique = self.__get_maximal_clique_for_node__(v, not_visited)
            v_maximal_clique_weight = temp_pi_vals[v]

            wcc_nodes_lists.append(v_maximal_clique)
            wcc_weights.append(v_maximal_clique_weight)

            for node in v_maximal_clique:
                temp_pi_vals[node] -= v_maximal_clique_weight

            wcc_weights_sum += v_maximal_clique_weight
            if wcc_weights_sum > stop_condition_term:
                stop_condition = True
                break

        if stop_condition:
            # save branch info (non-zero-weight nodes)
            return [node for node in F if temp_pi_vals[node] != 0], False
        else:
            # pruning
            return [], True

    def __second_branching_rule__(self, S, F, X):

        for x in X:
            if self.pi_vals[x] >= self.__sum_of_pis__(set(S) & set(self.neighbourhoods[x])) and \
                    self.__sum_of_pis__(F) > self.LB - self.__sum_of_pis__(S):
                return list(set(self.neighbourhoods[x]) & set(F))

        return []

    def __third_branching_rule__(self, F):

        for f in F:
            if self.pi_vals[f] >= self.__sum_of_pis__(set(F) & set(self.neighbourhoods[f])):
                return [f]

        return []

    def __find_branch_vertices__(self, non_zero_nodes, S, F, X):

        branching_sets = [non_zero_nodes,
                          self.__second_branching_rule__(S, F, X),
                          self.__third_branching_rule__(F)]

        branching_dict = {b_index: len(branching_sets[b_index]) for b_index in range(len(branching_sets))
                          if len(branching_sets[b_index]) > 0}

        # Return the smallest branching set
        return branching_sets[min(branching_dict, key=lambda t: branching_dict[t])]

    def execute(self):

        # S = current set
        # F = free vertices
        # X = excluded vertices
        S, F, X = [], list(self.nodes), []
        bnb_stack = [(S, F, X)]

        self.LB = 0
        self.LB_S = []

        while len(bnb_stack) > 0:

            S, F, X = bnb_stack.pop()

            current_LB = self.__sum_of_pis__(S)

            if current_LB > self.LB:
                self.LB = current_LB
                self.LB_S = list(S)

                # If we find an independent set with the weight higher than the target weight, then return
                if self.LB > self.beta * self.weight:
                    return self.LB_S

            # First pruning rule
            if len(F) > 0 and not self.__first_pruning_rule_check__(S, F, X):

                # Second pruning rule
                non_zero_nodes, apply_pruning = self.__weighted_clique_cover_construction_heuristic__(S, F)

                if not apply_pruning:

                    F_p = self.__find_branch_vertices__(non_zero_nodes, S, F, X)
                    p = len(F_p)

                    for i, f_i in list(enumerate(F_p))[::-1]:
                        new_X = list(X)
                        new_F = list(set(F) - (set(self.neighbourhoods[f_i]) | set(F_p[i:p])))
                        new_S = list(S + [f_i])

                        bnb_stack.append((new_S, new_F, new_X))
                        X += [f_i]

        return self.LB_S
