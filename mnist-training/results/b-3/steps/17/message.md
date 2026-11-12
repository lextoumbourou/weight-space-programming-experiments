Step 16 of 50: training loss 1.0132, accuracy 0.7045.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   890    12     7    19     2     8     0     0    52     1
               1     0  1019    26     0     3     0     6    10     0     0
               2    13    11   640   174    39     0    46    13    54     0
               3     3    19    32   629     0   191    25    68    52    11
               4     5    65    14     5   641     0     2    15    96   140
               5    13    27    52    69     8   539    77    46    60    24
               6    28    59     7     8    68    60   697     0    40     0
               7    17    10    24     8    28    16     0   849    13   125
               8     8   109    89    16     6    16    40   121   580    24
               9    13    61     2     3    96    19     2   112    92   561

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

At most 34 steps left. Reply with the complete build_weights() for step 17 in one Python code block.


Here are 16 training images your step 16 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 1 (top 3: 1 0.49, 9 0.31, 4 0.15)
2. true 9, predicted 0 (top 3: 0 0.79, 8 0.09, 4 0.07)
3. true 8, predicted 5 (top 3: 5 0.35, 8 0.31, 6 0.19)
4. true 3, predicted 5 (top 3: 5 0.60, 3 0.36, 8 0.04)
5. true 8, predicted 6 (top 3: 6 0.78, 8 0.18, 0 0.02)
6. true 5, predicted 2 (top 3: 2 0.62, 3 0.31, 8 0.03)
7. true 9, predicted 7 (top 3: 7 0.83, 8 0.04, 3 0.04)
8. true 4, predicted 9 (top 3: 9 0.52, 4 0.47, 5 0.01)
9. true 0, predicted 8 (top 3: 8 0.28, 3 0.25, 0 0.22)
10. true 3, predicted 5 (top 3: 5 0.58, 8 0.33, 3 0.04)
11. true 8, predicted 1 (top 3: 1 0.97, 7 0.03, 2 0.00)
12. true 2, predicted 3 (top 3: 3 0.32, 2 0.29, 4 0.26)
13. true 3, predicted 7 (top 3: 7 0.71, 3 0.26, 2 0.01)
14. true 9, predicted 7 (top 3: 7 0.88, 1 0.09, 9 0.02)
15. true 8, predicted 2 (top 3: 2 0.50, 8 0.42, 7 0.04)
16. true 3, predicted 5 (top 3: 5 0.82, 3 0.16, 6 0.02)

[image: mistakes.png]
