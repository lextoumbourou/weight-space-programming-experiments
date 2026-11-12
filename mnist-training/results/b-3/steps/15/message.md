Step 14 of 50: training loss 1.0054, accuracy 0.6912.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   881    12     3    18     1     6     0     0    69     1
               1     0  1026    20     0     2     0     6     9     0     1
               2    13    12   625   181    39     0    41    10    69     0
               3     3    22    31   662     0   156    27    43    71    15
               4     4    74    12     5   566     0     2     6   121   193
               5    15    34    51    85     8   493    77    28    95    29
               6    29    61     7    10    61    48   689     0    62     0
               7    15    11    31    15    27    12     3   737    23   216
               8     9   118    69    16     5     9    36    86   627    34
               9    14    77     2     3    76    15     2    57   109   606

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

At most 36 steps left. Reply with the complete build_weights() for step 15 in one Python code block.


Here are 16 training images your step 14 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 4 (top 3: 4 0.38, 7 0.18, 1 0.15)
2. true 2, predicted 6 (top 3: 6 0.32, 2 0.24, 1 0.23)
3. true 3, predicted 5 (top 3: 5 0.38, 3 0.33, 9 0.21)
4. true 8, predicted 3 (top 3: 3 0.46, 8 0.30, 5 0.10)
5. true 5, predicted 9 (top 3: 9 0.84, 8 0.05, 5 0.05)
6. true 7, predicted 4 (top 3: 4 0.60, 9 0.29, 3 0.07)
7. true 5, predicted 7 (top 3: 7 0.64, 5 0.19, 9 0.05)
8. true 7, predicted 9 (top 3: 9 0.61, 5 0.22, 4 0.08)
9. true 4, predicted 1 (top 3: 1 0.69, 4 0.16, 9 0.08)
10. true 7, predicted 4 (top 3: 4 0.61, 3 0.17, 6 0.09)
11. true 9, predicted 1 (top 3: 1 0.23, 8 0.22, 2 0.12)
12. true 7, predicted 4 (top 3: 4 0.48, 9 0.29, 3 0.15)
13. true 8, predicted 2 (top 3: 2 0.80, 8 0.08, 7 0.07)
14. true 5, predicted 8 (top 3: 8 0.29, 5 0.21, 2 0.21)
15. true 8, predicted 1 (top 3: 1 0.81, 7 0.18, 2 0.01)
16. true 6, predicted 5 (top 3: 5 0.43, 6 0.28, 8 0.21)

[image: mistakes.png]
