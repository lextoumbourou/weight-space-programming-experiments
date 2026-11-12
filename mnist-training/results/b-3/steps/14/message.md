Step 13 of 50: training loss 1.0549, accuracy 0.6888.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   914    14     7    15     1     5     1     0    34     0
               1     0  1033    16     0     2     0     7     6     0     0
               2    13    20   657   141    37     1    46     9    66     0
               3     3    28    44   615     1   199    36    45    51     8
               4     5    95    21     6   666     0     2     6    78   104
               5    16    45    63    65     8   551    97    24    27    19
               6    27    72     7     6    59    37   695     0    64     0
               7    41    22    39    12    38    54     3   806    15    60
               8    11   155   180    11     5    14    59    85   480     9
               9    18   100     4     3   116    47     6    86   110   471

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

At most 37 steps left. Reply with the complete build_weights() for step 14 in one Python code block.


Here are 16 training images your step 13 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 8 (top 3: 8 0.38, 5 0.29, 6 0.12)
2. true 8, predicted 7 (top 3: 7 0.36, 8 0.15, 9 0.10)
3. true 2, predicted 6 (top 3: 6 0.34, 8 0.22, 5 0.13)
4. true 2, predicted 3 (top 3: 3 0.41, 8 0.18, 5 0.14)
5. true 4, predicted 9 (top 3: 9 0.52, 4 0.38, 8 0.06)
6. true 8, predicted 1 (top 3: 1 0.80, 7 0.17, 6 0.01)
7. true 5, predicted 6 (top 3: 6 0.86, 5 0.05, 8 0.05)
8. true 2, predicted 7 (top 3: 7 0.57, 0 0.26, 2 0.06)
9. true 1, predicted 6 (top 3: 6 0.41, 2 0.26, 3 0.19)
10. true 9, predicted 4 (top 3: 4 0.30, 9 0.23, 1 0.22)
11. true 3, predicted 5 (top 3: 5 0.46, 3 0.24, 6 0.22)
12. true 9, predicted 2 (top 3: 2 0.26, 7 0.20, 8 0.17)
13. true 3, predicted 7 (top 3: 7 0.39, 1 0.28, 3 0.16)
14. true 8, predicted 1 (top 3: 1 0.78, 7 0.19, 2 0.02)
15. true 5, predicted 4 (top 3: 4 0.32, 5 0.21, 6 0.17)
16. true 3, predicted 6 (top 3: 6 0.33, 3 0.31, 5 0.25)

[image: mistakes.png]
