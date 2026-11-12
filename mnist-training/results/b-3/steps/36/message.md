Step 35 of 50: training loss 0.7829, accuracy 0.7638.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   889     6    17    30     1    12     2     0    33     1
               1     0   978    41     3     1     1     1    39     0     0
               2    11     5   702   172    33     0    20     7    40     0
               3     3     2    39   690     0   113    36    30   104    13
               4     7    23    22     6   780     1     2    16    32    94
               5     8     6    33    59     5   631    80    28    50    15
               6    25    22    17    13    61    49   766     0    14     0
               7    21     1    27    30    27    51     0   832     4    97
               8     8    36    83    17     7    15    47    88   670    38
               9    22    23     5     7    58    25     0    67    54   700

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
30 | 0.7942 | 0.7599
31 | 0.7960 | 0.7635
32 | 0.7836 | 0.7617
33 | 0.7867 | 0.7635
34 | 0.8062 | 0.7472
35 | 0.7829 | 0.7638

At most 15 steps left. Reply with the complete build_weights() for step 36 in one Python code block.


Here are 16 training images your step 35 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 7 (top 3: 7 0.62, 9 0.25, 8 0.04)
2. true 9, predicted 0 (top 3: 0 0.24, 2 0.18, 5 0.15)
3. true 0, predicted 8 (top 3: 8 0.50, 6 0.28, 0 0.21)
4. true 6, predicted 3 (top 3: 3 0.35, 2 0.21, 6 0.11)
5. true 8, predicted 1 (top 3: 1 0.72, 7 0.26, 6 0.01)
6. true 5, predicted 6 (top 3: 6 0.30, 0 0.26, 5 0.24)
7. true 9, predicted 8 (top 3: 8 0.48, 9 0.31, 2 0.05)
8. true 2, predicted 3 (top 3: 3 0.82, 5 0.08, 8 0.04)
9. true 2, predicted 8 (top 3: 8 0.56, 2 0.16, 6 0.15)
10. true 3, predicted 8 (top 3: 8 0.65, 6 0.13, 0 0.11)
11. true 5, predicted 6 (top 3: 6 0.45, 2 0.18, 5 0.15)
12. true 2, predicted 3 (top 3: 3 0.59, 4 0.20, 2 0.09)
13. true 6, predicted 4 (top 3: 4 0.90, 5 0.06, 6 0.02)
14. true 3, predicted 6 (top 3: 6 0.50, 3 0.24, 2 0.21)
15. true 5, predicted 6 (top 3: 6 0.41, 9 0.26, 4 0.14)
16. true 8, predicted 6 (top 3: 6 0.65, 8 0.34, 0 0.02)

[image: mistakes.png]
