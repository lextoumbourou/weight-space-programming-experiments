Step 22 of 50: training loss 0.8874, accuracy 0.7288.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   893    12     9    26     3     7     1     0    39     1
               1     0  1017    23     0     2     0     3    19     0     0
               2    10     8   679   156    47     0    27    18    45     0
               3     3    13    28   692     0   124    20    70    69    11
               4     5    59    22     6   616     0     2    21    64   188
               5    16    21    50    87     9   517    85    54    50    26
               6    28    62     8    11    83    40   712     1    22     0
               7    16     3    24     5    25    22     0   885    10   100
               8     6    92    67    13     4     5    45   126   616    35
               9    18    51     2     3    44    13     2   107    60   661

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810
4 | 2.1250 | 0.3982
5 | 1.3466 | 0.5185
6 | 1.1621 | 0.6170
7 | 1.3141 | 0.6005
8 | 1.1417 | 0.6499
9 | 3.4269 | 0.4356
10 | 1.5914 | 0.6284
11 | 4.5635 | 0.4265
12 | 1.2658 | 0.6402
13 | 1.0549 | 0.6888
14 | 1.0054 | 0.6912
15 | 1.3050 | 0.6310
16 | 1.0132 | 0.7045
17 | 1.2671 | 0.6900
18 | 1.0565 | 0.6974
19 | 0.9941 | 0.7178
20 | 0.9956 | 0.7153
21 | 1.0361 | 0.7076
22 | 0.8874 | 0.7288

At most 28 steps left. Reply with the complete build_weights() for step 23 in one Python code block.


Here are 16 training images your step 22 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 6 (top 3: 6 0.64, 5 0.15, 8 0.12)
2. true 8, predicted 7 (top 3: 7 0.91, 2 0.04, 1 0.02)
3. true 6, predicted 4 (top 3: 4 0.52, 5 0.21, 6 0.11)
4. true 8, predicted 3 (top 3: 3 0.43, 8 0.31, 6 0.14)
5. true 6, predicted 2 (top 3: 2 0.85, 4 0.05, 5 0.04)
6. true 4, predicted 9 (top 3: 9 0.78, 4 0.18, 7 0.02)
7. true 5, predicted 6 (top 3: 6 0.92, 5 0.03, 8 0.02)
8. true 3, predicted 1 (top 3: 1 0.45, 7 0.43, 2 0.09)
9. true 7, predicted 9 (top 3: 9 0.40, 7 0.32, 4 0.15)
10. true 7, predicted 0 (top 3: 0 0.96, 4 0.02, 5 0.01)
11. true 4, predicted 9 (top 3: 9 0.75, 4 0.23, 5 0.01)
12. true 9, predicted 1 (top 3: 1 0.56, 7 0.31, 9 0.09)
13. true 5, predicted 3 (top 3: 3 0.32, 5 0.27, 7 0.20)
14. true 4, predicted 9 (top 3: 9 0.45, 4 0.27, 8 0.09)
15. true 6, predicted 4 (top 3: 4 0.34, 2 0.24, 0 0.16)
16. true 0, predicted 3 (top 3: 3 0.71, 2 0.12, 5 0.08)

[image: mistakes.png]
