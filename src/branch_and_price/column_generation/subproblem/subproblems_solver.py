class SubproblemsSolver:

    def __init__(self, graph):
        self.pi_vals = []
        self.graph = graph

        self.max_weight_subgraphs = self.graph.subgraphs_by_max_weight()

    def set_pi_vals(self, pi_vals):
        self.pi_vals = pi_vals

    def solve(self):

        if len(self.pi_vals) == 0:
            raise Exception("Subproblem pi values need to be set before solve() call!")

        # This method returns multiple independent sets that correspond to the columns that were generated
        indep_sets = []

        for mw_subgraph in self.max_weight_subgraphs:
            # TO DO: implement alg described in the paper for solving the subproblem (first try TabuSearch then BnB)
            # ...
            # ...
            # ...
            pass

        return indep_sets
