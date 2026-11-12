Step 15 of 50: training loss 1.3050, accuracy 0.6310.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   804     1     0     0     1     4     1     0   180     0
               1     0   967    74     0     0     3    12     7     1     0
               2    22     4   499    60    69     2    72     5   257     0
               3     1     6    12   442     4   226    39    24   272     4
               4     2    20     2     0   692     0     2    10   217    38
               5     8     9    11    33    11   458   104     9   257    15
               6    23    13     5     0    60    29   694     0   143     0
               7    27     6    32     3    65    49     2   619    81   206
               8     1    38    15     2     5    10    38    42   849     9
               9     9    25     0     1   321    18     3    61   237   286

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

At most 35 steps left. Reply with the complete build_weights() for step 16 in one Python code block.


Here are 16 training images your step 15 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 4 (top 3: 4 0.83, 9 0.10, 8 0.06)
2. true 3, predicted 8 (top 3: 8 0.49, 3 0.35, 5 0.15)
3. true 2, predicted 8 (top 3: 8 0.85, 3 0.09, 2 0.03)
4. true 9, predicted 8 (top 3: 8 0.75, 9 0.16, 4 0.08)
5. true 3, predicted 5 (top 3: 5 0.68, 8 0.21, 3 0.11)
6. true 2, predicted 6 (top 3: 6 0.83, 2 0.12, 3 0.04)
7. true 3, predicted 5 (top 3: 5 0.63, 3 0.29, 8 0.08)
8. true 8, predicted 6 (top 3: 6 0.75, 8 0.20, 4 0.03)
9. true 4, predicted 8 (top 3: 8 0.76, 4 0.22, 0 0.02)
10. true 6, predicted 5 (top 3: 5 0.57, 8 0.36, 4 0.03)
11. true 9, predicted 4 (top 3: 4 0.90, 9 0.08, 8 0.02)
12. true 9, predicted 8 (top 3: 8 0.38, 9 0.33, 5 0.15)
13. true 3, predicted 5 (top 3: 5 0.53, 3 0.44, 8 0.03)
14. true 5, predicted 8 (top 3: 8 0.62, 5 0.36, 6 0.02)
15. true 4, predicted 8 (top 3: 8 0.70, 4 0.26, 9 0.04)
16. true 9, predicted 8 (top 3: 8 0.58, 4 0.22, 9 0.20)

[image: mistakes.png]
