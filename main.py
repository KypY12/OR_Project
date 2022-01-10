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
import os

from src.branch_and_price.branch_and_price import BranchAndPrice

from src.graphs.graph import Graph


def test(graphs):
    print(graphs.edges)
    print(graphs.nodes_weights)

    # indep_sets = IndependentSetsInitializer(graph).simple_assignation()
    #
    # print(indep_sets)
    #
    # lp = WVCPLinearProgram(graph, indep_sets)
    #
    # print(lp.c)
    # print(lp.A)
    # print(lp.b)
    #
    # solver = GurobiSolver(lp.A, lp.b, lp.c, 0, 1)
    #
    # if not solver.is_unbounded_or_unfeasible():
    #     print(solver.get_sol())
    #     print(solver.get_obj())
    #     print(solver.get_pi())
    #
    # pi_vals = solver.get_pi()
    #
    # rmp = RestrictedMasterProblem(graph, indep_sets)
    #
    # subgraphs = graph.subgraphs_by_max_weight()
    #
    # sol, obj, pi_vals = rmp.solve_relaxation()
    #
    # weights = sorted(list(set(graph.nodes_weights)))
    #
    # i = 4
    # res_indep_set = BranchAndBound(pi_vals, subgraphs[weights[i]], weights[i]).execute()
    #
    # print("BNB : ", sorted(res_indep_set))
    # print(SubproblemsSolver(graph).check_independency_subgraph(res_indep_set))
    #
    # found_indep_set = TabuSearchHeuristic(weight=weights[i],
    #                                       pi_vals=pi_vals,
    #                                       subgraph=subgraphs[weights[i]]).execute()
    #
    # print("TABU : ", sorted(found_indep_set))
    # print(SubproblemsSolver(graph).check_independency_subgraph(found_indep_set))


def run_for_instance(instance_file_path):
    graph = Graph().from_file(instance_file_path)

    best_found, elapsed_time = BranchAndPrice(graph=graph,
                                              epsilon=1e-8).execute()

    solution = best_found["sol"]
    obj = best_found["obj"]

    print(f"OBJECTIVE FUNCTION : {obj}")
    print(f"SOLUTION : {solution}")

    rmp = best_found["rmp"]
    indep_sets = rmp.lp.indep_sets

    solution_indep_sets = []
    for index, value in enumerate(solution):
        if value == 1:
            solution_indep_sets.append(indep_sets[index])

    original_nodes = rmp.lp.graph.original_nodes

    original_sol_indep_sets = []
    for indep_set in solution_indep_sets:

        current_set = []
        for node in indep_set:
            current_set += original_nodes[node]

        original_sol_indep_sets.append(current_set)

    indep_sets_weights = [max([graph.nodes_weights[node] for node in indep_set])
                          for indep_set in original_sol_indep_sets]
    indep_sets_weight = sum(indep_sets_weights)

    print(f"ACTUAL WEIGHT : {indep_sets_weight}")
    print(f"INDEP SETS : {original_sol_indep_sets}")
    print(f"INDEP SETS WEIGHTS : {indep_sets_weights}")
    print(f"EXECUTION TIME : {elapsed_time} seconds")

    with open(f"./results/{instance_file_path.split('/')[-1][:-4]}", "w") as file:
        data_to_write = \
            f"OBJECTIVE FUNCTION : {obj}\n" + \
            f"SOLUTION : {solution}\n" + \
            f"INDEP SETS : {original_sol_indep_sets}\n" + \
            f"INDEP SETS WEIGHTS : {indep_sets_weights}\n" + \
            f"EXECUTION TIME : {elapsed_time} seconds"
        file.write(data_to_write)


instances_paths = [
    # "./instances/R50_1g.col",
    # "./instances/R50_1gb.col",
    # "./instances/R50_9g.col",
    # "./instances/R50_9gb.col",

    # "./instances/R50_5g.col",
    # "./instances/R50_5gb.col",

    # "./instances/R75_9g.col",
    # "./instances/R75_9gb.col",
    # "./instances/R75_1g.col",
    # "./instances/R75_1gb.col",
    # "./instances/R100_9g.col",
    # "./instances/R100_9gb.col",
    # "./instances/R75_5g.col",
    # "./instances/R75_5gb.col",

    "./instances/GEOM30b.col",
    # "./instances/GEOM40b.col",
    # "./instances/GEOM50b.col",
    # "./instances/GEOM60b.col",

    # "./instances/GEOM70.col",
    # "./instances/GEOM70a.col",
    # "./instances/GEOM70b.col",
    # "./instances/GEOM80.col",
    # "./instances/GEOM80a.col",
    # "./instances/GEOM80b.col",

    # "./instances/GEOM90.col",
    # "./instances/GEOM90a.col",
    # "./instances/GEOM90b.col",
    # "./instances/GEOM100.col",
    # "./instances/GEOM100a.col",
    # "./instances/GEOM100b.col",

    # "./instances/GEOM110.col",
    # "./instances/GEOM110a.col",
    # "./instances/GEOM110b.col",

    # "./instances/GEOM120.col",
    # "./instances/GEOM120a.col",
    # "./instances/GEOM120b.col",

    # "./instances/DSJC125.9g.col",
    # "./instances/DSJC125.9gb.col"
]

if __name__ == '__main__':

    for path in instances_paths:
        run_for_instance(path)
