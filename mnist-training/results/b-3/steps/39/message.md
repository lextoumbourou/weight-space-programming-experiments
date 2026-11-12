Step 38 of 50: training loss 0.7774, accuracy 0.7669.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   881     6    28    26     1    13     5     0    29     2
               1     0   969    43     1     1     2     0    48     0     0
               2    13     5   691   174    41     0    12     8    45     1
               3     4     1    39   688     3   110    30    28   114    13
               4     6    23    20     5   791     0     2    13    25    98
               5    11     6    31    54     6   634    89    29    41    14
               6    32    23    22     8    66    38   766     2    10     0
               7    23     1    22    32    32    50     0   841     0    89
               8    14    36    64    14     8    14    41    90   686    42
               9    23    17     5     7    52    29     0    66    40   722

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
37 | 0.7774 | 0.7684
38 | 0.7774 | 0.7669

At most 12 steps left. Reply with the complete build_weights() for step 39 in one Python code block.


Here are 16 training images your step 38 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 9 (top 3: 9 0.67, 4 0.27, 5 0.03)
2. true 7, predicted 9 (top 3: 9 0.44, 7 0.23, 0 0.16)
3. true 2, predicted 3 (top 3: 3 0.59, 5 0.22, 9 0.05)
4. true 5, predicted 3 (top 3: 3 0.42, 5 0.32, 2 0.10)
5. true 9, predicted 8 (top 3: 8 0.31, 4 0.18, 2 0.17)
6. true 5, predicted 6 (top 3: 6 0.63, 8 0.33, 5 0.01)
7. true 5, predicted 6 (top 3: 6 0.98, 8 0.02, 5 0.00)
8. true 7, predicted 9 (top 3: 9 0.39, 4 0.24, 5 0.20)
9. true 9, predicted 1 (top 3: 1 0.53, 7 0.36, 2 0.07)
10. true 4, predicted 9 (top 3: 9 0.71, 4 0.16, 8 0.06)
11. true 4, predicted 9 (top 3: 9 0.46, 4 0.23, 8 0.16)
12. true 4, predicted 9 (top 3: 9 0.30, 4 0.29, 8 0.10)
13. true 2, predicted 7 (top 3: 7 0.46, 3 0.27, 2 0.20)
14. true 4, predicted 9 (top 3: 9 0.48, 4 0.42, 8 0.09)
15. true 3, predicted 5 (top 3: 5 0.47, 3 0.36, 8 0.12)
16. true 5, predicted 6 (top 3: 6 0.34, 9 0.32, 4 0.12)

[image: mistakes.png]
