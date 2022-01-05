from src.branch_and_price.column_generation.subproblem.branch_and_bound import BranchAndBound
from src.branch_and_price.column_generation.subproblem.tabu_search_heuristic import TabuSearchHeuristic


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

    def solve(self):

        if len(self.pi_vals) == 0:
            raise Exception("Subproblem pi values need to be set before solve() call!")

        found_indep_set = []

        for mw_subgraph in self.max_weight_subgraphs:
            found_indep_set = TabuSearchHeuristic(weight=mw_subgraph,
                                                  pi_vals=self.pi_vals,
                                                  subgraph=self.max_weight_subgraphs.get(mw_subgraph)).execute()
            if len(found_indep_set) > 0:
                break

        if len(found_indep_set) == 0:
            for mw_subgraph in self.max_weight_subgraphs:
                found_indep_set = BranchAndBound(weight=mw_subgraph,
                                                 pi_vals=self.pi_vals,
                                                 subgraph=self.max_weight_subgraphs.get(mw_subgraph)).execute()
                if len(found_indep_set) > 0:
                    break

        return found_indep_set
