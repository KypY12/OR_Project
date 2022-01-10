from src.branch_and_price.branch_and_price import BranchAndPrice

from src.graphs.graph import Graph


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

    # with open(f"./results/{instance_file_path.split('/')[-1][:-4]}", "w") as file:
    #     data_to_write = \
    #         f"OBJECTIVE FUNCTION : {obj}\n" + \
    #         f"SOLUTION : {solution}\n" + \
    #         f"INDEP SETS : {original_sol_indep_sets}\n" + \
    #         f"INDEP SETS WEIGHTS : {indep_sets_weights}\n" + \
    #         f"EXECUTION TIME : {elapsed_time} seconds"
    #     file.write(data_to_write)


instances_paths = [
    # "./instances/R50_1g.col",
    # "./instances/R50_1gb.col",
    # "./instances/R50_9g.col",
    "./instances/R50_9gb.col",

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

    # "./instances/GEOM30b.col",
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
