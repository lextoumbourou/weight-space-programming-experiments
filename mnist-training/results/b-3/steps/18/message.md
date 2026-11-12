Step 17 of 50: training loss 1.2671, accuracy 0.6900.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   922    14     3     8     0     5     0     1    38     0
               1     0  1027    24     0     1     0     7     3     1     1
               2    24    19   660   131    44     0    39    10    61     2
               3     3    29    38   588     0   203    29    67    60    13
               4     5    84    10     4   502     0     3     9    91   275
               5    29    46    41    66    10   519    73    27    76    28
               6    42    67     7     7    63    65   689     0    27     0
               7    36    24    24     2    17    27     0   842    10   108
               8    15   145    93    14     5    11    40   119   541    26
               9    33    84     1     2    60    12     1    95    63   610

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

At most 33 steps left. Reply with the complete build_weights() for step 18 in one Python code block.


Here are 16 training images your step 17 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 0 (top 3: 0 0.51, 7 0.26, 9 0.23)
2. true 3, predicted 5 (top 3: 5 0.55, 3 0.43, 0 0.01)
3. true 2, predicted 8 (top 3: 8 0.73, 3 0.15, 6 0.10)
4. true 2, predicted 9 (top 3: 9 0.60, 3 0.15, 4 0.15)
5. true 4, predicted 1 (top 3: 1 1.00, 7 0.00, 9 0.00)
6. true 5, predicted 1 (top 3: 1 0.97, 7 0.01, 6 0.01)
7. true 4, predicted 7 (top 3: 7 0.52, 8 0.38, 9 0.05)
8. true 3, predicted 1 (top 3: 1 0.94, 7 0.03, 3 0.02)
9. true 3, predicted 7 (top 3: 7 0.94, 2 0.05, 3 0.01)
10. true 4, predicted 9 (top 3: 9 0.72, 4 0.13, 8 0.13)
11. true 8, predicted 7 (top 3: 7 0.61, 2 0.24, 3 0.12)
12. true 6, predicted 0 (top 3: 0 0.92, 5 0.07, 8 0.01)
13. true 2, predicted 3 (top 3: 3 0.59, 8 0.37, 4 0.02)
14. true 2, predicted 6 (top 3: 6 0.77, 3 0.11, 4 0.11)
15. true 6, predicted 5 (top 3: 5 0.77, 8 0.17, 6 0.04)
16. true 9, predicted 1 (top 3: 1 0.97, 7 0.03, 2 0.00)

[image: mistakes.png]
