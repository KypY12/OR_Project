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

        # This method returns multiple independent sets that correspond to the columns that were generated
        indep_sets = []
        for mw_subgraph in self.max_weight_subgraphs:


            found_indep_set = TabuSearchHeuristic(weight=mw_subgraph,
                                                 pi_vals=self.pi_vals,
                                                 subgraph=self.max_weight_subgraphs.get(mw_subgraph)).execute()
            print(found_indep_set)
            print(self.check_independency_subgraph(found_indep_set))

            # TO DO: implement alg described in the paper for solving the subproblem (first try TabuSearch then BnB)
            # ...
            # ...
            # ...
            #pass

        return indep_sets


