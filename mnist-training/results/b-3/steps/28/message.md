Step 27 of 50: training loss 0.8180, accuracy 0.7502.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   898     9     9    23     0    10     2     0    39     1
               1     0  1010    29     1     1     0     4    19     0     0
               2     9     6   693   177    24     0    35     6    40     0
               3     3     9    35   666     0   132    41    43    89    12
               4     6    36    23     4   732     1     3    15    64    99
               5    10    10    35    65     6   598    84    36    52    19
               6    34    31     8    12    51    52   755     0    24     0
               7    24     4    25    25    24    41     0   835     8   104
               8     6    54    90    14     7    13    50    92   655    28
               9    24    34     5     5    55    22     3    85    68   660

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

At most 23 steps left. Reply with the complete build_weights() for step 28 in one Python code block.


Here are 16 training images your step 27 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 3 (top 3: 3 0.51, 0 0.20, 5 0.16)
2. true 4, predicted 8 (top 3: 8 0.49, 4 0.42, 6 0.07)
3. true 2, predicted 6 (top 3: 6 0.55, 8 0.17, 2 0.11)
4. true 9, predicted 1 (top 3: 1 0.67, 7 0.31, 4 0.01)
5. true 2, predicted 3 (top 3: 3 0.46, 2 0.36, 5 0.07)
6. true 2, predicted 3 (top 3: 3 0.53, 4 0.19, 5 0.11)
7. true 5, predicted 6 (top 3: 6 0.48, 5 0.17, 2 0.14)
8. true 3, predicted 8 (top 3: 8 0.38, 3 0.32, 5 0.21)
9. true 4, predicted 8 (top 3: 8 0.41, 2 0.25, 0 0.10)
10. true 2, predicted 3 (top 3: 3 0.51, 2 0.38, 6 0.08)
11. true 9, predicted 4 (top 3: 4 0.66, 9 0.17, 5 0.06)
12. true 2, predicted 3 (top 3: 3 0.42, 5 0.27, 6 0.13)
13. true 8, predicted 7 (top 3: 7 0.41, 1 0.28, 2 0.13)
14. true 3, predicted 8 (top 3: 8 0.34, 5 0.33, 3 0.28)
15. true 3, predicted 5 (top 3: 5 0.39, 3 0.31, 8 0.26)
16. true 0, predicted 5 (top 3: 5 0.40, 0 0.39, 3 0.13)

[image: mistakes.png]
