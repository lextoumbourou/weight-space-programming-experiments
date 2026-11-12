Step 24 of 50: training loss 0.9191, accuracy 0.7269.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   788    11    17     0     0     3   129     1    37     5
               1     0  1002    34     8     1     4     2    11     1     1
               2    32    15   620   116    12     8    41    14   119    13
               3     6     3    20   716     0   186     0     9    84     6
               4     4    35     4     1   652     0    55     2    29   201
               5     6    15     7   120     0   477    76     8   206     0
               6    24    32     1     4    35    11   848     0    11     1
               7     7     8    22    17    35    19     0   862     8   112
               8     6    78   126    45     2    61    35    10   575    71
               9    18    19     1    10    66    38    13    30    37   729

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078
5 | 2.7367 | 0.4958
6 | 2.3875 | 0.4751
7 | 5.6237 | 0.2327
8 | 1.8055 | 0.4696
9 | 1.9854 | 0.4561
10 | 1.5771 | 0.5330
11 | 1.8457 | 0.4671
12 | 2.1344 | 0.4372
13 | 1.9350 | 0.5070
14 | 4.0279 | 0.4305
15 | 1.3307 | 0.6072
16 | 1.1902 | 0.6406
17 | 1.3253 | 0.6170
18 | 1.0953 | 0.6732
19 | 1.0859 | 0.6762
20 | 1.0582 | 0.6870
21 | 1.0690 | 0.7032
22 | 1.0120 | 0.7094
23 | 0.9694 | 0.7188
24 | 0.9191 | 0.7269

At most 26 steps left. Reply with the complete build_weights() for step 25 in one Python code block.


Here are 16 training images your step 24 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 5 (top 3: 5 0.50, 3 0.46, 8 0.04)
2. true 8, predicted 2 (top 3: 2 0.84, 1 0.11, 8 0.04)
3. true 9, predicted 0 (top 3: 0 0.99, 6 0.00, 5 0.00)
4. true 2, predicted 8 (top 3: 8 0.35, 9 0.24, 4 0.19)
5. true 2, predicted 3 (top 3: 3 0.57, 2 0.25, 9 0.14)
6. true 3, predicted 5 (top 3: 5 0.78, 3 0.17, 8 0.05)
7. true 4, predicted 9 (top 3: 9 0.55, 6 0.19, 4 0.14)
8. true 5, predicted 6 (top 3: 6 0.94, 8 0.04, 5 0.01)
9. true 5, predicted 8 (top 3: 8 0.65, 6 0.27, 2 0.05)
10. true 4, predicted 9 (top 3: 9 0.59, 4 0.34, 8 0.02)
11. true 6, predicted 0 (top 3: 0 0.99, 6 0.01, 8 0.00)
12. true 5, predicted 8 (top 3: 8 0.58, 6 0.28, 2 0.11)
13. true 2, predicted 5 (top 3: 5 0.40, 3 0.20, 8 0.16)
14. true 2, predicted 8 (top 3: 8 0.92, 2 0.03, 9 0.03)
15. true 8, predicted 7 (top 3: 7 0.90, 3 0.04, 1 0.03)
16. true 5, predicted 8 (top 3: 8 0.32, 6 0.28, 5 0.16)

[image: mistakes.png]
