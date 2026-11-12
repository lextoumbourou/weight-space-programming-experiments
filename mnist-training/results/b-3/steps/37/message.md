Step 36 of 50: training loss 0.7809, accuracy 0.7660.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   888     6    35    22     1    12     5     0    20     2
               1     0   942    47     0     1     0     0    74     0     0
               2    15     5   731   132    44     0    11    10    40     2
               3     4     1    57   674     4   104    30    36   106    14
               4     8    20    22     2   798     0     2    17    16    98
               5    13     6    38    53     8   616    89    35    39    18
               6    37    22    24     8    72    33   759     4     8     0
               7    25     1    27    20    32    38     0   858     0    89
               8    16    33    80    13     8    12    42    98   660    47
               9    25    15     5     7    53    21     1    72    28   734

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
36 | 0.7809 | 0.7660

At most 14 steps left. Reply with the complete build_weights() for step 37 in one Python code block.


Here are 16 training images your step 36 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 1, predicted 7 (top 3: 7 0.44, 2 0.34, 1 0.21)
2. true 5, predicted 6 (top 3: 6 0.64, 8 0.18, 0 0.16)
3. true 8, predicted 4 (top 3: 4 0.54, 3 0.36, 9 0.04)
4. true 7, predicted 2 (top 3: 2 0.50, 3 0.18, 8 0.11)
5. true 2, predicted 3 (top 3: 3 0.68, 9 0.13, 5 0.06)
6. true 9, predicted 4 (top 3: 4 0.37, 9 0.34, 7 0.10)
7. true 3, predicted 7 (top 3: 7 0.80, 3 0.12, 2 0.03)
8. true 4, predicted 7 (top 3: 7 0.52, 1 0.14, 4 0.12)
9. true 3, predicted 5 (top 3: 5 0.51, 3 0.28, 8 0.13)
10. true 4, predicted 2 (top 3: 2 0.36, 4 0.28, 3 0.12)
11. true 0, predicted 5 (top 3: 5 0.44, 2 0.21, 0 0.19)
12. true 8, predicted 2 (top 3: 2 0.39, 7 0.30, 8 0.14)
13. true 2, predicted 8 (top 3: 8 0.53, 2 0.25, 3 0.06)
14. true 3, predicted 8 (top 3: 8 0.50, 3 0.29, 5 0.14)
15. true 3, predicted 5 (top 3: 5 0.91, 3 0.05, 8 0.02)
16. true 5, predicted 6 (top 3: 6 0.46, 8 0.23, 2 0.10)

[image: mistakes.png]
