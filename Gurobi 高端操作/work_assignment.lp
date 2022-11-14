\ Model Work_Assignment
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize multi-objectives
  TotalSlack: Priority=0 Weight=1 AbsTol=1e-06 RelTol=0
   totSlack
  Fairness: Priority=0 Weight=0.02 AbsTol=1e-06 RelTol=0
   - minShift + maxShift
Subject To
 R0: x_0_0 + x_1_0 + x_2_0 + x_3_0 + x_4_0 + x_5_0 + Slack = 2
 R1: x_0_1 + x_1_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + Slack = 3
 R2: x_0_2 + x_1_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + Slack = 4
 R3: x_0_3 + x_1_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + Slack = 5
 R4: x_0_4 + x_1_4 + x_2_4 + x_3_4 + x_4_4 + x_5_4 + Slack = 4
 R5: x_0_5 + x_1_5 + x_2_5 + x_3_5 + x_4_5 + x_5_5 + Slack = 3
 R6: x_0_6 + x_1_6 + x_2_6 + x_3_6 + x_4_6 + x_5_6 + Slack = 5
 R7: x_0_7 + x_1_7 + x_2_7 + x_3_7 + x_4_7 + x_5_7 + Slack = 2
 R8: x_0_8 + x_1_8 + x_2_8 + x_3_8 + x_4_8 + x_5_8 + Slack = 5
 R9: x_0_9 + x_1_9 + x_2_9 + x_3_9 + x_4_9 + x_5_9 + Slack = 3
 total__Slack: - Slack - Slack - Slack - Slack - Slack - Slack - Slack
   - Slack - Slack - Slack + totSlack = 0
 total_Shifts_0: - x_0_0 - x_0_1 - x_0_2 - x_0_3 - x_0_4 - x_0_5 - x_0_6
   - x_0_7 - x_0_8 - x_0_9 + totShifts_0 = 0
 total_Shifts_1: - x_1_0 - x_1_1 - x_1_2 - x_1_3 - x_1_4 - x_1_5 - x_1_6
   - x_1_7 - x_1_8 - x_1_9 + totShifts_1 = 0
 total_Shifts_2: - x_2_0 - x_2_1 - x_2_2 - x_2_3 - x_2_4 - x_2_5 - x_2_6
   - x_2_7 - x_2_8 - x_2_9 + totShifts_2 = 0
 total_Shifts_3: - x_3_0 - x_3_1 - x_3_2 - x_3_3 - x_3_4 - x_3_5 - x_3_6
   - x_3_7 - x_3_8 - x_3_9 + totShifts_3 = 0
 total_Shifts_4: - x_4_0 - x_4_1 - x_4_2 - x_4_3 - x_4_4 - x_4_5 - x_4_6
   - x_4_7 - x_4_8 - x_4_9 + totShifts_4 = 0
 total_Shifts_5: - x_5_0 - x_5_1 - x_5_2 - x_5_3 - x_5_4 - x_5_5 - x_5_6
   - x_5_7 - x_5_8 - x_5_9 + totShifts_5 = 0
Bounds
 x_0_2 = 0
 x_0_5 = 0
 x_0_8 = 0
 x_1_0 = 0
 x_1_1 = 0
 x_1_5 = 0
 x_2_0 = 0
 x_2_3 = 0
 x_2_6 = 0
 x_3_1 = 0
 x_3_5 = 0
 x_3_9 = 0
 x_4_3 = 0
 x_4_4 = 0
 x_4_6 = 0
 x_4_9 = 0
 x_5_0 = 0
 x_5_4 = 0
 x_5_7 = 0
Binaries
 x_0_0 x_0_1 x_0_2 x_0_3 x_0_4 x_0_5 x_0_6 x_0_7 x_0_8 x_0_9 x_1_0 x_1_1
 x_1_2 x_1_3 x_1_4 x_1_5 x_1_6 x_1_7 x_1_8 x_1_9 x_2_0 x_2_1 x_2_2 x_2_3
 x_2_4 x_2_5 x_2_6 x_2_7 x_2_8 x_2_9 x_3_0 x_3_1 x_3_2 x_3_3 x_3_4 x_3_5
 x_3_6 x_3_7 x_3_8 x_3_9 x_4_0 x_4_1 x_4_2 x_4_3 x_4_4 x_4_5 x_4_6 x_4_7
 x_4_8 x_4_9 x_5_0 x_5_1 x_5_2 x_5_3 x_5_4 x_5_5 x_5_6 x_5_7 x_5_8 x_5_9
General Constraints
 minShift: minShift = MIN ( totShifts_0 , totShifts_1 , totShifts_2 ,
   totShifts_3 , totShifts_4 , totShifts_5 )
 maxShift: maxShift = MAX ( totShifts_0 , totShifts_1 , totShifts_2 ,
   totShifts_3 , totShifts_4 , totShifts_5 )
End
