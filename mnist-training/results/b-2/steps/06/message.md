Step 5 of 50: training loss 1.1885, accuracy 0.6594.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   895    15    47     5     1     8    19     0     1     0
               1     3  1010    33     0     0     4     0    12     0     2
               2    24    35   638   196    30     7     8    12    12    28
               3     9     7    14   788     1   122    10    14    35    30
               4     8   153    39    11   573     4    25    17     3   150
               5    12     7    15   134     5   573    85    59    22     3
               6   111    55    15     9    58    63   650     1     5     0
               7    32    29    48    81     0     4     0   523     0   373
               8    29   121    62    21     2    12    67   216   303   176
               9    44    38    20    66    14    22    19    97     0   641

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906
4 | 1.3284 | 0.6249
5 | 1.1885 | 0.6594

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.


Here are 16 training images your step 5 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 9 (top 3: 9 0.97, 7 0.03, 0 0.00)
2. true 2, predicted 3 (top 3: 3 0.86, 2 0.14, 9 0.00)
3. true 3, predicted 5 (top 3: 5 0.99, 3 0.01, 6 0.00)
4. true 6, predicted 5 (top 3: 5 0.93, 3 0.03, 0 0.02)
5. true 7, predicted 9 (top 3: 9 0.85, 7 0.15, 1 0.00)
6. true 2, predicted 3 (top 3: 3 0.95, 2 0.04, 8 0.00)
7. true 7, predicted 9 (top 3: 9 0.60, 7 0.20, 1 0.10)
8. true 5, predicted 3 (top 3: 3 0.76, 5 0.23, 2 0.00)
9. true 5, predicted 6 (top 3: 6 0.53, 8 0.45, 1 0.01)
10. true 7, predicted 2 (top 3: 2 0.66, 7 0.31, 8 0.01)
11. true 7, predicted 9 (top 3: 9 0.71, 7 0.28, 3 0.00)
12. true 2, predicted 9 (top 3: 9 0.59, 2 0.19, 3 0.19)
13. true 8, predicted 9 (top 3: 9 0.57, 8 0.28, 7 0.10)
14. true 6, predicted 1 (top 3: 1 0.47, 6 0.44, 8 0.08)
15. true 6, predicted 5 (top 3: 5 0.37, 6 0.28, 0 0.10)
16. true 8, predicted 7 (top 3: 7 0.41, 8 0.24, 1 0.23)

[image: mistakes.png]
