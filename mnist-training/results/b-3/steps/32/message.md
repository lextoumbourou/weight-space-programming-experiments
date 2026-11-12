Step 31 of 50: training loss 0.7960, accuracy 0.7635.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   896     7    26    28     1    12     1     0    19     1
               1     0   959    37     2     1     1     0    64     0     0
               2    12     5   723   165    35     0    13     8    29     0
               3     3     1    51   703     1   112    26    40    84     9
               4     8    25    27     7   781     0     2    21    17    95
               5    12     7    37    66     5   632    72    36    35    13
               6    34    25    25    13    66    58   735     2     9     0
               7    23     1    25    30    26    44     0   869     0    72
               8    13    34    98    18     7    17    43   105   633    41
               9    23    17     7     7    56    29     0    86    32   704

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

At most 19 steps left. Reply with the complete build_weights() for step 32 in one Python code block.


Here are 16 training images your step 31 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 7 (top 3: 7 0.40, 8 0.18, 1 0.18)
2. true 3, predicted 5 (top 3: 5 0.63, 3 0.28, 0 0.04)
3. true 3, predicted 7 (top 3: 7 0.26, 3 0.24, 1 0.22)
4. true 8, predicted 2 (top 3: 2 0.30, 0 0.19, 7 0.17)
5. true 8, predicted 2 (top 3: 2 0.39, 8 0.39, 0 0.07)
6. true 5, predicted 6 (top 3: 6 0.38, 4 0.35, 5 0.13)
7. true 8, predicted 2 (top 3: 2 0.64, 8 0.18, 3 0.06)
8. true 2, predicted 3 (top 3: 3 0.40, 8 0.31, 6 0.13)
9. true 4, predicted 9 (top 3: 9 0.60, 4 0.35, 5 0.03)
10. true 7, predicted 4 (top 3: 4 0.70, 5 0.15, 9 0.14)
11. true 5, predicted 6 (top 3: 6 0.50, 5 0.44, 8 0.03)
12. true 8, predicted 9 (top 3: 9 0.40, 8 0.25, 4 0.16)
13. true 9, predicted 5 (top 3: 5 0.63, 9 0.16, 3 0.08)
14. true 7, predicted 5 (top 3: 5 0.61, 9 0.28, 4 0.03)
15. true 6, predicted 4 (top 3: 4 0.23, 2 0.21, 3 0.21)
16. true 8, predicted 2 (top 3: 2 0.31, 5 0.23, 8 0.15)

[image: mistakes.png]
