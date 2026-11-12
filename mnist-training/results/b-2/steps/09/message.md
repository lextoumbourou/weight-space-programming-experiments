Step 8 of 50: training loss 1.1344, accuracy 0.6834.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   892    14    33     5     1     8    37     0     1     0
               1     4  1012    36     0     0     4     0     5     0     3
               2    23    21   566   250    41     6    15    32    17    19
               3     6     2    11   789     2   144     9    20    35    12
               4     5   111    25    13   641     2    43     5    11   127
               5    12     5    14   138     6   592    91    12    43     2
               6   100    39     6     9   130   103   561     0    19     0
               7    42    18    47    92     2     6     0   706     2   175
               8    21    89    95    23     6    15    69    98   463   130
               9    43    40    37    78    29    35    18    66     3   612

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

At most 42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.


Here are 16 training images your step 8 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 3 (top 3: 3 0.73, 0 0.20, 2 0.05)
2. true 6, predicted 8 (top 3: 8 0.62, 4 0.21, 1 0.07)
3. true 4, predicted 6 (top 3: 6 0.38, 5 0.31, 4 0.14)
4. true 5, predicted 6 (top 3: 6 0.71, 5 0.17, 0 0.03)
5. true 7, predicted 5 (top 3: 5 0.26, 3 0.26, 4 0.24)
6. true 4, predicted 6 (top 3: 6 0.64, 8 0.14, 9 0.08)
7. true 8, predicted 9 (top 3: 9 0.45, 8 0.21, 1 0.18)
8. true 9, predicted 1 (top 3: 1 0.38, 6 0.36, 8 0.16)
9. true 7, predicted 2 (top 3: 2 0.67, 7 0.31, 9 0.02)
10. true 8, predicted 1 (top 3: 1 0.50, 8 0.40, 9 0.04)
11. true 9, predicted 3 (top 3: 3 0.59, 9 0.36, 5 0.04)
12. true 2, predicted 9 (top 3: 9 0.49, 3 0.36, 2 0.12)
13. true 6, predicted 4 (top 3: 4 0.99, 8 0.01, 5 0.00)
14. true 2, predicted 0 (top 3: 0 0.57, 7 0.29, 9 0.10)
15. true 9, predicted 3 (top 3: 3 0.86, 7 0.06, 9 0.06)
16. true 4, predicted 1 (top 3: 1 0.31, 7 0.23, 8 0.15)

[image: mistakes.png]
