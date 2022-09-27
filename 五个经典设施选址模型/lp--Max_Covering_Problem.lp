\ Model Maximum Covering Model
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  4 Serve[0] + 5 Serve[1] + 3 Serve[3] + 3 Serve[4] + 3 Serve[5] + Serve[6]
   + 3 Serve[7] + 5 Serve[8] + 2 Serve[9]
Subject To
 Cover_before_serve[0]: Select[1] + Select[7] + Select[9] - Serve[0] >= 0
 Cover_before_serve[1]: Select[0] + Select[3] + Select[4] + Select[5]
   + Select[6] + Select[8] - Serve[1] >= 0
 Cover_before_serve[2]: Select[0] + Select[2] + Select[3] + Select[5]
   + Select[6] + Select[9] - Serve[2] >= 0
 Cover_before_serve[3]: Select[1] + Select[2] + Select[3] + Select[4]
   + Select[5] + Select[7] + Select[9] - Serve[3] >= 0
 Cover_before_serve[4]: Select[0] + Select[1] + Select[2] + Select[4]
   + Select[7] + Select[8] - Serve[4] >= 0
 Cover_before_serve[5]: Select[0] + Select[2] + Select[8] + Select[9]
   - Serve[5] >= 0
 Cover_before_serve[6]: Select[3] + Select[4] + Select[6] + Select[9]
   - Serve[6] >= 0
 Cover_before_serve[7]: Select[1] + Select[2] + Select[3] + Select[4]
   + Select[5] + Select[6] + Select[8] + Select[9] - Serve[7] >= 0
 Cover_before_serve[8]: Select[2] + Select[5] + Select[6] + Select[8]
   - Serve[8] >= 0
 Cover_before_serve[9]: Select[1] + Select[5] + Select[6] + Select[8]
   - Serve[9] >= 0
 Num_limit: Select[0] + Select[1] + Select[2] + Select[3] + Select[4]
   + Select[5] + Select[6] + Select[7] + Select[8] + Select[9] = 5
Bounds
Binaries
 Select[0] Select[1] Select[2] Select[3] Select[4] Select[5] Select[6]
 Select[7] Select[8] Select[9] Serve[0] Serve[1] Serve[2] Serve[3] Serve[4]
 Serve[5] Serve[6] Serve[7] Serve[8] Serve[9]
End
