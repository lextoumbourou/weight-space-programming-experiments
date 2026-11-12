Step 18 of 50: training loss 1.0565, accuracy 0.6974.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   903    14    19    32     3     5     0     1    14     0
               1     0  1030    17     0     2     0     3    12     0     0
               2     9    21   706   156    34     0    26    17    21     0
               3     3    24    49   686     0   121    23    99    15    10
               4     5    94    32     7   562     0     3    16    41   223
               5    18    31    90    93     9   481    73    74    21    25
               6    28    87    10    21    78    55   672     0    16     0
               7    14    14    28     6    21     5     0   916     3    83
               8    18   123   162    23     5    12    39   182   418    27
               9    21    73     7     3    50    15     3   145    44   600

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

At most 32 steps left. Reply with the complete build_weights() for step 19 in one Python code block.


Here are 16 training images your step 18 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 1 (top 3: 1 0.49, 4 0.29, 7 0.14)
2. true 8, predicted 1 (top 3: 1 0.99, 7 0.01, 2 0.00)
3. true 8, predicted 1 (top 3: 1 0.33, 2 0.32, 7 0.28)
4. true 8, predicted 6 (top 3: 6 0.38, 8 0.18, 3 0.16)
5. true 5, predicted 7 (top 3: 7 0.86, 1 0.13, 0 0.00)
6. true 3, predicted 7 (top 3: 7 0.85, 2 0.09, 3 0.06)
7. true 5, predicted 7 (top 3: 7 0.43, 2 0.17, 5 0.11)
8. true 5, predicted 6 (top 3: 6 0.36, 5 0.29, 3 0.14)
9. true 3, predicted 7 (top 3: 7 0.85, 1 0.06, 2 0.03)
10. true 0, predicted 3 (top 3: 3 0.44, 0 0.27, 5 0.17)
11. true 8, predicted 1 (top 3: 1 0.98, 7 0.02, 2 0.00)
12. true 7, predicted 0 (top 3: 0 0.43, 9 0.26, 5 0.13)
13. true 4, predicted 8 (top 3: 8 0.42, 4 0.32, 0 0.14)
14. true 4, predicted 9 (top 3: 9 0.51, 4 0.32, 1 0.10)
15. true 5, predicted 7 (top 3: 7 0.73, 1 0.21, 2 0.05)
16. true 3, predicted 2 (top 3: 2 0.57, 3 0.29, 8 0.12)

[image: mistakes.png]
