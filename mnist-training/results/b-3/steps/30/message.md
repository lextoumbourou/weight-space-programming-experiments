Step 29 of 50: training loss 0.8148, accuracy 0.7511.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   898     9     9    23     0    10     2     0    39     1
               1     0  1004    33     1     1     1     2    22     0     0
               2     9     5   697   182    26     0    29     6    36     0
               3     3     6    39   675     1   136    35    39    84    12
               4     6    32    22     4   754     1     2    16    56    90
               5    10    10    35    63     6   608    81    35    48    19
               6    33    30     9    12    52    58   752     0    21     0
               7    24     2    28    26    25    42     0   826     8   109
               8     6    53    98    14     7    14    50    90   646    31
               9    22    34     6     5    68    23     2    84    66   651

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
24 | 0.8428 | 0.7345
25 | 0.8313 | 0.7399
26 | 0.8296 | 0.7406
27 | 0.8180 | 0.7502
28 | 0.8325 | 0.7465
29 | 0.8148 | 0.7511

At most 21 steps left. Reply with the complete build_weights() for step 30 in one Python code block.


Here are 16 training images your step 29 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 1 (top 3: 1 0.86, 6 0.09, 7 0.01)
2. true 4, predicted 9 (top 3: 9 0.68, 4 0.30, 8 0.01)
3. true 8, predicted 9 (top 3: 9 0.39, 7 0.34, 3 0.09)
4. true 4, predicted 8 (top 3: 8 0.43, 4 0.41, 9 0.05)
5. true 3, predicted 5 (top 3: 5 0.45, 6 0.33, 8 0.13)
6. true 9, predicted 4 (top 3: 4 0.71, 9 0.13, 6 0.06)
7. true 8, predicted 6 (top 3: 6 0.96, 8 0.03, 4 0.01)
8. true 5, predicted 6 (top 3: 6 0.97, 8 0.03, 5 0.00)
9. true 7, predicted 3 (top 3: 3 0.43, 2 0.21, 5 0.16)
10. true 2, predicted 3 (top 3: 3 0.47, 2 0.42, 5 0.05)
11. true 8, predicted 7 (top 3: 7 0.60, 1 0.20, 2 0.09)
12. true 5, predicted 6 (top 3: 6 0.72, 8 0.19, 5 0.07)
13. true 2, predicted 3 (top 3: 3 0.51, 2 0.38, 6 0.08)
14. true 6, predicted 4 (top 3: 4 0.92, 5 0.03, 2 0.02)
15. true 9, predicted 8 (top 3: 8 0.43, 5 0.31, 9 0.14)
16. true 3, predicted 2 (top 3: 2 0.54, 3 0.28, 5 0.09)

[image: mistakes.png]
