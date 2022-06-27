# 旅行商问题（TSP）建模方法
TSP问题建模考虑因素包括：
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

该模型考虑的约束并不周全，会导致子环路的出现，一般采用 **subtour-elimination** 或 **Miller-Tucker-Zemlin (MTZ)** 方法帮助上述模型消除子环路。