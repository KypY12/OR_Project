import sys

import numpy as np
from gurobipy import GRB

from src.branch_and_price.column_generation.subproblem.branch_and_bound import BranchAndBound
from src.branch_and_price.column_generation.subproblem.tabu_search_heuristic import TabuSearchHeuristic
from src.linear_programs.lp_solvers.gurobi_solver import GurobiSolver


class SubproblemsSolver:

    def __init__(self, graph):
        self.pi_vals = []
        self.graph = graph

        self.max_weight_subgraphs = self.graph.subgraphs_by_max_weight()

    def set_pi_vals(self, pi_vals):
        self.pi_vals = pi_vals

    def check_independency_subgraph(self, indep_set):
        for node in indep_set:
            for other_node in indep_set:
                if node != other_node and node in self.graph.neighbourhoods[other_node]:
                    return False

        return True

    def __create_lp_problem__(self, nodes, neighbourhoods, pis, weight):

        c = [pis[node] for node in nodes]

        b_size = sum([len(neighbourhoods[node]) for node in nodes]) // 2

        if b_size == 0:
            return []

        b = [1 for _ in range(b_size)]

        A = []
        visited = []
        for node in nodes:
            visited.append(node)
            for neigh in neighbourhoods[node]:
                if neigh not in visited:
                    A.append([1 if n == node or n == neigh else 0 for n in nodes])

        c = np.array(c)
        b = np.array(b)
        A = np.array(A)

        solver = GurobiSolver(A, b, c, 0, np.inf, "<=", GRB.BINARY, GRB.MAXIMIZE)

        if solver.is_unbounded_or_unfeasible():
            return []

        sol = solver.get_sol()

        if solver.get_obj() <= weight:
            return []

        return sorted([nodes[index] for index, value in enumerate(sol) if value == 1])

    def solve(self):

        if len(self.pi_vals) == 0:
            raise Exception("Subproblem pi values need to be set before solve() call!")

        indep_sets = []

        # for mw_subgraph in self.max_weight_subgraphs:
        #     nodes = self.max_weight_subgraphs.get(mw_subgraph)["nodes"]
        #     neighbourhoods = self.max_weight_subgraphs.get(mw_subgraph)["neighbourhoods"]
        #     pis = {node: self.pi_vals[node] for node in nodes}
        #
        #     found_indep_set = self.__create_lp_problem__(nodes, neighbourhoods, pis, mw_subgraph)
        #
        #     if len(found_indep_set) > 0 and found_indep_set not in indep_sets:
        #         indep_sets.append(found_indep_set)

        for mw_subgraph in self.max_weight_subgraphs:
            found_indep_set = TabuSearchHeuristic(weight=mw_subgraph,
                                                  pi_vals=self.pi_vals,
                                                  subgraph=self.max_weight_subgraphs.get(mw_subgraph)).execute()
            if len(found_indep_set) > 0 and found_indep_set not in indep_sets:
                indep_sets.append(found_indep_set)

            # else:
            #     found_indep_set = BranchAndBound(weight=mw_subgraph,
            #                                      pi_vals=self.pi_vals,
            #                                      subgraph=self.max_weight_subgraphs.get(mw_subgraph)).execute()
            #     if len(found_indep_set) > 0 and found_indep_set not in indep_sets:
            #         indep_sets.append(found_indep_set)

        if len(indep_sets) == 0:
            for mw_subgraph in self.max_weight_subgraphs:
                found_indep_set = BranchAndBound(weight=mw_subgraph,
                                                 pi_vals=self.pi_vals,
                                                 subgraph=self.max_weight_subgraphs.get(mw_subgraph)).execute()
                if len(found_indep_set) > 0 and found_indep_set not in indep_sets:
                    indep_sets.append(found_indep_set)

        return indep_sets
