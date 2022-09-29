
from gurobipy import *
import matplotlib.pyplot as plt

model = read("C:\\Users\\79087\\Documents\\GitHub\\Toy-Box-of-Operations-Research-Optimization\\Gurobi advanced operation\\VRPTW_r102_20_5.mps")

bstList = []
bndList = []
gapList = []

def mycallback(model, where):
    if(where == GRB.Callback.MIPSOL):
        bst = model.cbGet(GRB.Callback.MIPSOL_OBJBST)
        bnd = model.cbGet(GRB.Callback.MIPSOL_OBJBND)
        gap = abs(bst-bnd)/bst
        bstList.append(bst)
        bndList.append(bnd)
        gapList.append(gap)

model.optimize(mycallback)
for i in range(len(gapList)):
    print('当前最好解是{:.2f}，当前界是{:.2f}，gap是{:.2f}'.format(bstList[i], bndList[i], gapList[i]))

plt.figure( figsize=(5,2))
plt.plot(gapList)
