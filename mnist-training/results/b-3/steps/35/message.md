Step 34 of 50: training loss 0.8062, accuracy 0.7472.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   886     7    10    27     0    10     3     0    47     1
               1     0   982    43     2     1     1     2    33     0     0
               2     9     5   690   173    28     0    25     8    52     0
               3     3     3    40   662     0   114    41    34   118    15
               4     5    26    26     5   683     1     2    16    70   149
               5    10     8    33    67     5   586   100    31    57    18
               6    25    23    16    13    49    45   775     0    21     0
               7    25     2    29    25    27    49     0   819     8   106
               8     8    40    84    13     5    12    49    79   681    38
               9    23    27     5     6    37    21     4    61    69   708

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

At most 16 steps left. Reply with the complete build_weights() for step 35 in one Python code block.


Here are 16 training images your step 34 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 5 (top 3: 5 0.60, 9 0.22, 0 0.07)
2. true 6, predicted 4 (top 3: 4 0.76, 5 0.16, 6 0.02)
3. true 6, predicted 0 (top 3: 0 0.71, 5 0.19, 2 0.07)
4. true 4, predicted 9 (top 3: 9 0.68, 4 0.23, 8 0.07)
5. true 9, predicted 8 (top 3: 8 0.53, 9 0.27, 7 0.07)
6. true 7, predicted 4 (top 3: 4 0.46, 3 0.25, 5 0.07)
7. true 3, predicted 7 (top 3: 7 0.71, 1 0.20, 2 0.07)
8. true 4, predicted 8 (top 3: 8 0.51, 4 0.34, 9 0.08)
9. true 9, predicted 4 (top 3: 4 0.49, 9 0.29, 5 0.09)
10. true 2, predicted 8 (top 3: 8 0.36, 0 0.33, 2 0.15)
11. true 4, predicted 9 (top 3: 9 0.68, 4 0.24, 2 0.02)
12. true 3, predicted 8 (top 3: 8 0.78, 3 0.08, 2 0.06)
13. true 8, predicted 5 (top 3: 5 0.40, 3 0.24, 8 0.22)
14. true 2, predicted 4 (top 3: 4 0.75, 3 0.22, 9 0.01)
15. true 2, predicted 8 (top 3: 8 0.62, 0 0.11, 6 0.08)
16. true 8, predicted 2 (top 3: 2 0.31, 8 0.26, 5 0.19)

[image: mistakes.png]
