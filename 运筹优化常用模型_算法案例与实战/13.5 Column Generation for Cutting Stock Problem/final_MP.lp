\ Model master_problem
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  x_1 + x_2 + x_3 + x_4 + x_5 + new_x1 + new_x2 + new_x3
Subject To
 c_1: 8 x_1 + 6 x_2 + 6 x_3 + 5 x_4 + 5 x_5 >= 46
 c_2: x_2 + x_4 + 2 x_5 + 7 new_x2 + 2 new_x3 >= 22
 c_3: x_3 + x_4 + 4 new_x1 + 3 new_x3 >= 43
Bounds
End
