Step 9 of 50: training loss 1.9282, accuracy 0.6363.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   861     9    28    15     1     5    66     0     5     1
               1     2   971    53     0     0     4     7     6     0    21
               2    19    11   473   356    37     6    28    19    10    31
               3     5     4     8   878     2    63     6    16    25    23
               4     4    77    30    19   558     3    68     5     3   216
               5    12     4     5   268     6   456   110    11    39     4
               6    70    16     5    15   113   117   596     0    35     0
               7    26     6    47   101     0     3     6   569     2   330
               8    18    82    82    27     6    11   164    78   291   250
               9    27    19    34    83    13     9    28    38     0   710

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906
4 | 1.3284 | 0.6249
5 | 1.1885 | 0.6594
6 | 1.1142 | 0.6913
7 | 1.5617 | 0.6031
8 | 1.1344 | 0.6834
9 | 1.9282 | 0.6363

At most 41 steps left. Reply with the complete build_weights() for step 10 in one Python code block.


Here are 16 training images your step 9 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 2 (top 3: 2 0.73, 6 0.15, 7 0.05)
2. true 2, predicted 3 (top 3: 3 0.95, 4 0.04, 8 0.01)
3. true 7, predicted 9 (top 3: 9 0.65, 7 0.34, 3 0.01)
4. true 2, predicted 3 (top 3: 3 0.51, 2 0.46, 9 0.02)
5. true 8, predicted 7 (top 3: 7 0.74, 8 0.21, 2 0.01)
6. true 4, predicted 6 (top 3: 6 0.34, 4 0.34, 2 0.11)
7. true 5, predicted 3 (top 3: 3 0.70, 6 0.16, 2 0.05)
8. true 7, predicted 9 (top 3: 9 0.99, 7 0.01, 5 0.00)
9. true 6, predicted 4 (top 3: 4 0.99, 8 0.00, 6 0.00)
10. true 6, predicted 0 (top 3: 0 0.83, 6 0.13, 4 0.04)
11. true 8, predicted 7 (top 3: 7 0.83, 9 0.10, 1 0.04)
12. true 7, predicted 9 (top 3: 9 0.77, 7 0.23, 0 0.00)
13. true 6, predicted 4 (top 3: 4 0.96, 0 0.04, 6 0.00)
14. true 1, predicted 2 (top 3: 2 0.69, 7 0.24, 1 0.04)
15. true 8, predicted 5 (top 3: 5 0.80, 3 0.19, 0 0.01)
16. true 9, predicted 3 (top 3: 3 0.99, 7 0.01, 2 0.00)

[image: mistakes.png]
