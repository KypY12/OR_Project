import random
import copy


class TabuSearchHeuristic:

    def __init__(self, pi_vals, weight, subgraph, max_iterations=100, beta=1.1):
        self.pi_vals = pi_vals
        self.weight = weight
        self.subgraph = subgraph
        self.nodes = subgraph["nodes"]
        self.neighbourhoods = subgraph["neighbourhoods"]
        self.max_iteations = max_iterations
        self.beta = beta

        self.tabu_list = dict()
        self.nodes_out_indep_set = []

        self.max = 0
        self.current_indep_set = []
        self.found_indep_set = []

    def __generate_random_maximal_indep_set__(self):
        nodes = copy.deepcopy(self.nodes)

        random.shuffle(nodes)

        indep_set = []

        for node in nodes:

            is_feasible = True
            for other in indep_set:
                if node in self.neighbourhoods[other]:
                    is_feasible = False
                    break

            if is_feasible:
                indep_set.append(node)

        return indep_set

    def __sum_of_pis__(self, indep_set):

        return sum([self.pi_vals[node] for node in indep_set])

    def __check_number_connections_to_indep_set(self, neighbours, indep_set, num_connections):

        return len(set(neighbours).intersection(set(indep_set))) == num_connections

    def __get_nodes_connected_to_indep_set__(self, num_connections):
        nodes_unused = [node for node in self.nodes if node not in self.current_indep_set]

        self.nodes_out_indep_set = []
        for node in nodes_unused:

            if self.__check_number_connections_to_indep_set(self.neighbourhoods[node], self.current_indep_set, num_connections):
                self.nodes_out_indep_set.append(node)

    def __get_node_connected_from_indep_set__(self, node_out, num_connections):
        nodes_in_indep_set = list(set(self.neighbourhoods[node_out]).intersection(set(self.current_indep_set)))

        if num_connections == 1:
            return nodes_in_indep_set[0]
        elif num_connections == 2:
            return nodes_in_indep_set[0], nodes_in_indep_set[1]

    def __update_tabu_list__(self):

        for node in self.tabu_list:
            self.tabu_list[node] -= 1

            if self.tabu_list[node] == 0:
                del self.tabu_list[node]

    def __expand_random_maximal_indep_set__(self):
        nodes_unused = [node for node in self.nodes if node not in self.current_indep_set]
        random.shuffle(nodes_unused)

        for node in nodes_unused:
            is_feasible = True

            for other_node in self.current_indep_set:
                if node in self.neighbourhoods[other_node]:
                    is_feasible = False
                    break

            if is_feasible:
                self.current_indep_set.append(node)

    def __execute_1_1_exchange__(self):
        for out_node in self.nodes_out_indep_set:
            in_node = self.__get_node_connected_from_indep_set__(node_out=out_node, num_connections=1)

            new_indep_set = copy.deepcopy(self.current_indep_set)
            new_indep_set.remove(in_node)
            new_indep_set.append(out_node)

            if out_node not in self.tabu_list:
                if self.__sum_of_pis__(new_indep_set) >= self.max or \
                        self.__sum_of_pis__(new_indep_set) > self.__sum_of_pis__(self.found_indep_set):

                    self.current_indep_set = copy.deepcopy(new_indep_set)
                    self.max = self.__sum_of_pis__(self.current_indep_set)

                    self.tabu_list[in_node] = len(self.current_indep_set) + 1
                    return "exchanged"

        return "unchanged"

    def __execute_2_1_exchange__(self):
        for out_node in self.nodes_out_indep_set:
            first_in_node, second_in_node = self.__get_node_connected_from_indep_set__(node_out=out_node, num_connections=2)

            new_indep_set = copy.deepcopy(self.current_indep_set)
            new_indep_set.remove(first_in_node)
            new_indep_set.remove(second_in_node)
            new_indep_set.append(out_node)

            if out_node not in self.tabu_list:
                if self.__sum_of_pis__(new_indep_set) >= self.max or \
                        self.__sum_of_pis__(new_indep_set) > self.__sum_of_pis__(self.found_indep_set):

                    self.current_indep_set = copy.deepcopy(new_indep_set)
                    self.max = self.__sum_of_pis__(self.current_indep_set)

                    self.tabu_list[first_in_node] = len(self.current_indep_set) + 1
                    self.tabu_list[second_in_node] = len(self.current_indep_set) + 1
                    return "exchanged"

        return "unchanged"

    def execute(self):

        self.current_indep_set = self.__generate_random_maximal_indep_set__()
        self.found_indep_set = copy.deepcopy(self.current_indep_set)

        if self.__sum_of_pis__(self.found_indep_set) > self.beta * self.weight:
            return self.found_indep_set

        for iteration in range(self.max_iteations):
            self.max = -1

            # 1-1 exchange
            self.__get_nodes_connected_to_indep_set__(num_connections=1)

            while True:
                exec_response = self.__execute_1_1_exchange__()
                if exec_response == "exchanged":
                    self.__get_nodes_connected_to_indep_set__(num_connections=1)
                elif exec_response == "unchanged":
                    break

            # 2-1 exchange
            if self.max == -1:
                self.__get_nodes_connected_to_indep_set__(num_connections=2)

                while True:
                    exec_response = self.__execute_2_1_exchange__()
                    if exec_response == "exchanged":
                        self.__get_nodes_connected_to_indep_set__(num_connections=2)
                    elif exec_response == "unchanged":
                        break

            # expand the independent set
            self.__expand_random_maximal_indep_set__()

            # update the independent set
            if self.__sum_of_pis__(self.current_indep_set) > self.__sum_of_pis__(self.found_indep_set):
                self.found_indep_set = copy.deepcopy(self.current_indep_set)

            # return the independent set
            if self.__sum_of_pis__(self.found_indep_set) > self.beta * self.weight or self.max == -1:
                return self.found_indep_set

            # update number iterations for nodes in tabu list
            self.__update_tabu_list__()

        return self.found_indep_set
