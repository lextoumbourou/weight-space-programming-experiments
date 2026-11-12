Step 33 of 50: training loss 0.7867, accuracy 0.7635.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   889     6    17    30     1    12     2     0    33     1
               1     0   978    41     3     1     1     1    39     0     0
               2    11     5   705   169    34     0    19     7    40     0
               3     3     2    40   684     0   118    35    30   105    13
               4     7    24    22     6   779     1     2    16    32    94
               5     8     6    33    58     5   633    77    28    52    15
               6    25    22    17    13    61    50   765     0    14     0
               7    22     1    27    29    27    51     0   832     4    97
               8     8    40    84    16     7    15    46    85   670    38
               9    23    23     5     6    58    25     0    67    54   700

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

At most 17 steps left. Reply with the complete build_weights() for step 34 in one Python code block.


Here are 16 training images your step 33 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 4 (top 3: 4 0.40, 6 0.39, 3 0.11)
2. true 9, predicted 4 (top 3: 4 0.33, 9 0.23, 7 0.18)
3. true 2, predicted 0 (top 3: 0 0.33, 8 0.33, 2 0.30)
4. true 2, predicted 0 (top 3: 0 0.40, 8 0.29, 2 0.15)
5. true 8, predicted 6 (top 3: 6 0.96, 8 0.03, 4 0.01)
6. true 2, predicted 4 (top 3: 4 0.52, 8 0.38, 6 0.03)
7. true 6, predicted 3 (top 3: 3 0.71, 6 0.15, 2 0.09)
8. true 3, predicted 5 (top 3: 5 0.59, 8 0.29, 0 0.04)
9. true 3, predicted 2 (top 3: 2 0.38, 7 0.27, 3 0.26)
10. true 5, predicted 2 (top 3: 2 0.40, 8 0.25, 5 0.16)
11. true 8, predicted 2 (top 3: 2 0.60, 8 0.26, 0 0.07)
12. true 1, predicted 3 (top 3: 3 0.45, 6 0.24, 2 0.24)
13. true 3, predicted 7 (top 3: 7 0.27, 4 0.20, 6 0.16)
14. true 3, predicted 5 (top 3: 5 0.91, 3 0.04, 8 0.02)
15. true 3, predicted 8 (top 3: 8 0.51, 3 0.25, 5 0.22)
16. true 9, predicted 8 (top 3: 8 0.59, 5 0.17, 9 0.08)

[image: mistakes.png]
