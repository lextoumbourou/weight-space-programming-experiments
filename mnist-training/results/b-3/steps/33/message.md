Step 32 of 50: training loss 0.7836, accuracy 0.7617.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   888     7    16    31     1    11     2     0    34     1
               1     0   978    40     3     1     1     1    40     0     0
               2    10     5   699   176    33     0    16     8    43     0
               3     3     2    38   683     0   114    33    35   110    12
               4     6    25    20     6   769     1     1    16    40    99
               5     8     9    33    60     5   624    74    31    55    16
               6    26    24    16    14    61    52   758     0    16     0
               7    22     1    26    28    27    51     0   838     4    93
               8     8    41    78    17     7    15    38    89   678    38
               9    23    23     5     6    54    25     0    69    54   702

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

At most 18 steps left. Reply with the complete build_weights() for step 33 in one Python code block.


Here are 16 training images your step 32 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 4 (top 3: 4 0.35, 9 0.26, 8 0.16)
2. true 3, predicted 8 (top 3: 8 0.26, 3 0.23, 4 0.20)
3. true 8, predicted 3 (top 3: 3 0.48, 7 0.19, 2 0.19)
4. true 0, predicted 5 (top 3: 5 0.60, 3 0.33, 2 0.03)
5. true 1, predicted 2 (top 3: 2 0.49, 7 0.44, 1 0.05)
6. true 6, predicted 5 (top 3: 5 0.37, 6 0.24, 0 0.20)
7. true 5, predicted 8 (top 3: 8 0.44, 5 0.33, 6 0.13)
8. true 3, predicted 7 (top 3: 7 0.43, 3 0.18, 9 0.12)
9. true 3, predicted 8 (top 3: 8 0.88, 6 0.05, 5 0.03)
10. true 7, predicted 5 (top 3: 5 0.44, 9 0.37, 4 0.10)
11. true 9, predicted 2 (top 3: 2 0.32, 5 0.23, 9 0.14)
12. true 7, predicted 5 (top 3: 5 0.43, 8 0.14, 9 0.11)
13. true 5, predicted 7 (top 3: 7 0.31, 9 0.29, 5 0.24)
14. true 7, predicted 9 (top 3: 9 0.58, 7 0.21, 5 0.13)
15. true 4, predicted 7 (top 3: 7 0.78, 2 0.07, 1 0.06)
16. true 1, predicted 7 (top 3: 7 0.49, 2 0.40, 3 0.09)

[image: mistakes.png]
