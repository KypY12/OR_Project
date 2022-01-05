from copy import deepcopy

import numpy as np

from src.branch_and_price.column_generation.master_problem.restricted_master_problem import RestrictedMasterProblem
from src.branch_and_price.column_generation.subproblem.subproblems_solver import SubproblemsSolver
from src.initializers.independent_sets_initializer import IndependentSetsInitializer


class BranchAndPrice:

    def __init__(self, graph, epsilon):

        self.graph = graph
        self.epsilon = epsilon

    def __get_max_fractional__(self, sol):

        max_fractional_index = -1
        max_fractional_part = -1

        for index, elem in enumerate(sol):
            fractional_part = elem - np.floor(elem)

            if fractional_part > self.epsilon and (
                    max_fractional_index == -1 or fractional_part > max_fractional_part):
                max_fractional_index = index
                max_fractional_part = fractional_part

        return max_fractional_index

    def __same_color_branch__(self, i, j, graph, indep_sets):

        graph = graph.copy()
        indep_sets = deepcopy(indep_sets)

        low_node = min([i, j])
        high_node = max([i, j])

        # Merge the two nodes into one
        graph.original_nodes[low_node] += graph.original_nodes[high_node]

        # Set the new node weight to the max weight
        graph.nodes_weights[low_node] = max(graph.nodes_weights[low_node], graph.nodes_weights[high_node])

        # Replace the high_node with the new node (with the same index as low_node)
        # and decrement the index of nodes higher than high_node in the independent sets
        for sets_index, indep_set in enumerate(indep_sets):
            for index, node in enumerate(indep_set):
                if node == high_node:
                    indep_sets[sets_index][index] = low_node
                elif node > high_node:
                    indep_sets[sets_index][index] -= 1
        #             !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

        # Remove high node from the graph
        graph.number_of_nodes -= 1
        graph.neighbourhoods.pop(high_node)
        graph.nodes_weights.pop(high_node)
        graph.original_nodes.pop(high_node)
        graph.max_weight_subgraphs = dict()

        # Return the new problem
        return {"rmp": RestrictedMasterProblem(graph, indep_sets),
                "sp_solver": SubproblemsSolver(graph)}

    def __different_color_branch__(self, i, j, graph, indep_sets):

        graph = graph.copy()
        indep_sets = deepcopy(indep_sets)

        # Add the new edge
        graph.neighbourhoods[i].append(j)
        graph.neighbourhoods[j].append(i)

        # Remove the sets that contain both i and j (they are no longer independent sets)
        indep_sets = [indep_set for indep_set in indep_sets
                      if i not in indep_set or j not in indep_set]

        # Return the new problem
        return {"rmp": RestrictedMasterProblem(graph, indep_sets),
                "sp_solver": SubproblemsSolver(graph)}

    def __branch__(self, max_fractional, rmp):

        graph = rmp.lp.graph
        indep_sets = rmp.lp.indep_sets

        indep_sets_max_weights = [max([graph.nodes_weights[node] for node in indep_set]) for indep_set in indep_sets]

        # Get independent set S1
        S1 = indep_sets[max_fractional]

        # Get node i
        i = S1[np.argmax([graph.nodes_weights[node] for node in S1])]

        # Get independent set S2
        S2 = []
        #   Search by the first condition
        for index, indep_set in enumerate(indep_sets):
            if index != max_fractional and \
                    i in indep_set and \
                    indep_sets_max_weights[index] == graph.nodes_weights[i]:
                # if indep_set contains i and its cost is equal to the weight of i
                S2 = indep_set
                break

        if len(S2) == 0:

            graph_weights_sorted = sorted(list(set(graph.nodes_weights)))
            i_weight_index = graph_weights_sorted.index(graph.nodes_weights[i])

            if i_weight_index > 0:
                #   Search by the second condition
                weight = graph_weights_sorted[i_weight_index - 1]

            else:
                #   Search by the third condition
                weight = graph_weights_sorted[i_weight_index + 1]

            S2 = indep_sets[indep_sets_max_weights.index(weight)]

        # Get node j
        #   Get the elements that are either in S1 or in S2, but not in both (symmetric difference)
        #   and remove node i
        j_candidates = list((set(S1) ^ set(S2)) - {i})
        j_candidates_weights = [graph.nodes_weights[node] for node in j_candidates]
        j = j_candidates[np.argmax(j_candidates_weights)]

        return [self.__same_color_branch__(i, j, graph, indep_sets),
                self.__different_color_branch__(i, j, graph, indep_sets)]

    def __solve_problem__(self, rmp, sp_solver):
        new_column = [0]
        is_bounded = True
        sol, obj = 0, 0

        new_columns = []
        while len(new_column) > 0:
            sol, obj, pi_vals = rmp.solve_relaxation()

            if (sol, obj, pi_vals) == (-1, -1, -1):
                is_bounded = False
                break

            print(pi_vals)
            sp_solver.set_pi_vals(pi_vals)
            new_column = sp_solver.solve()

            if new_column in new_columns:
                print("wrong")

            new_columns += [new_column]

            rmp.add_column(new_column)

        return is_bounded, sol, obj

    def execute(self):
        # Independent Sets Initialization
        indep_sets = IndependentSetsInitializer(self.graph).simple_assignation()

        rmp = RestrictedMasterProblem(self.graph, indep_sets)
        sp_solver = SubproblemsSolver(self.graph)

        problems_stack = [{"rmp": rmp,
                           "sp_solver": sp_solver}]

        best_so_far = {"sol": -1,
                       "obj": -1,
                       "rmp": -1}

        while len(problems_stack) > 0:

            problem = problems_stack.pop()

            is_bounded, sol, obj = self.__solve_problem__(**problem)

            print(sol)
            print(obj)
            print("================")

            if is_bounded and (best_so_far["rmp"] == -1 or obj > best_so_far["obj"]):

                max_fractional = self.__get_max_fractional__(sol)

                if max_fractional == -1:
                    # if the solution is integer (binary)
                    best_so_far = {"sol": sol,
                                   "obj": obj,
                                   "rmp": problem["rmp"]}
                    print(best_so_far)

                else:
                    problems_stack += self.__branch__(max_fractional, problem["rmp"])
