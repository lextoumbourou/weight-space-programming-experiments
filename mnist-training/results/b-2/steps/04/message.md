Step 3 of 50: training loss 1.4210, accuracy 0.5906.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   818    15   106     7     0    13    30     1     0     1
               1     0   892    58     0     0     0     0   114     0     0
               2    18    83   687    95    17    11    11    21     1    46
               3     8    33    39   659     4   150    13    49     8    67
               4     9   180    97     2   379     0    29    68     0   219
               5     6    19    17   124     1   525   128    85     4     6
               6   104    46    19     9     2    27   759     1     0     0
               7    11    63    38    47     8     5     0   580     0   338
               8    51   120   116    40     4    10    85   396    48   139
               9    50    39    29    37    25    12    35   175     0   559

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.


Here are 16 training images your step 3 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 7 (top 3: 7 0.36, 1 0.28, 2 0.21)
2. true 0, predicted 2 (top 3: 2 0.45, 0 0.38, 6 0.12)
3. true 8, predicted 7 (top 3: 7 0.37, 2 0.30, 6 0.12)
4. true 2, predicted 9 (top 3: 9 0.38, 2 0.37, 0 0.13)
5. true 8, predicted 2 (top 3: 2 0.52, 7 0.38, 9 0.05)
6. true 0, predicted 2 (top 3: 2 0.85, 6 0.12, 0 0.02)
7. true 8, predicted 9 (top 3: 9 0.49, 1 0.38, 7 0.05)
8. true 3, predicted 7 (top 3: 7 0.30, 3 0.29, 8 0.18)
9. true 0, predicted 2 (top 3: 2 0.61, 0 0.27, 6 0.12)
10. true 3, predicted 2 (top 3: 2 0.47, 9 0.22, 1 0.10)
11. true 2, predicted 1 (top 3: 1 0.90, 2 0.09, 7 0.01)
12. true 3, predicted 5 (top 3: 5 0.54, 3 0.20, 0 0.15)
13. true 1, predicted 2 (top 3: 2 0.81, 7 0.19, 1 0.00)
14. true 4, predicted 1 (top 3: 1 0.78, 4 0.20, 9 0.02)
15. true 2, predicted 1 (top 3: 1 0.45, 2 0.32, 4 0.13)
16. true 7, predicted 9 (top 3: 9 0.67, 7 0.26, 1 0.07)

[image: mistakes.png]
