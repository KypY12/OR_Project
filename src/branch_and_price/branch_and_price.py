import time
from copy import deepcopy

import numpy as np

from src.branch_and_price.column_generation.master_problem.restricted_master_problem import RestrictedMasterProblem
from src.branch_and_price.column_generation.subproblem.subproblems_solver import SubproblemsSolver
from src.graphs.graph import Graph
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

    def __same_color_branch__(self, i, j, current_graph, current_indep_sets):

        graph = Graph().copy_from_graph(current_graph)
        indep_sets = deepcopy(current_indep_sets)

        low_node = min([i, j])
        high_node = max([i, j])

        # Merge the two nodes into one
        graph.original_nodes[low_node] += graph.original_nodes[high_node]

        # Set the new node weight to the max weight
        graph.nodes_weights[low_node] = max(graph.nodes_weights[low_node], graph.nodes_weights[high_node])

        # Remove independent sets that will become invalid after merging low_node and high_node
        new_indep_sets = []
        for indep_set in indep_sets:

            is_feasible = True
            contains_high_node = high_node in indep_set
            contains_low_node = low_node in indep_set

            if contains_high_node and not contains_low_node:

                # Remove independent sets that contain high node and at least one node that is adjacent with low node
                for node in indep_set:
                    if node in graph.neighbourhoods[low_node]:
                        is_feasible = False
                        break

            elif not contains_high_node and contains_low_node:

                # Remove independent sets that contain low node and at least one node that is adjacent with high node
                for node in indep_set:
                    if node in graph.neighbourhoods[high_node]:
                        is_feasible = False
                        break

            if is_feasible:
                new_indep_sets.append(indep_set)

        indep_sets = new_indep_sets

        # Add high node neighbours to the new node (at low node index)
        graph.neighbourhoods[low_node] = [
            neigh for neigh in list(set(graph.neighbourhoods[low_node] + graph.neighbourhoods[high_node]))
            if neigh != low_node and neigh != high_node
        ]

        # Replace the high_node with the new node (with the same index as low_node)
        # and decrement the index of nodes higher than high_node in the independent sets
        for sets_index, indep_set in enumerate(indep_sets):
            remove_index = -1

            for index, node in enumerate(indep_set):

                if node == high_node:

                    if low_node in indep_set:  # if low_node is already in the set, just remove high_node
                        remove_index = index
                    else:  # otherwise replace high_node with low_node
                        indep_set[index] = low_node

                elif node > high_node:
                    indep_set[index] -= 1

            if remove_index > -1:
                indep_set.pop(remove_index)

        # Do the same thing in the neighbourhoods
        for node, neighs in enumerate(graph.neighbourhoods):

            if node != high_node:  # the high_node neighbours will be removed, so its neighbours don't concern us here
                remove_index = -1

                for index, other in enumerate(neighs):

                    if other == high_node:

                        if low_node in neighs:  # if low_node is in neighbours, just remove the high_node later
                            remove_index = index
                        else:  # otherwise replace high_node with low_node
                            neighs[index] = low_node

                    elif other > high_node:
                        neighs[index] -= 1

                if remove_index > -1:
                    neighs.pop(remove_index)

        # Remove high node from the graph
        graph.number_of_nodes -= 1
        graph.neighbourhoods.pop(high_node)
        graph.nodes_weights.pop(high_node)
        graph.original_nodes.pop(high_node)
        graph.max_weight_subgraphs = dict()

        # Return the new problem
        return {"rmp": RestrictedMasterProblem(graph, indep_sets),
                "sp_solver": SubproblemsSolver(graph),
                "branch_type": "same_color"}

    def __different_color_branch__(self, i, j, current_graph, current_indep_sets):

        graph = Graph().copy_from_graph(current_graph)
        indep_sets = deepcopy(current_indep_sets)

        # Add the new edge
        graph.neighbourhoods[i].append(j)
        graph.neighbourhoods[j].append(i)

        # Remove the sets that contain both i and j (they are no longer independent sets)
        indep_sets = [indep_set for indep_set in indep_sets
                      if i not in indep_set or j not in indep_set]

        # Return the new problem
        return {"rmp": RestrictedMasterProblem(graph, indep_sets),
                "sp_solver": SubproblemsSolver(graph),
                "branch_type": "different_color"}

    def __branch__(self, max_fractional, rmp):

        graph = rmp.lp.graph
        indep_sets = rmp.lp.indep_sets

        indep_sets_max_weights = [max([graph.nodes_weights[node] for node in indep_set]) for indep_set in indep_sets]
        graph_weights_sorted = sorted(list(set(graph.nodes_weights)))

        # Get independent set S1
        S1 = indep_sets[max_fractional]

        # Get node i
        i = S1[np.argmax([graph.nodes_weights[node] for node in S1])]
        i_weight_index = graph_weights_sorted.index(graph.nodes_weights[i])

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

            if i_weight_index > 0:
                #   Search by the second condition
                searched_weight = graph_weights_sorted[i_weight_index - 1]

                for w_index, m_weight in enumerate(indep_sets_max_weights):
                    if m_weight == searched_weight:
                        S2 = indep_sets[w_index]
                        break

            if len(S2) == 0 and i_weight_index < len(graph_weights_sorted) - 1:
                #   Search by the third condition
                searched_weight = graph_weights_sorted[i_weight_index + 1]

                for w_index, m_weight in enumerate(indep_sets_max_weights):
                    if m_weight == searched_weight:
                        S2 = indep_sets[w_index]
                        break

        j = -1
        if len(S2) > 0:
            # Get node j
            #   Get the elements that are either in S1 or in S2, but not in both (symmetric difference)
            #   and remove node i
            j_candidates = list((set(S1) ^ set(S2)) - {i})
            #   Only nodes that are not adjacent to i
            j_candidates = [j_c for j_c in j_candidates if j_c not in graph.neighbourhoods[i]]

            if len(j_candidates) > 0:
                j_candidates_weights = [graph.nodes_weights[node] for node in j_candidates]
                j = j_candidates[np.argmax(j_candidates_weights)]

        if j > -1:
            return [
                self.__different_color_branch__(i, j, graph, indep_sets),
                self.__same_color_branch__(i, j, graph, indep_sets),
            ]
        else:
            return []

    def __solve_problem__(self, rmp, sp_solver):

        new_columns = [0]
        is_bounded = True
        sol, obj = 0, 0

        while len(new_columns) > 0:
            sol, obj, pi_vals = rmp.solve_relaxation()

            if sol == -1:
                is_bounded = False
                break

            sp_solver.set_pi_vals(pi_vals)
            new_columns = sp_solver.solve()

            rmp.add_columns(new_columns)

        return is_bounded, sol, obj

    def execute(self):

        start = time.perf_counter()
        indep_sets = IndependentSetsInitializer(self.graph).simple_assignation()

        rmp = RestrictedMasterProblem(self.graph, indep_sets)
        sp_solver = SubproblemsSolver(self.graph)

        problems_stack = [{"rmp": rmp,
                           "sp_solver": sp_solver,
                           "branch_type": "ROOT"}]

        best_so_far = {"sol": -1,
                       "obj": -1,
                       "rmp": -1}

        while len(problems_stack) > 0:

            problem = problems_stack.pop()

            print("================")
            print(problem["branch_type"])
            print("SOLVING RMP")

            is_bounded, sol, obj = self.__solve_problem__(problem["rmp"], problem["sp_solver"])

            if is_bounded and (best_so_far["rmp"] == -1 or obj < best_so_far["obj"]):

                max_fractional = self.__get_max_fractional__(sol)

                if max_fractional == -1:
                    # if the solution is integer (binary)
                    best_so_far = {"sol": sol,
                                   "obj": obj,
                                   "rmp": problem["rmp"]}

                    self.__print_best_so_far__(best_so_far)

                else:
                    print("BRANCHING ...")

                    problems_stack += self.__branch__(max_fractional, problem["rmp"])

        end = time.perf_counter()

        return best_so_far, end - start

    def __print_best_so_far__(self, best_found):

        print(f"OBJECTIVE FUNCTION : {best_found['obj']}")
        print(f"SOLUTION : {best_found['sol']}")
