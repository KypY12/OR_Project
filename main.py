'''
OR Project Reading implementation
    Adam Cristian - MOC1
    Chiparus Alexandru-Denis - MOC1

Article: "Exact weighted vertex coloring via branch-and-price", Fabio Furini, Enrico Malaguti

Problem: Weighted Vertex Coloring Problem
    + Description:
        A positive weight is associated to each vertex of a graphs.
        A color is associated to each vertex in such a way that:
            -> colors on adjacent vertices are different;
            -> the objective is to to minimize the sum of costs of the colors used
            -> the cost of a color is the maximum weight of the vertices assigned to that color

    + Notation:
        -> G = (V, E) (the graphs from the problem) ;
        -> m = |V| ;
        -> n = |E| ;
        -> w_i = the weight of node i ;
        -> W = {w : exists i in V, w_i = w} (the set of weights that appear in V) ;
        -> (S_handwritten)_w = family of all independent sets of G
                               having the heaviest vertex of weight w (the cost is w) ;
        -> S [in (S_handwritten)_w] = an independent set [of cost w];
        -> x_S = a binary variable which take the value 1 when all vertices of S receive the same color and
                                                        0 when at least two vertices in S receive different colors. ;

    + Definitions:
        -> Independent set = a subset of V in which no two adjacent vertices belong to it.
                            (A coloring for the graphs is a partition of vertex set into independent sets)
        -> Color classes = the independent sets of a coloring.

'''
from src.graphs.graph import Graph
from src.initializers.independent_sets_initializer import IndependentSetsInitializer
from src.linear_programs.lp_solvers.gurobi_solver import GurobiSolver
from src.linear_programs.wvcp_linear_program import WVCPLinearProgram

if __name__ == '__main__':

    graph = Graph().from_file("./instances/R50_1g.col")

    # print(graphs.edges)
    # print(graphs.nodes_weights)

    indep_sets = IndependentSetsInitializer(graph).simple_assignation()

    print(indep_sets)

    lp = WVCPLinearProgram(graph, indep_sets)

    print(lp.c)
    print(lp.A)
    print(lp.b)

    solver = GurobiSolver(lp.A, lp.b, lp.c)

    if not solver.is_unbounded_or_unfeasible():
        print(solver.get_sol())
        print(solver.get_obj())
        print(solver.get_pi())

    pi_vals = solver.get_pi()