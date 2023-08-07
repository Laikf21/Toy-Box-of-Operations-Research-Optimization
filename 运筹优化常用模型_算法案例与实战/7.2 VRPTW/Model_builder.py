#!/usr/bin/env python
# coding: utf-8

# * Liu Xinglu
# * hsinglul@163.com
# * Tsinghua University
# * 2022-04-25


#!/usr/bin/env python
# coding: utf-8

# * Liu Xinglu
# * hsinglul@163.com
# * Tsinghua University
# * 2022-03-31

"""
注意事项：每一次求解模型前，一定要首先更新模型的所有 bounds

加速的操作：
1. 数据的预处理
2. 不在节点存储模型
3. 通过设置bound加cut
4. branch on arc
5. 每个node只存储已经改变了的，没必要存储所有的 var_LB

"""

from gurobipy import *
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import copy
import time
import networkx as nx
import matplotlib.animation as animation   #  生成动画

import Data

"""
Build VRPTW Model and solve
"""
class Model_builder(object):
    """
    This class is to build models, including RMP and pricing problems.
    """

    def __init__(self):
        self.data = None
        self.VRPTW_model = None     # the initial VRPTW model
        self.RMP = None             # RMP model
        self.cons_RMP = {}          # constraints of RMP
        self.duals_of_RMP = {}         # duals of RMP
        self.SP = None              # Pricing model
        self.y = {}                 # decision variables in RMP
        self.x = {}                 # routing variables of SP
        self.s = {}                 # time variables of SP
        self.routes = {}            # routes in RMP, key: varName, value: route


    def build_RMP(self, data):
        """
        Build the RMP with initial columns.
        :param data:
        :return:
        """
        """ build the model object """
        self.RMP = Model('RMP')

        # data node = [0, 1, 2, 3, 4, 5, 6]
        """ for each customer, generate a feasible path """
        for customer_ID in range(1, data.customer_num + 1):
            var_name = 'y_' + str(customer_ID)
            self.routes[var_name] = [0, customer_ID, data.customer_num + 1]   # [0, 1, 6]
            obj_coef = data.dis_matrix[0, customer_ID] + data.dis_matrix[customer_ID, data.customer_num + 1]
            self.y[customer_ID] = self.RMP.addVar(lb=0, ub=1, obj=obj_coef, vtype=GRB.CONTINUOUS, name=var_name)

            """ add constraints into the RMP """
            con_name = 'cons_' + str(customer_ID)
            self.cons_RMP[customer_ID] = self.RMP.addConstr(self.y[customer_ID] == 1, name=con_name)

        self.RMP.update()

        """ initialize the dual variables """
        for key in self.cons_RMP.keys():
            self.duals_of_RMP[key] = 0
        self.duals_of_RMP[0] = 0
        self.duals_of_RMP[data.customer_num + 1] = 0

    def print_RMP(self):
        """
        Pirnt the solution of the current RMP.
        :return:
        """
        if(self.RMP.status == 2):
            print(" ---------  The solution ---------  ")
            print(" incumbent obj: {}".format(self.RMP.ObjVal))
            for var in self.RMP.getVars():
                var_name = var.varName
                if(var.x > 0.1):
                    print("{} = {}, \t | Route: {}".format(var_name, var.x, self.routes[var_name]))


    def build_SP(self, data):
        """
        Build the subproblem with the input data.
        :param data:
        :return:
        """

        """ build the model """
        self.SP = Model('SP')

        """ define the decision variables """
        for i in range(data.node_num):
            var_s_name = 's_' + str(i)
            # self.s[i] = self.SP.addVar(lb=data.ready_time[i], ub=data.due_time[i], vtype=GRB.CONTINUOUS, name=var_s_name)
            self.s[i] = self.SP.addVar(lb=0, ub=10000, vtype=GRB.CONTINUOUS, name=var_s_name)
            for j in range(data.node_num):
                if(data.arcs[i, j] == 1):
                    var_x_name = 'x_' + str(i) + '_' + str(j)
                    self.x[i, j] = self.SP.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=var_x_name)

        """ add the objective functions """
        obj = LinExpr()
        for i in range(data.node_num):
            for j in range(data.node_num):
                if(data.arcs[i, j] == 1):
                    coef = data.dis_matrix[i, j] - self.duals_of_RMP[i]
                    obj.addTerms(coef, self.x[i, j])

        self.SP.setObjective(obj, GRB.MINIMIZE)

        """" add constraints """
        lhs = LinExpr()
        for customer_ID in range(1, data.customer_num + 1):
            for j in range(data.node_num):
                if(data.arcs[customer_ID, j] == 1):
                    lhs.addTerms(data.demand[customer_ID], self.x[customer_ID, j])
        self.SP.addConstr(lhs <= data.capacity, name='capacity')

        """ start """
        lhs = LinExpr()
        for j in range(data.node_num):
            if(data.arcs[0, j] == 1):
                lhs.addTerms(1, self.x[0, j])
        self.SP.addConstr(lhs == 1, name='start')

        """ flow conservation """
        for customer_ID in range(1, data.customer_num + 1):
            lhs = LinExpr()
            for i in range(data.node_num):
                if(data.arcs[i, customer_ID] == 1):
                    lhs.addTerms(1, self.x[i, customer_ID])
            for j in range(data.node_num):
                if(data.arcs[customer_ID, j] == 1):
                    lhs.addTerms(-1, self.x[customer_ID, j])

            self.SP.addConstr(lhs == 0, name='flow_conservation_' + str(customer_ID))

        """ arrive """
        lhs = LinExpr()
        for i in range(data.node_num):
            if(data.arcs[i, data.node_num - 1] == 1):
                lhs.addTerms(1, self.x[i, data.node_num - 1])
        self.SP.addConstr(lhs == 1, name='arrive')

        """ time window constraints """
        for i in range(data.node_num):
            for j in range(data.node_num):
                if(data.arcs[i, j] == 1):
                    # big_M = data.due_time[i] + data.dis_matrix[i, j] - data.ready_time[i]
                    big_M = 5000
                    self.SP.addConstr(self.s[i] + data.dis_matrix[i, j] - self.s[j] - big_M * (1 - self.x[i, j]) <= 0,
                                      name='TW_' + str(i) + '_' + str(j))

        """ time window constraints 2 """
        for i in range(data.node_num):
            self.SP.addConstr(data.ready_time[i] <= self.s[i], name='TW_range_lb_' + str(i))
            self.SP.addConstr(self.s[i] <= data.due_time[i], name='TW_range_ub_' + str(i))

        self.SP.update()


    def print_SP(self, data):
        """
        Pirnt the solution of the current SP.
        :return:
        """

        
        if(self.SP.status == 2):
            print(" ---------  The solution of SP---------  ")
            print(" SP obj: {}".format(self.SP.ObjVal))
            for var in self.SP.getVars():
                var_name = var.varName
                if(var.x > 0.1 and var_name.startswith('x')):
                    print("{} = {}".format(var_name, var.x))

            print(" ---------  The route of current SP---------  ")
            current_node = 0
            route = [current_node]
            while(current_node != data.node_num - 1):
                for j in range(data.node_num):
                    if(data.arcs[current_node, j] == 1 and self.x[current_node, j].x > 0.1):
                        current_node = j
                        route.append(j)
            print('route: {}'.format(route))



    def build_VRPTW(self, data):
        self.VRPTW_model = Model('VRPTW')

        """ create decision variables """
        x = {}    # routing decisions: x_ijk
        s = {}    # service time decisions: s_ik
        for i in range(data.node_num):
            for k in range(data.vehicle_num):
                name = 's_' + str(i) + '_' + str(k)
                s[i, k] = self.VRPTW_model.addVar(lb=data.ready_time[i], ub=data.due_time[i], vtype=GRB.CONTINUOUS, name=name)
                for j in range(data.node_num):
                    if(data.arcs[i, j] == 1):
                        name = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                        x[i, j, k] = self.VRPTW_model.addVar(lb=0, ub=1, vtype=GRB.BINARY,
                                                     name=name)
                        
        """ set the objective function """
        obj = LinExpr()
        for i in range(data.node_num):
            for k in range(data.vehicle_num):
                for j in range(data.node_num):
                    if(data.arcs[i, j] == 1):
                        obj.addTerms(data.dis_matrix[i, j], x[i, j, k])

        self.VRPTW_model.setObjective(obj, GRB.MINIMIZE)

        """ constraints 1 : each customer must be visited exactly once """
        # 0, 1, ..., customer_num, customer_num + 1
        for i in range(1, data.node_num - 1):
            lhs = LinExpr()
            for j in range(data.node_num):
                if(data.arcs[i, j] == 1):
                    for k in range(data.vehicle_num):
                        lhs.addTerms(1, x[i, j, k])
            self.VRPTW_model.addConstr(lhs == 1, name = 'c_1' + str(i))

        """ constraints 2 : each vehicle must start from the depot """
        for k in range(data.vehicle_num):
            lhs = LinExpr()
            for j in range(1, data.node_num):
                lhs.addTerms(1, x[0, j, k])
            self.VRPTW_model.addConstr(lhs == 1, name = 'c_2' + str(k))

        """ constraints 3 : flow conservation """
        for k in range(data.vehicle_num):
            for h in range(1, data.node_num - 1): # 改成range(0, data.node_num - 1)
                lhs = LinExpr()
                rhs = LinExpr()
                for i in range(data.node_num):
                    if(data.arcs[i, h] == 1):
                        lhs.addTerms(1, x[i, h, k])

                for j in range(data.node_num):
                    if(data.arcs[h, j] == 1):
                        rhs.addTerms(1, x[h, j, k])
                self.VRPTW_model.addConstr(lhs == rhs, 'c_3' + str(k) + '_' + str(h))

        """ constraints 4 : each vehicle must return back to the depot """
        for k in range(data.vehicle_num):
            lhs = LinExpr()
            for i in range(0, data.node_num - 1):
                lhs.addTerms(1, x[i, data.node_num - 1, k])
            self.VRPTW_model.addConstr(lhs == 1, name = 'c_4' + str(k))

        """ constraints 5 : capacity constraint """
        for k in range(data.vehicle_num):
            lhs = LinExpr()
            for i in range(0, data.node_num - 1):
                for j in range(1, data.node_num):
                    if(data.arcs[i, j] == 1):
                        lhs.addTerms(data.demand[i], x[i, j, k])
            self.VRPTW_model.addConstr(lhs <= data.capacity, name = 'c_5' + str(k))

        """ constraints 6 : time window constraints """
        # constraint (6)
        big_M = 0
        for i in range(data.node_num):
            for j in range(data.node_num):
                if(data.arcs[i, j] == 1):
                    big_M = max(data.due_time[i] + data.dis_matrix[i, j] - data.ready_time[i], big_M)

                    # #设置big_M出错
                    # big_M = 100  

        # big_M = 1
        for k in range(data.vehicle_num):
            for i in range(0, data.node_num - 1):
                for j in range(1, data.node_num):
                    if(data.arcs[i, j] == 1):
                        self.VRPTW_model.addConstr(s[i, k] + data.dis_matrix[i, j] + data.service_time[i] - s[j, k] - big_M * (1 - x[i, j, k])
                                              <= 0 , name='c_6' + str(i) + '_' + str(j) + '_' + str(k))

        """ constraints 7 : each arc is visted at most once """
        for i in range(data.node_num):
            for j in range(data.node_num):
                if(data.arcs[i, j] == 1 and (i != 0 and j != data.node_num - 1) ):   # 就是不能是 0- virTual depot
                    lhs = LinExpr()
                    for k in range(data.vehicle_num):
                        lhs.addTerms(1, x[i, j, k])
                    self.VRPTW_model.addConstr(lhs <= 1, name = 'c_7_' + str(i) + '_' + str(j))

        """ constraints 8 : 破除对称性 """
        for k in range(data.vehicle_num - 1):
            lhs = LinExpr()
            for i in range(0, data.node_num - 1):
                for j in range(1, data.node_num):
                    if(data.arcs[i, j] == 1):
                        lhs.addTerms(data.demand[i], x[i, j, k])

            rhs = LinExpr()
            for i in range(0, data.node_num - 1):
                for j in range(1, data.node_num):
                    if(data.arcs[i, j] == 1):
                        rhs.addTerms(data.demand[i], x[i, j, k+1])

            self.VRPTW_model.addConstr(lhs >= rhs, name = 'c_8_' + str(k))


        """ constraints 9 : 选的边的个数 """
        lhs = LinExpr()
        for k in range(data.vehicle_num):
            for i in range(0, data.node_num - 1):
                for j in range(1, data.node_num):
                    if(data.arcs[i, j] == 1):
                        lhs.addTerms(1, x[i, j, k])
        self.VRPTW_model.addConstr(lhs <= data.vehicle_num + data.customer_num)

        return self.VRPTW_model


    def print_solution(self, data, model, file_dir='None', file_name='None'):
        """
        输出解，获或者导出到文件
        :param data:
        :param model:
        :param file_dir:
        :param file_path:
        :return:
        """
        import os

        # new_file_dir = ''
        # solution_file_name = ''
        if(file_dir != 'None'):
            data.create_file_dir(file_dir)
            #
            # # 因为os.getcwd()是得到当前工作目录，但是字符串中有 'G:\\03【科研】\\【OR_Group培训】\\【MIP培训】\\【测试代码 】\\Lecture_03_VRPTW_and_Branch_and_Bound'
            # # 但是我们需要的格式是 path = "E:/ly" 这样的
            # current_file_dir = os.getcwd().replace('\\', '/')
            # new_file_dir = current_file_dir + '/' + file_dir
            # # 创建工作目录
            # if not os.path.exists(new_file_dir):
            #     os.mkdir(new_file_dir)


        solution_file_name = os.getcwd().replace('\\', '/') + '/' + file_dir + '/' + file_name

        # model.optimize()   # 以防没有求解
        print('---------- print the solution ---------- ')
        if(model.status != 2):
            print('the model is infeasible.')
        else:
            print('The objective value: {}'.format(model.ObjVal))
            print('--------------  Routes ------------------')
            for k in range(data.vehicle_num):
                vehicle_is_used = False
                total_load = 0
                print(' Vehicle {}: '.format(k), end=' ')
                current_pos = 0
                print('[{}'.format(current_pos), end='-')
                while(current_pos != data.node_num - 1):
                    # 寻找 (current_node, j, k) == 1的变量
                    for j in range(1, data.node_num):  # 找x[current_node, j, k] = 1的下一条弧
                        if (data.arcs[current_pos, j] == 1):
                            temp_var_name = 'x_' + str(current_pos) + '_' + str(j) + '_' + str(k)
                            temp_var = model.getVarByName(temp_var_name)
                            if (temp_var.x > 0.1):  # > 0 有点太小，会有数值问题
                                current_pos = j

                                if (current_pos != data.node_num - 1):
                                    print('{}'.format(current_pos), end='-')
                                elif (current_pos == data.node_num - 1):
                                    print('{}'.format(current_pos), end='')

                                total_load += data.demand[current_pos]

                                vehicle_is_used = True
                                break

                    # 如果这辆车没触发，直接跳出循环。跳出while循环，
                    if(vehicle_is_used == False):
                        break

                print('], load : {}'.format(total_load))
                #     for i in range(current_node, data.node_num):    # 找x[current_node, j, k] = 1的下一条弧
                #         for j in range(data.node_num):
                #             if(data.arcs[i, j] == 1):
                #                 temp_var_name = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                #                 temp_var = model.getVarByName(temp_var_name)
                #                 if(temp_var.x > 0.1):   # > 0 有点太小，会有数值问题
                #                     current_node = j
                #
                #                     if(current_node != data.node_num - 1):
                #                         print('{}'.format(current_node), end='-')
                #                     elif(current_node == data.node_num - 1):
                #                         print('{}'.format(current_node), end='')
                #
                #                     total_load += data.demand[current_node]
                #                     # the go to while
                #                     node_is_updated = True
                #                     break
                #         if(node_is_updated == True):
                #             break
                # print('], load : {}'.format(total_load))

        if(file_name != 'None' and model.status == 2):
            # 我们就写入到文件
            with open(solution_file_name, 'w') as f:   # 'x' 是可以写，但是'w'是替换覆盖
                f.write('---------- print the solution ---------- \n')
                f.write('The objective value: {}\n'.format(model.ObjVal))
                f.write('--------------  Routes ------------------\n')
                for k in range(data.vehicle_num):
                    vehicle_is_used = False
                    total_load = 0
                    f.write(' Vehicle {}: '.format(k))
                    current_pos = 0
                    f.write('[{}'.format(current_pos))
                    while (current_pos != data.node_num - 1):
                        # 寻找 (current_node, j, k) == 1的变量
                        for j in range(1, data.node_num):  # 找x[current_node, j, k] = 1的下一条弧
                            if (data.arcs[current_pos, j] == 1):
                                temp_var_name = 'x_' + str(current_pos) + '_' + str(j) + '_' + str(k)
                                temp_var = model.getVarByName(temp_var_name)
                                if (temp_var.x > 0.1):  # > 0 有点太小，会有数值问题
                                    current_pos = j

                                    if (current_pos != data.node_num - 1):
                                        f.write('{}-'.format(current_pos))
                                    elif (current_pos == data.node_num - 1):
                                        f.write('{}'.format(current_pos))

                                    total_load += data.demand[current_pos]

                                    vehicle_is_used = True
                                    break

                        # 如果这辆车没触发，直接跳出循环。跳出for循环，
                        if (vehicle_is_used == False):
                            break

                    f.write('], load : {}\n'.format(total_load))


    def print_solution_of_incumbent_node(self, data, incumbent_node, file_dir='None', file_name='None'):
        """
        输出解，获或者导出到文件
        :param data:
        :param incumbent_node:
        :param file_dir:
        :param file_path:
        :return:
        """
        import os

        # new_file_dir = ''
        # solution_file_name = ''
        if(file_dir != 'None'):
            data.create_file_dir(file_dir)
            #
            # # 因为os.getcwd()是得到当前工作目录，但是字符串中有 'G:\\03【科研】\\【OR_Group培训】\\【MIP培训】\\【测试代码 】\\Lecture_03_VRPTW_and_Branch_and_Bound'
            # # 但是我们需要的格式是 path = "E:/ly" 这样的
            # current_file_dir = os.getcwd().replace('\\', '/')
            # new_file_dir = current_file_dir + '/' + file_dir
            # # 创建工作目录
            # if not os.path.exists(new_file_dir):
            #     os.mkdir(new_file_dir)


        solution_file_name = os.getcwd().replace('\\', '/') + '/' + file_dir + '/' + file_name

        # model.optimize()   # 以防没有求解
        print('---------- print the solution ---------- ')
        if(incumbent_node.model_status != 2):
            print('the model is infeasible.')
        else:
            print('The objective value: {}'.format(incumbent_node.local_UB))
            print('\n--------------  Routes ------------------\n')
            for k in range(data.vehicle_num):
                vehicle_is_used = False
                total_load = 0
                print(' Vehicle {}: '.format(k), end=' ')
                current_pos = 0
                print('[{}'.format(current_pos), end='-')
                while(current_pos != data.node_num - 1):
                    # 寻找 (current_node, j, k) == 1的变量
                    for j in range(1, data.node_num):  # 找x[current_node, j, k] = 1的下一条弧
                        if (data.arcs[current_pos, j] == 1):
                            temp_var_name = 'x_' + str(current_pos) + '_' + str(j) + '_' + str(k)
                            if (incumbent_node.x_int_sol[temp_var_name] > 0.1):  # > 0 有点太小，会有数值问题
                                current_pos = j

                                if (current_pos != data.node_num - 1):
                                    print('{}'.format(current_pos), end='-')
                                elif (current_pos == data.node_num - 1):
                                    print('{}'.format(current_pos), end='')

                                total_load += data.demand[current_pos]

                                vehicle_is_used = True
                                break

                    # 如果这辆车没触发，直接跳出循环。跳出while循环，
                    if(vehicle_is_used == False):
                        break

                print('], load : {}'.format(total_load))
        print('-------------------------------------\n\n\n')
                #     for i in range(current_node, data.node_num):    # 找x[current_node, j, k] = 1的下一条弧
                #         for j in range(data.node_num):
                #             if(data.arcs[i, j] == 1):
                #                 temp_var_name = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                #                 temp_var = model.getVarByName(temp_var_name)
                #                 if(temp_var.x > 0.1):   # > 0 有点太小，会有数值问题
                #                     current_node = j
                #
                #                     if(current_node != data.node_num - 1):
                #                         print('{}'.format(current_node), end='-')
                #                     elif(current_node == data.node_num - 1):
                #                         print('{}'.format(current_node), end='')
                #
                #                     total_load += data.demand[current_node]
                #                     # the go to while
                #                     node_is_updated = True
                #                     break
                #         if(node_is_updated == True):
                #             break
                # print('], load : {}'.format(total_load))

        if(file_name != 'None' and incumbent_node.model_status == 2):
            # 我们就写入到文件
            with open(solution_file_name, 'w') as f:   # 'x' 是可以写，但是'w'是替换覆盖
                f.write('---------- print the solution ---------- \n')
                f.write('The objective value: {}\n'.format(incumbent_node.local_UB))
                f.write('--------------  Routes ------------------\n')
                for k in range(data.vehicle_num):
                    vehicle_is_used = False
                    total_load = 0
                    f.write(' Vehicle {}: '.format(k))
                    current_pos = 0
                    f.write('[{}'.format(current_pos))
                    while (current_pos != data.node_num - 1):
                        # 寻找 (current_node, j, k) == 1的变量
                        for j in range(1, data.node_num):  # 找x[current_node, j, k] = 1的下一条弧
                            if (data.arcs[current_pos, j] == 1):
                                temp_var_name = 'x_' + str(current_pos) + '_' + str(j) + '_' + str(k)
                                if (incumbent_node.x_int_sol[temp_var_name] > 0.1):  # > 0 有点太小，会有数值问题
                                    current_pos = j

                                    if (current_pos != data.node_num - 1):
                                        f.write('{}-'.format(current_pos))
                                    elif (current_pos == data.node_num - 1):
                                        f.write('{}'.format(current_pos))

                                    total_load += data.demand[current_pos]

                                    vehicle_is_used = True
                                    break

                        # 如果这辆车没触发，直接跳出循环。跳出for循环，
                        if (vehicle_is_used == False):
                            break

                    f.write('], load : {}\n'.format(total_load))