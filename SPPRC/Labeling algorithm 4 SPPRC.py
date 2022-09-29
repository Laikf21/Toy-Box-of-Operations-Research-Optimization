import networkx as nx
import numpy as np
import pandas as pd
import math
import re
import os

# 更改工作路径至当前路径
os.chdir('C:/Users/79087/Documents/GitHub/Toy-Box-of-Operations-Research-Optimization/SPPRC')


# 创建数据存储对象
class Data():
    customerNum = 0
    nodeNum     = 0
    vehicleNum  = 0
    capacity    = 0
    cor_X       = []
    cor_Y       = []
    demand      = []
    readyTime   = []
    dueTime     = []
    serviceTime = []
    disMatrix   = []

# 数据读取函数
def readData(data, path, customerNum):
    data.customerNum = customerNum
    data.nodeNum = customerNum + 2

    count = 0
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        count += 1
        if(count == 5):
            line = line[:-1].strip()
            stri = re.split(r' +', line)
            data.vehicleNum = int(stri[0])
            data.capacity = int(stri[1])
        elif(count >= 10 and count <= 10 + customerNum):
            line = line[:-1].strip()
            stri = re.split(r' +', line)
            data.cor_X.append(float(stri[1]))
            data.cor_Y.append(float(stri[2]))
            data.demand.append(float(stri[3]))
            data.readyTime.append(float(stri[4]))
            data.dueTime.append(float(stri[5]))
            data.serviceTime.append(float(stri[6]))
    
    # 将初始点作为终点
    data.cor_X.append(data.cor_X[0])
    data.cor_Y.append(data.cor_Y[0])
    data.demand.append(data.demand[0])
    data.readyTime.append(data.readyTime[0])
    data.dueTime.append(data.dueTime[0])
    data.serviceTime.append(data.serviceTime[0])

    data.disMatrix = [[[0] for i in range(data.nodeNum)] for j in range(data.nodeNum)]
    for i in range(data.nodeNum):
        for j in range(data.nodeNum):
            temp =  (data.cor_X[i] - data.cor_X[j])**2 + ( data.cor_Y[i]-data.cor_Y[j])**2
            data.disMatrix[i][j] = math.sqrt(temp)
            temp = 0

    return data

# 数据打印函数
def printData(data, customerNum):
    print('\n---------基本信息---------')
    print('Vehicle number is {:>6d}' .format(data.vehicleNum))
    print('Vehicle capacity is {:>4d}' .format(data.capacity))
    for i in range(customerNum):
        print('{:>4.1f}, {:5.1f}, {:>6.1f}, {:>4.1f}'.format(data.demand[i], data.readyTime[i], data.dueTime[i], data.serviceTime[i]))
    
    print('\n---------距离矩阵---------')
    for i in range(data.nodeNum):
        for j in range(data.nodeNum):
            print('{:>3.1f}'.format(data.disMatrix[i][j]), end = "")
        print()

if __name__ == '__main__':

    data = Data()
    path = 'c101.txt'
    customerNum = 100
    data = readData(data, path, customerNum)

    printData(data, customerNum)
