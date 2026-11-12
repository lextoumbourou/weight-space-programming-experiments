Step 21 of 50: training loss 1.0361, accuracy 0.7076.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   923    12    12    29     3     7     1     1     3     0
               1     0  1017    24     1     2     1     0    19     0     0
               2    16    10   695   196    45     0     8    19     1     0
               3     3    13    32   741     2   150     7    73     6     3
               4     8    63    36    10   801     1     1    31     0    32
               5    17    23    53    96    11   618    25    63     3     6
               6    35    80    13    28   121   114   574     1     1     0
               7    25     3    25     7    29    48     0   932     0    21
               8    34    99   267    36     9    46    40   176   280    22
               9    27    55    12     6   143    52     0   167     4   495

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

At most 29 steps left. Reply with the complete build_weights() for step 22 in one Python code block.


Here are 16 training images your step 21 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 4 (top 3: 4 0.64, 3 0.12, 9 0.11)
2. true 5, predicted 7 (top 3: 7 0.61, 5 0.15, 2 0.11)
3. true 9, predicted 1 (top 3: 1 0.52, 7 0.48, 2 0.00)
4. true 4, predicted 1 (top 3: 1 0.60, 4 0.35, 6 0.02)
5. true 9, predicted 4 (top 3: 4 0.33, 0 0.28, 9 0.23)
6. true 8, predicted 2 (top 3: 2 0.53, 8 0.21, 3 0.19)
7. true 8, predicted 1 (top 3: 1 0.91, 7 0.06, 2 0.01)
8. true 8, predicted 3 (top 3: 3 0.55, 0 0.20, 5 0.17)
9. true 6, predicted 4 (top 3: 4 0.43, 5 0.43, 0 0.11)
10. true 3, predicted 1 (top 3: 1 0.68, 2 0.15, 3 0.09)
11. true 3, predicted 5 (top 3: 5 0.83, 3 0.16, 8 0.00)
12. true 5, predicted 3 (top 3: 3 0.51, 5 0.48, 6 0.01)
13. true 5, predicted 3 (top 3: 3 0.38, 5 0.27, 2 0.21)
14. true 8, predicted 2 (top 3: 2 0.84, 8 0.04, 3 0.04)
15. true 8, predicted 2 (top 3: 2 0.57, 7 0.16, 8 0.16)
16. true 8, predicted 2 (top 3: 2 0.71, 8 0.10, 0 0.10)

[image: mistakes.png]
