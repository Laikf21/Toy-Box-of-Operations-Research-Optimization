
# 旅行商问题（TSP）的建模方法
旅行商问题是著名的NP-hard问题，具体描述如下：给定一个有向图 $G=(V,E)$，其中V是总数为N的节点集合 $|V|=N$，E是边的集合，TSP的目标是找到一条从某个起点出发，一次不重复地经过所有其他节点，最终返回起点的最短路。

TSP问题建模需要考虑因素包括：
- 决策变量：边(i, j)在最优解中是否被选中
- 目标函数：最小化总成本
- 约束1：每个点被到达且仅被到达一次
- 约束2：每个点离开且只被离开一次

初步模型如下:
$$
\min  \sum_i{\sum_j{\begin{array}{c}
	c_{ij}x_{ij}\\
\end{array}}}
\\
\sum_{i\in V}{\begin{array}{c}
	x_{ij}=1\\
\end{array}}
\\
\sum_{j\in V}{x_{ij}=1}
\\
x_{ij}\in \left\{ 0,1 \right\} 
$$

由于该模型的不完备，容易导致子环路的出现。子环路是指没有包含所有节点V的一条闭环。一般采用 **subtour-elimination** 或 **Miller-Tucker-Zemlin (MTZ)** 方法消除上述模型会出现的子环路

<br />

## **消除子环路：Subtour-Elimination**
子环路出现意味着出现了包含点个数为 $S,(S<|V|=N)$ 的子环。因此我们可以朴素地认为，只要加入子环路删除约束，依次删除所有少于N的子环即可。
$$
\sum_{i,j\in S}{x_{ij}\le |S|-1} \qquad 2\le|S|\le n-1,\; S\subset V
$$
上述约束的数量级至多为 $2^N$，略显繁杂，一般通过求解器callback函数，以惰性更新的方式添加约束。

<br />

## **消除子环路：Miller-Tucker-Zemlin (MTZ)**
通过引入辅助决策变量 $\mu_i \; \forall i \in V, \mu_i \ge 0$，对于每条边 $(i,j) \in E$，构造 MTZ 约束。

$$ \mu_i-\mu_j+Mx_{ij} \le M-1, \quad \forall i,j \in V, \; i,j\ne 0, i\ne j $$

M是一个足够大的正数，理论上应当为 $\mu_i -\mu_j+1$ 的一个上界即可。