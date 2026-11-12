Step 30 of 50: training loss 0.7942, accuracy 0.7599.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   903     9    17    29     0    10     2     0    20     1
               1     0   979    38     2     1     1     1    42     0     0
               2    10     5   717   174    31     0    19     8    26     0
               3     3     4    43   706     0   122    32    39    70    11
               4     6    28    28     6   774     1     2    20    19    99
               5    11     9    38    63     6   624    78    36    33    17
               6    31    27    19    13    64    56   748     0     9     0
               7    24     1    26    26    27    46     0   851     0    89
               8     9    44   126    16     7    16    50    99   598    44
               9    24    24     9     6    55    26     0    85    33   699

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

At most 20 steps left. Reply with the complete build_weights() for step 31 in one Python code block.


Here are 16 training images your step 30 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 2 (top 3: 2 0.74, 3 0.16, 8 0.05)
2. true 6, predicted 4 (top 3: 4 0.70, 6 0.15, 5 0.10)
3. true 2, predicted 1 (top 3: 1 0.65, 2 0.26, 7 0.07)
4. true 5, predicted 2 (top 3: 2 0.55, 3 0.22, 5 0.10)
5. true 5, predicted 6 (top 3: 6 0.32, 7 0.24, 5 0.22)
6. true 9, predicted 7 (top 3: 7 0.73, 1 0.24, 2 0.01)
7. true 5, predicted 3 (top 3: 3 0.30, 5 0.30, 2 0.29)
8. true 5, predicted 0 (top 3: 0 0.26, 6 0.25, 5 0.23)
9. true 4, predicted 2 (top 3: 2 0.46, 3 0.36, 4 0.09)
10. true 9, predicted 7 (top 3: 7 0.33, 9 0.30, 5 0.11)
11. true 3, predicted 5 (top 3: 5 0.59, 3 0.34, 6 0.04)
12. true 6, predicted 0 (top 3: 0 0.60, 5 0.31, 6 0.04)
13. true 2, predicted 0 (top 3: 0 0.59, 5 0.17, 4 0.09)
14. true 9, predicted 4 (top 3: 4 0.41, 9 0.30, 5 0.13)
15. true 3, predicted 5 (top 3: 5 0.47, 3 0.26, 8 0.17)
16. true 8, predicted 9 (top 3: 9 0.53, 5 0.19, 7 0.11)

[image: mistakes.png]
