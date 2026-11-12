Step 24 of 50: training loss 0.8428, accuracy 0.7345.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   889    10     6    18     1     9     1     0    56     1
               1     0  1017    25     1     1     0     4    16     0     0
               2     8     6   695   124    49     0    33    11    64     0
               3     3    15    35   578     1   128    47    60   149    14
               4     5    51    15     3   669     0     0    14    76   150
               5    13    16    37    49     6   556    82    45    85    26
               6    34    43     7     8    75    30   728     0    42     0
               7    21     4    15    14    27    21     0   865    11   112
               8     6    70    50     9     5     8    40   104   693    24
               9    20    47     2     3    45    16     3    87    83   655

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

At most 26 steps left. Reply with the complete build_weights() for step 25 in one Python code block.


Here are 16 training images your step 24 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 9 (top 3: 9 0.48, 8 0.22, 4 0.15)
2. true 6, predicted 5 (top 3: 5 0.39, 6 0.31, 8 0.15)
3. true 4, predicted 8 (top 3: 8 0.52, 4 0.16, 0 0.14)
4. true 9, predicted 7 (top 3: 7 0.44, 8 0.29, 9 0.15)
5. true 2, predicted 4 (top 3: 4 0.50, 6 0.41, 5 0.04)
6. true 5, predicted 3 (top 3: 3 0.34, 5 0.29, 2 0.20)
7. true 2, predicted 4 (top 3: 4 0.50, 3 0.29, 8 0.11)
8. true 2, predicted 6 (top 3: 6 0.49, 2 0.32, 8 0.08)
9. true 4, predicted 9 (top 3: 9 0.57, 4 0.31, 8 0.07)
10. true 5, predicted 6 (top 3: 6 0.50, 8 0.30, 5 0.19)
11. true 5, predicted 8 (top 3: 8 0.36, 5 0.31, 6 0.28)
12. true 7, predicted 4 (top 3: 4 0.61, 5 0.16, 9 0.15)
13. true 3, predicted 5 (top 3: 5 0.32, 8 0.27, 3 0.22)
14. true 2, predicted 3 (top 3: 3 0.34, 5 0.23, 8 0.18)
15. true 2, predicted 8 (top 3: 8 0.65, 4 0.09, 0 0.08)
16. true 9, predicted 7 (top 3: 7 0.43, 9 0.37, 1 0.11)

[image: mistakes.png]
