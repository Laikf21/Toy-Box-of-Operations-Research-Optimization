





import copy
from lib2to3.pytree import Node
import re
import math
import itertools
import numpy as np


Nodes = [1, 2, 3, 4]

nodeNum = len(Nodes)

dis_matrix = np.array([[0, 8, 12, 17]
                    , [4, 0, 10, 9]
                    , [7, 14, 0, 13]
                    , [9, 7, 11, 0]])

def TSP_Dynamic_Programming(Nodes, dis_matrix):
    Labet_set = {}
    nodeNum = len(Nodes)
    org = 1

    # cycle stage: V, V-1, ..., 2
    for stage_ID in range(nodeNum, 1, -1):
        print('stage :', stage_ID)
        for i in range(2, nodeNum+1):
            current_node = i
            left_node_list = copy.deepcopy(Nodes)
            if (org in left_node_list):
                left_node_list.remove(org)
            left_node_set = set(left_node_list)

            #obtain all the subset of left node set
            subset_all = list( map(set, itertools.combinations(left_node_set, nodeNum - stage_ID)) )

            for subset in subset_all:
                if(len(subset) == 0):
                    key = (stage_ID, current_node, "None")
                    next_node = org
                    Labet_set[key] = [dis_matrix[i-1][org-1], next_node]
                else:
                    key = (stage_ID, current_node)
                    min_distance = 1000000
                    for temp_next_node in subset:
                        subsub_set = copy.deepcopy(subset)
                        subsub_set.remove(temp_next_node)
                        if(subsub_set == None or len(subsub_set) == 0):
                            subsub_set = 'None'
                        sub_key = (stage_ID +1, temp_next_node, str(subsub_set))
                        if (sub_key in Labet_set.keys()):
                            if(dis_matrix[current_node - 1][temp_next_node-1] + Labet_set[sub_key][0] < min_distance):
                                min_distance = dis_matrix[current_node - 1][temp_next_node-1]+Labet_set[sub_key][0]
                                next_node = temp_next_node
                                Labet_set[key] = [min_distance, next_node]

    # stage 1
    stage_ID = 1
    current_node = org
    subset = set(copy.deepcopy(Nodes))
    subset.remove(org)
    final_key = (stage_ID, current_node, str(subset))
    min_distance = 1000000
    for temp_next_node in subset:
        subsub_set = copy.deepcopy(subset)
        subsub_set.remove(temp_next_node)
        if(subsub_set == None or len(subsub_set) == 0):
            subsub_set = 'None'
        sub_key = (stage_ID +1, temp_next_node,str(subsub_set))
        if(sub_key in Labet_set.keys()):
            if(dis_matrix[current_node-1][temp_next_node-1] + Labet_set[sub_key][0]<min_distance):
                min_distance = dis_matrix[current_node-1][temp_next_node-1]+Labet_set[sub_key][0]
                next_node = temp_next_node
                Labet_set[final_key] = [min_distance, next_node]

    #extract optimal solution
    opt_route = [org]
    not_visited_node = set(copy.deepcopy(Nodes))
    not_visited_node.remove(org)
    next_node = Labet_set[final_key][1]
    while True:
        opt_route.append(next_node)
        if( len(opt_route) == nodeNum +1):
            break
        current_stage = len(opt_route)
        not_visited_node.remove(next_node)
        if( not_visited_node == None or len(not_visited_node)==0 ):
            not_visited_node = 'None'
        next_key = (current_stage, next_node, str(not_visited_node))
        next_node = Labet_set[next_key][1]

    opt_dis = Labet_set[final_key][0]
    
    print('objective value:', Labet_set[final_key][0])
    print('optimal rounte:', opt_route)

    return opt_dis, opt_route

# call DP function to solve TSP
opt_dis, opt_route = TSP_Dynamic_Programming(Nodes, dis_matrix)
print('\n\n -------------- optimal solution --------------\n')
print('objevtive:', opt_dis)
print('optimal rounte:', opt_route)