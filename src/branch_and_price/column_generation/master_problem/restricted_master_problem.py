from src.linear_programs.lp_solvers.gurobi_solver import GurobiSolver
from src.linear_programs.wvcp_linear_program import WVCPLinearProgram


class RestrictedMasterProblem:

    def __init__(self, graph, indep_sets):
        self.lp = WVCPLinearProgram(graph, indep_sets)

    def add_column(self, indep_set):
        if len(indep_set) > 0:
            self.lp.add_columns([indep_set])

    def solve_relaxation(self):

        solver = GurobiSolver(self.lp.A, self.lp.b, self.lp.c, lb=0, ub=1)

        if not solver.is_unbounded_or_unfeasible():
            return solver.get_sol(), solver.get_obj(), solver.get_pi()
        else:
            return -1, -1, -1
