'''
max z = 2*x1 + 3*x2
          x1 + 2*x2 + x3           == 8
        4*x1 +           + x4      == 26
               4*x2           + x5 == 12
x1, x2, x3, x4, x5 >= 0
'''

import numpy as np
import pandas as pd
import copy

# 模型的参数部分
Basic = [2, 3, 4]
Nonbasic = [0, 1]
c = np.array([2,3,0,0,0]).astype(float)
c_B = np.array([0,0,0]).astype(float)
c_N = np.array([2,3]).astype(float)
A = np.array([[1,2,1,0,0],
              [4,0,0,1,0],
              [0,4,0,0,1]]).astype(float)
A_N = np.array([[1,2],
                [4,0],
                [0,4]]).astype(float)
b = np.array([8,16,12]).astype(float)
B_inv = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]]).astype(float)

x_opt = np.array([0,0,0,0,0]).astype(float)
z_opt = 0

solutionStatus = None
row_num = len(A)
column_num = len(A[0])

reducedCost = c_N - np.dot(np.dot(c_B, B_inv), A_N)

max_sigma = max(reducedCost)

eps = 0.001

# 进行单纯形法的迭代
iterNum = 1
while(max_sigma >= eps):
    # 识别unbounded
    '''
    pass
    '''

    # 确定入基变量
    enter_var_index = Nonbasic[np.argmax(reducedCost)]
    print(f'入基变量的下标为：{enter_var_index}')

    # 确定出基变量
    min_ratio = 100000
    leave_var_index = 0 
    for i in range(row_num):        
        print(f'b: {b[i]}', f'\t A: {A[i][enter_var_index]}', f'\t ratio: {b[i]/A[i][enter_var_index]}')
        if A[i][enter_var_index] == 0:
            # print('模型不可行')
            # solutionStatus = 'infeasible'
            continue
        elif (b[i]/A[i][enter_var_index] < min_ratio) and (b[i]/A[i][enter_var_index] > 0):
            
            min_ratio = b[i]/A[i][enter_var_index]
            leave_var_index = i

    # 处理入基变量与出基变量
    leave_var = Basic[leave_var_index]
    Basic[leave_var_index] = enter_var_index
    Nonbasic.remove(enter_var_index)
    Nonbasic.append(leave_var)
    Nonbasic.sort()

    # 高斯消元
    # 更新pivot row
    pivot_number = A[leave_var_index][enter_var_index]
    for col in range(column_num):
        A[leave_var_index][col] = A[leave_var_index][col]/pivot_number
    b[leave_var_index] = b[leave_var_index] /pivot_number 
    # 更新其他row
    for row in range(row_num):
        if row != leave_var_index:
            factor = -A[row][enter_var_index]/1.0
            for col in range(column_num):
                A[row][col] = A[row][col] + factor * A[leave_var_index][col]
            b[row] = b[row] + factor * b[leave_var_index]
    
    # 更新c_N, c_B, A_N and B_inv
    for i in range(len(Nonbasic)):
        var_index = Nonbasic[i]
        c_N[i] = c[var_index]
    for i in range(len(Basic)):
        var_index  = Basic[i]
        c_B[i] = c[var_index]
    for i in range(row_num):
        for j in range(len(Nonbasic)):
            var_index = Nonbasic[j]
            A_N[i][j] = A[i][var_index]
    for i in range(len(Basic)):
        col = Basic[i]
        for row in range(row_num):
            B_inv[row][i] = A[row][col]

    # 更新reduced cost
    reducedCost = c_N - np.dot(np.dot(c_B, B_inv), A_N)
    max_sigma = max(reducedCost)
    iterNum += 1

# 检查解的状态
for i in range(len(reducedCost)):
    if(reducedCost[i] == 0):
        solutionStatus = 'Alternative optimal solutions'
        break
    else:
        solutionStatus = 'Optimal'

# get the solution
x_basic = np.dot(B_inv, b)
x_opt = np.array([0.0] * column_num).astype(float)
for i in range(len(Basic)):
    basic_var_index = Basic[i]
    x_opt[basic_var_index] = x_basic[i]
z_opt = np.dot(np.dot(c_B, B_inv), b)

print('Simplex iteration:', iterNum)
print('objective:', z_opt)
print('optimal solution', x_opt)


            