Step 19 of 50: training loss 0.9941, accuracy 0.7178.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   910    12    12    26     3     7     1     1    18     1
               1     0  1018    24     0     3     0     2    17     0     0
               2    10    10   692   187    44     0    16    17    14     0
               3     3    16    38   691     0   168    16    74    15     9
               4     5    67    31     8   735     1     2    18    22    94
               5    12    23    54    79     9   605    43    62    13    15
               6    22    73    10    22   102    99   630     0     9     0
               7    18     8    25    10    29    35     0   909     1    55
               8     7   102   171    28     4    22    43   169   440    23
               9    20    59     7     5    97    30     1   153    41   548

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

At most 31 steps left. Reply with the complete build_weights() for step 20 in one Python code block.


Here are 16 training images your step 19 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 2 (top 3: 2 0.37, 5 0.24, 3 0.15)
2. true 6, predicted 4 (top 3: 4 0.97, 5 0.02, 6 0.01)
3. true 9, predicted 1 (top 3: 1 0.93, 7 0.07, 9 0.00)
4. true 3, predicted 8 (top 3: 8 0.63, 5 0.22, 3 0.13)
5. true 9, predicted 5 (top 3: 5 0.71, 0 0.13, 9 0.10)
6. true 9, predicted 0 (top 3: 0 0.53, 4 0.21, 9 0.08)
7. true 4, predicted 1 (top 3: 1 0.43, 4 0.39, 9 0.12)
8. true 8, predicted 3 (top 3: 3 0.72, 8 0.14, 2 0.07)
9. true 8, predicted 5 (top 3: 5 0.46, 6 0.27, 8 0.21)
10. true 7, predicted 3 (top 3: 3 0.34, 7 0.32, 2 0.26)
11. true 4, predicted 7 (top 3: 7 0.83, 1 0.11, 9 0.03)
12. true 0, predicted 2 (top 3: 2 0.47, 3 0.31, 8 0.07)
13. true 8, predicted 7 (top 3: 7 0.56, 1 0.34, 2 0.06)
14. true 3, predicted 8 (top 3: 8 0.59, 3 0.21, 5 0.14)
15. true 6, predicted 0 (top 3: 0 0.93, 8 0.03, 5 0.03)
16. true 8, predicted 2 (top 3: 2 0.49, 7 0.32, 8 0.12)

[image: mistakes.png]
