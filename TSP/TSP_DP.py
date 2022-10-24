'''
该版本的TSP动态规划问题成功求解
'''

import copy
import re
import math
import itertools
import numpy as np


Nodes = [1, 2, 3, 4]

nodeNum = len(Nodes)

dis_matrix = np.array([[0, 8, 12, 17]
                     ,[4, 0, 10, 9]
                     ,[7, 14, 0, 13]
                     ,[9, 7, 11, 0]])



def TSP_Dynamic_Programming(Nodes, dis_matrix):
    dy_func = {}          # 动态规划方程
    dy_func_node = {}     # 存储最优顺序
    nodeNum = len(Nodes)
    org = 1

    # cycle stage: V, V-1, ..., 2
    for stage_ID in range(nodeNum, 1, -1):
        print('stage :', stage_ID)

        for i in range( 2, nodeNum + 1 ):
            current_node = i
            left_node_list = copy.deepcopy(Nodes)
            if (org in left_node_list):
                left_node_list.remove(org)
            left_node_set = set(left_node_list)

            #obtain all the subset of left node set
            subset_all = list(map(set, itertools.combinations(left_node_set, nodeNum - stage_ID)) )
            subset_all_copy = copy.deepcopy(subset_all)

            # 当处在最后一个阶段时
            if(stage_ID == nodeNum):
                key = (current_node, 'None')
                dy_func[key] = dis_matrix[i-1][org-1]
                dy_func_node[key] = 'None'

            # 当不处在最后一个阶段时
            else:
                min_distance = 1000000
                for temp_set in subset_all:      # 删除subset中包含当前节点的项
                    if(current_node in temp_set):
                        subset_all_copy.remove(temp_set)

                for sub_set in subset_all_copy:
                    sub_set = list(sub_set)
                    sub_set.sort()
                    key = (current_node, str(sub_set))

                    if(len(sub_set) == 1):       # 当sub_set只有一个元素时
                        last_node = sub_set.pop()
                        dy_func[key] = dis_matrix[i-1][last_node-1] + dy_func[(last_node, 'None')]
                        dy_func_node[key] = (last_node, 'None')
                    else:                        # 当sub_set有多个元素时
                        find_min = set()
                        find_min_node = {}                      
                        for next_node in sub_set:
                            subset_copy = copy.deepcopy(sub_set)
                            subset_copy.remove(next_node)
                            subset_copy = list(subset_copy)
                            subset_copy.sort()
                            find_min.add( dis_matrix[i-1][next_node-1] + dy_func[(next_node, str(subset_copy))] )
                            find_min_node[ dis_matrix[i-1][next_node-1] + dy_func[(next_node, str(subset_copy))] ] = (next_node, str(subset_copy))
                        dy_func[key] = min(find_min)
                        dy_func_node[key] = find_min_node[dy_func[key]]


    # stage 1
    stage_ID = current_node = i = 1
    print('stage :', stage_ID)
    left_node_list = copy.deepcopy(Nodes)
    if (org in left_node_list):
        left_node_list.remove(org)
    left_node_set = set(left_node_list)

    subset_all = list(map(set, itertools.combinations(left_node_set, nodeNum - stage_ID)) )
    subset_all_copy = copy.deepcopy(subset_all)

    min_distance = 1000000
    for temp_set in subset_all:
        if(current_node in temp_set):
            subset_all_copy.remove(temp_set)

    for sub_set in subset_all_copy:
        sub_set = list(sub_set)
        sub_set.sort()
        key = (current_node, str(sub_set))
        find_min = set()                        
        for next_node in sub_set:
            subset_copy = copy.deepcopy(sub_set)
            subset_copy.remove(next_node)
            subset_copy = list(subset_copy)
            subset_copy.sort()
            find_min.add( dis_matrix[i-1][next_node-1] + dy_func[(next_node, str(subset_copy))] )
            find_min_node[ dis_matrix[i-1][next_node-1] + dy_func[(next_node, str(subset_copy))] ] = (next_node, str(subset_copy))
        opt_dis = dy_func[key] = min(find_min)
        dy_func_node[key] = find_min_node[dy_func[key]]
        
    # extract optimal solution

    opt_route = [1]

    for key in dy_func_node.keys():
        if(key[0] == 1):
            next_key = dy_func_node[key]

    opt_route.append(next_key[0])
    for i in range(nodeNum-2):
        for key in dy_func_node.keys():
            if(key == next_key):
                next_key = dy_func_node[key]
                opt_route.append(next_key[0])
                break
    opt_route.append(1)
    
    return opt_dis, opt_route


# call DP function to solve TSP
opt_dis, opt_route = TSP_Dynamic_Programming(Nodes, dis_matrix)
print('\n-------------- optimal solution --------------\n')
print('objevtive:', opt_dis)
print('optimal rounte:', opt_route)
