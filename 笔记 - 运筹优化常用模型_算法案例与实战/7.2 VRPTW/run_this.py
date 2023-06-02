#!/usr/bin/env python
# coding: utf-8

# * Liu Xinglu
# * hsinglul@163.com
# * Tsinghua University

# version 3: 2022-09-28
# version 2: 2022-04-25
# version 1: 2022-03-31

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
import Model_builder
# import Branch_and_Price



""" 下面是本代码所有的其他代码  """

if __name__ == "__main__":

    """ Read the instance data. """

    file_path = 'c101.txt'
    customer_num = 40

    data = Data.Data()    
    data = data.read_data(file_name=file_path, customer_num=customer_num)
    data = data.preprocess(data)
    data = data.generateAdjMatrix(data)


    """ Build the model. """

    model_handler = Model_builder.Model_builder()


    """ Test the branch and price """

    model_handler.build_VRPTW(data)
    model_handler.VRPTW_model.optimize()
    model_handler.VRPTW_model.write('vrptw.lp')

    
    # model_handler.VRPTW_model.computeIIS()
    # model_handler.VRPTW_model.write('vrptw.ilp')

    
    # BP_solver = Branch_and_Price.Branch_and_Price(data)
    # BP_solver.Branch_and_Price_solver(model_handler, data)

    # model_handler.build_SP(data=data)
    # model_handler.SP.optimize()
    # model_handler.print_SP(data)

    # BP_handler = BP.Branch_and_Price(data=data)
    # BP_handler.copy_model(model_handler)
    # BP_handler.Column_Generation()

    # print("RMP:", model_handler.RMP.NumVars)
    # model_handler.RMP.write('RMP.lp')


    # """ Print solutions """
    # for v in model_handler.VRPTW_model.getVars():
    #     if(v.X > 0 and v.varName.split('_')[0]=='x'):            
    #         print(v.varName, ' = ',v.X)

    model_handler.print_solution(data, model_handler.VRPTW_model)






