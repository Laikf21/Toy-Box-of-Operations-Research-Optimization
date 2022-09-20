\ Model Nori&Leets_Problem
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  8 x_1 + 10 x_2 + 7 x_3 + 6 x_4 + 11 x_5 + 9 x_6 + x_7
Subject To
 Constraint_1: 12 x_1 + 9 x_2 + 25 x_3 + 20 x_4 + 17 x_5 + 13 x_6 + x_7
   >= 60
 Constraint_2: 35 x_1 + 42 x_2 + 18 x_3 + 31 x_4 + 56 x_5 + 49 x_6 + x_7
   >= 150
 Constraint_3: 37 x_1 + 53 x_2 + 28 x_3 + 24 x_4 + 29 x_5 + 20 x_6 + x_7
   >= 125
Bounds
 x_1 <= 1
 x_2 <= 1
 x_3 <= 1
 x_4 <= 1
 x_5 <= 1
 x_6 <= 1
End
