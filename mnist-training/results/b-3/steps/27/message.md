Step 26 of 50: training loss 0.8296, accuracy 0.7406.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   897     9     8    17     1     9     1     0    48     1
               1     0  1013    28     1     0     0     5    17     0     0
               2     9     6   698   143    42     0    32     6    54     0
               3     3    12    35   616     0   118    51    48   134    13
               4     5    39    21     3   668     1     1    15    68   162
               5    12    11    39    56     5   569    89    38    73    23
               6    34    31     7     9    66    36   749     0    35     0
               7    23     4    24    22    24    31     0   838     8   116
               8     6    59    72    12     5     9    44    90   685    27
               9    21    36     3     4    38    20     3    85    78   673

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

At most 24 steps left. Reply with the complete build_weights() for step 27 in one Python code block.


Here are 16 training images your step 26 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 9 (top 3: 9 0.61, 4 0.36, 5 0.02)
2. true 3, predicted 5 (top 3: 5 0.58, 3 0.40, 8 0.01)
3. true 0, predicted 1 (top 3: 1 0.86, 8 0.07, 6 0.02)
4. true 0, predicted 8 (top 3: 8 0.45, 0 0.37, 6 0.15)
5. true 4, predicted 9 (top 3: 9 0.49, 4 0.36, 5 0.12)
6. true 4, predicted 9 (top 3: 9 0.49, 4 0.38, 8 0.10)
7. true 7, predicted 9 (top 3: 9 0.71, 7 0.14, 5 0.07)
8. true 8, predicted 2 (top 3: 2 0.46, 8 0.44, 3 0.03)
9. true 4, predicted 9 (top 3: 9 0.61, 4 0.25, 5 0.08)
10. true 5, predicted 8 (top 3: 8 0.53, 3 0.23, 5 0.10)
11. true 6, predicted 4 (top 3: 4 0.43, 8 0.21, 6 0.18)
12. true 9, predicted 1 (top 3: 1 0.77, 7 0.15, 0 0.02)
13. true 4, predicted 9 (top 3: 9 0.53, 4 0.39, 8 0.06)
14. true 5, predicted 8 (top 3: 8 0.60, 5 0.24, 6 0.14)
15. true 4, predicted 9 (top 3: 9 0.50, 4 0.37, 5 0.06)
16. true 8, predicted 6 (top 3: 6 0.69, 8 0.11, 0 0.10)

[image: mistakes.png]
