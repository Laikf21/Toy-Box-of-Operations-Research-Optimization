#!/usr/bin/env python
# coding: utf-8

# * Liu Xinglu
# * hsinglul@163.com
# * Tsinghua University
# * 2022-04-02

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

"""
Read instance data
"""
class Data(object):
    def __init__(self):
        self.customer_num = 0
        self.node_num = 0
        self.vehicle_num = 0
        self.coor_X = {}
        self.coor_Y = {}
        self.demand = {}
        self.service_time = {}
        self.ready_time = {}
        self.due_time = {}
        self.dis_matrix = {}
        self.capacity = 0
        self.arcs = {}

    def read_data(self, file_name, customer_num):
        """
        This function is to read instance data from the txt file.

        :param file_name: the txt file to be read.
        :param customer_num: problem size. make it controllable,
        :return: a instance data instance.
        """
        data = Data()

        file_name = os.getcwd().replace('\\', '/') + '/' + file_name

        data.customer_num = customer_num
        data.node_num = customer_num + 2

        # read the instance file
        f = open(file_name, 'r')
        lines = f.readlines()
        cnt = 0
        for line in lines:
            cnt += 1
            if(cnt == 5):
                line = line[:-1].strip()          # '  5                200\n'
                str_arr = re.split(r" +", line)   # ['5', '200']
                data.vehicle_num = (int)(str_arr[0])
                data.capacity = (int)(str_arr[1])

            elif(cnt >= 10 and cnt <= 10 + customer_num):
                #    ' 0      40         50          0          0       1236          0\n'
                line = line[:-1].strip()
                str_arr = re.split(r" +", line)   # ['0'     '40'         '50'          '0'          '0'       '1236'          '0']
                node_ID = (int)(str_arr[0])
                data.coor_X[node_ID] = (int)(str_arr[1])
                data.coor_Y[node_ID] = (int)(str_arr[2])
                data.demand[node_ID] = (int)(str_arr[3])
                data.ready_time[node_ID] = (int)(str_arr[4])
                data.due_time[node_ID] = (int)(str_arr[5])
                data.service_time[node_ID] = (int)(str_arr[6])

        """ add a virtual depot node for the convenience of modelling """
        data.coor_X[customer_num+1] = data.coor_X[0]
        data.coor_Y[customer_num+1] = data.coor_Y[0]
        data.demand[customer_num+1] = data.demand[0]
        data.ready_time[customer_num+1] = data.ready_time[0]
        data.due_time[customer_num+1] = data.due_time[0]
        data.service_time[customer_num+1] = data.service_time[0]

        """ compute the distance matrix of the customers """
        for i in range(data.node_num):
            for j in range(data.node_num):
                temp = (data.coor_X[i] - data.coor_X[j])**2 + (data.coor_Y[i] - data.coor_Y[j])**2
                data.dis_matrix[i, j] = round(math.sqrt(temp), 1)
                # print(data.dis_matrix[i, j])

                data.arcs[i, j] = 1 # 对于所有arc成立

        return data

    def generateAdjMatrix(self, data):
        """ compute the distance matrix of the customers """
        for i in range(data.node_num):
            for j in range(data.node_num):
                # print(data.dis_matrix[i, j])

                if(i != j):
                    data.arcs[i, j] = 1
                else:
                    data.arcs[i, j] = 0

                # data.arcs[i, j] = 1 # 对于所有arc成立

        # 下面这两种弧也一定要删掉，不删会有问题
        for i in range(data.node_num):
            data.arcs[data.node_num - 1, i] = 0   # 从虚拟终点到达起点的，删去
            data.arcs[i, 0] = 0                   # 从中间点回到0的，删去
        
        return data


    def print_data(self, data):
        """
        This function is to print the instance info.
        :param data: a data instance.
        :return:
        """
        print('-------  Instance Info --------')
        print('vehicle number: {}'.format(data.vehicle_num))
        print('customer number: {}'.format(data.customer_num))
        print('node number: {}'.format(data.node_num))
        for i in data.demand.keys():
            print('{}\t\t{}\t\t{}\t\t{}'.format(data.demand[i], data.ready_time[i],data.due_time[i], data.service_time[i]))

        print('-------  distance matrix --------')
        for i in range(data.node_num):
            for j in range(data.node_num):
                print("%6.2f" % (data.dis_matrix[i, j]), end = '')
            print()

    def preprocess(self, data):
        # preprocessing for ARCS
        # 除去不符合时间窗和容量约束的边
        for i in range(data.node_num):
            for j in range(data.node_num):
                if(i == j):
                    # data.arcs[i, j] = 0
                    pass
                elif(data.ready_time[i] + data.service_time[i] + data.dis_matrix[i, j] > data.due_time[j]
                  or data.demand[i] + data.demand[j] > data.capacity):
                    data.arcs[i, j] = 0
                elif(data.ready_time[0] + data.service_time[i] + data.dis_matrix[0, i] + data.dis_matrix[i, data.node_num-1] > data.due_time[data.node_num-1]):
                    print("the calculating example is false")

        # for i in range(data.node_num):
        #     data.arcs[data.node_num - 1, i] = 0
        #     data.arcs[i, 0] = 0
        
        return data

    def create_file_dir(self, dir):
        """
        This function is to create dirs if the dirs is not exist.

        :param dir:
        :return:None.
        """
        import os
        # 因为os.getcwd()是得到当前工作目录，但是字符串中有 'G:\\03【科研】\\【OR_Group培训】\\【MIP培训】\\【测试代码 】\\Lecture_03_VRPTW_and_Branch_and_Bound'
        # 但是我们需要的格式是 path = "E:/bp" 这样的
        current_file_dir = os.getcwd().replace('\\', '/')

        # 为了处理多级目录
        dir_arr = dir.split('/')
        for single_dir in dir_arr:
            current_file_dir += '/' + single_dir

            # 创建工作目录
            if not os.path.exists(current_file_dir):
                os.mkdir(current_file_dir)