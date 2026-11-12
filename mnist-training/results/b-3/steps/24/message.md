Step 23 of 50: training loss 0.8718, accuracy 0.7277.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   885    11    10    20     3     7     2     0    52     1
               1     0  1016    27     0     3     0     3    15     0     0
               2     9     7   704   121    55     0    29    11    54     0
               3     3    10    46   606     0   142    33    66   113    11
               4     5    49    24     3   657     0     1    15    67   162
               5    15    19    56    68     8   506   100    46    71    26
               6    28    52     8     9    91    21   729     1    28     0
               7    18     3    30     7    30    27     0   860    12   103
               8     6    76    82     9     6     6    45    92   649    38
               9    16    50     3     2    53    12     2    89    69   665

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
23 | 0.8718 | 0.7277

At most 27 steps left. Reply with the complete build_weights() for step 24 in one Python code block.


Here are 16 training images your step 23 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 5 (top 3: 5 0.59, 3 0.25, 8 0.13)
2. true 2, predicted 8 (top 3: 8 0.56, 2 0.22, 3 0.15)
3. true 4, predicted 9 (top 3: 9 0.71, 4 0.28, 8 0.00)
4. true 9, predicted 4 (top 3: 4 0.46, 9 0.43, 8 0.07)
5. true 3, predicted 5 (top 3: 5 0.61, 3 0.33, 6 0.04)
6. true 7, predicted 9 (top 3: 9 0.37, 4 0.20, 5 0.19)
7. true 9, predicted 1 (top 3: 1 0.87, 7 0.11, 9 0.01)
8. true 2, predicted 3 (top 3: 3 0.70, 9 0.11, 2 0.06)
9. true 9, predicted 7 (top 3: 7 0.36, 8 0.22, 9 0.21)
10. true 4, predicted 9 (top 3: 9 0.61, 4 0.37, 8 0.01)
11. true 7, predicted 5 (top 3: 5 0.44, 9 0.40, 4 0.08)
12. true 6, predicted 3 (top 3: 3 0.50, 6 0.31, 8 0.09)
13. true 5, predicted 6 (top 3: 6 0.50, 5 0.33, 8 0.10)
14. true 7, predicted 2 (top 3: 2 0.71, 7 0.25, 3 0.03)
15. true 5, predicted 7 (top 3: 7 0.45, 9 0.22, 8 0.14)
16. true 9, predicted 7 (top 3: 7 0.51, 9 0.20, 5 0.12)

[image: mistakes.png]
