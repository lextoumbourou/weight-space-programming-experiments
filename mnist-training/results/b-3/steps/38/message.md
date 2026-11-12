Step 37 of 50: training loss 0.7774, accuracy 0.7684.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   885     6    27    25     1    13     5     0    27     2
               1     0   965    42     1     1     0     0    55     0     0
               2    14     5   705   156    42     0    12    10    45     1
               3     5     1    43   685     4   103    28    30   117    14
               4     6    21    22     2   798     0     2    14    22    96
               5    13     6    32    58     6   625    87    30    43    15
               6    35    23    22     8    70    35   762     3     9     0
               7    24     1    24    28    33    39     0   849     0    92
               8    15    35    64    14     8    14    40    93   684    42
               9    23    15     4     7    55    23     1    68    39   726

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

At most 13 steps left. Reply with the complete build_weights() for step 38 in one Python code block.


Here are 16 training images your step 37 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 3 (top 3: 3 0.47, 8 0.25, 4 0.11)
2. true 5, predicted 1 (top 3: 1 0.51, 5 0.18, 7 0.10)
3. true 6, predicted 5 (top 3: 5 0.30, 6 0.25, 0 0.24)
4. true 9, predicted 2 (top 3: 2 0.49, 8 0.16, 9 0.14)
5. true 0, predicted 5 (top 3: 5 0.54, 2 0.21, 3 0.13)
6. true 7, predicted 9 (top 3: 9 0.43, 8 0.26, 0 0.15)
7. true 5, predicted 6 (top 3: 6 0.39, 2 0.28, 3 0.10)
8. true 3, predicted 8 (top 3: 8 0.67, 5 0.15, 3 0.09)
9. true 3, predicted 5 (top 3: 5 0.49, 3 0.47, 6 0.03)
10. true 3, predicted 8 (top 3: 8 0.53, 5 0.13, 2 0.11)
11. true 7, predicted 5 (top 3: 5 0.42, 9 0.36, 4 0.18)
12. true 7, predicted 9 (top 3: 9 0.28, 7 0.26, 5 0.24)
13. true 8, predicted 7 (top 3: 7 0.60, 2 0.31, 3 0.03)
14. true 6, predicted 4 (top 3: 4 0.45, 6 0.37, 5 0.06)
15. true 7, predicted 5 (top 3: 5 0.35, 3 0.18, 4 0.16)
16. true 4, predicted 1 (top 3: 1 0.33, 7 0.25, 2 0.18)

[image: mistakes.png]
