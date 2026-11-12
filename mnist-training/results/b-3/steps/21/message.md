Step 20 of 50: training loss 0.9956, accuracy 0.7153.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   908    12    12    26     3     7     1     1    20     1
               1     0  1017    26     1     3     1     0    16     0     0
               2    11    10   685   196    44     0    16    14    14     0
               3     3    16    37   702     1   163    11    70    18     9
               4     5    63    34     8   754     1     2    17    18    81
               5    13    23    53    83    10   610    35    59    14    15
               6    23    72    10    26   109   107   611     0     9     0
               7    20     8    28    11    32    40     0   897     3    51
               8     8   101   185    28     4    26    39   161   433    24
               9    20    59     8     6   105    33     1   152    41   536

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

At most 30 steps left. Reply with the complete build_weights() for step 21 in one Python code block.


Here are 16 training images your step 20 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 7 (top 3: 7 0.62, 2 0.18, 1 0.17)
2. true 8, predicted 9 (top 3: 9 0.49, 8 0.26, 7 0.10)
3. true 7, predicted 0 (top 3: 0 0.61, 9 0.20, 5 0.10)
4. true 8, predicted 2 (top 3: 2 0.57, 8 0.29, 7 0.06)
5. true 9, predicted 4 (top 3: 4 0.44, 9 0.42, 7 0.07)
6. true 4, predicted 1 (top 3: 1 0.99, 7 0.01, 4 0.00)
7. true 3, predicted 5 (top 3: 5 0.91, 6 0.06, 4 0.01)
8. true 3, predicted 8 (top 3: 8 0.47, 3 0.29, 5 0.20)
9. true 3, predicted 2 (top 3: 2 0.40, 7 0.38, 3 0.20)
10. true 0, predicted 3 (top 3: 3 0.41, 0 0.34, 2 0.13)
11. true 4, predicted 1 (top 3: 1 0.55, 7 0.39, 4 0.03)
12. true 5, predicted 7 (top 3: 7 0.74, 1 0.18, 2 0.08)
13. true 8, predicted 7 (top 3: 7 0.29, 8 0.26, 2 0.23)
14. true 3, predicted 7 (top 3: 7 0.68, 3 0.24, 2 0.06)
15. true 3, predicted 7 (top 3: 7 0.92, 3 0.05, 2 0.02)
16. true 0, predicted 3 (top 3: 3 0.75, 2 0.10, 5 0.10)

[image: mistakes.png]
