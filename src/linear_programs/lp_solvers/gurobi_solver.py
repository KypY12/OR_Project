import gurobipy as gp
from gurobipy import GRB


class GurobiSolver:

    def __init__(self, A, b, c, lb, ub):
        self.env = gp.Env(empty=True)
        self.env.setParam("LogToConsole", 0)
        self.env.start()

        self.A, self.b, self.c = A, b, c
        self.lb, self.ub = lb, ub

        self.model, self.x = self.__solve__()

    def __solve__(self):
        # Create the model
        model = gp.Model("Gurobi Model", env=self.env)

        # Create the variables
        x = model.addMVar(shape=self.c.shape, vtype=GRB.CONTINUOUS, name="x", lb=self.lb, ub=self.ub)

        # Set the objective function
        model.setObjective(self.c @ x, GRB.MINIMIZE)

        # Create the constraints
        model.addConstr(self.A @ x >= self.b, name="constraints")

        model.optimize()

        return model, x

    def is_unbounded_or_unfeasible(self):
        return self.model.getAttr(GRB.attr.Status) == GRB.INF_OR_UNBD or \
               self.model.getAttr(GRB.attr.Status) == GRB.INFEASIBLE or \
               self.model.getAttr(GRB.attr.Status) == GRB.UNBOUNDED

    def get_obj(self):
        # Returns the optimal value of the objective function
        return self.model.objVal

    def get_sol(self):
        # Returns the optimal solution
        return self.x.x.tolist()

    def get_pi(self):
        # Return the values of the optimal solution of the dual problem
        return self.model.Pi
