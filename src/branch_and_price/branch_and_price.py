from src.branch_and_price.column_generation.master_problem.restricted_master_problem import RestrictedMasterProblem
from src.branch_and_price.column_generation.subproblem.subproblems_solver import SubproblemsSolver
from src.initializers.independent_sets_initializer import IndependentSetsInitializer


class BranchAndPrice:

    def __init__(self, graph):

        self.graph = graph
        self.indep_sets = IndependentSetsInitializer(graph).simple_assignation()

        self.rmp = RestrictedMasterProblem(self.graph, self.indep_sets)
        self.sp_solver = SubproblemsSolver(self.graph)

    def execute(self):

        # TO DO: implement BnP like BnB from homeworks (based on wikipedia diagram and the article)



        pass
