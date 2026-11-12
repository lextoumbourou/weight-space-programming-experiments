Step 12 of 50: training loss 2.1344, accuracy 0.4372.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   945     6    21     0     0     2     0     0    17     0
               1     0  1010    34     2     0    17     1     0     0     0
               2   224    48   591     4     5    27    61     4    26     0
               3    81    83   202   182     0   425     0    37    20     0
               4   217   179    32     2   477    32    34     4     6     0
               5   167   200    80     5     1   421    27     2    12     0
               6   305   111    11     6    13   123   394     0     4     0
               7    96   134   323    12    24   238     0   222     3    38
               8   131   107   465     6     3   184     5     0   107     1
               9   192   153    74     5   228   268     1     4    13    23

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078
5 | 2.7367 | 0.4958
6 | 2.3875 | 0.4751
7 | 5.6237 | 0.2327
8 | 1.8055 | 0.4696
9 | 1.9854 | 0.4561
10 | 1.5771 | 0.5330
11 | 1.8457 | 0.4671
12 | 2.1344 | 0.4372

At most 38 steps left. Reply with the complete build_weights() for step 13 in one Python code block.


Here are 16 training images your step 12 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 0 (top 3: 0 0.83, 5 0.08, 4 0.07)
2. true 2, predicted 6 (top 3: 6 0.68, 8 0.14, 4 0.09)
3. true 9, predicted 2 (top 3: 2 0.32, 5 0.24, 3 0.19)
4. true 4, predicted 0 (top 3: 0 0.33, 2 0.25, 6 0.20)
5. true 9, predicted 1 (top 3: 1 0.30, 5 0.28, 4 0.13)
6. true 5, predicted 1 (top 3: 1 0.67, 2 0.27, 0 0.02)
7. true 3, predicted 1 (top 3: 1 0.61, 5 0.35, 7 0.03)
8. true 4, predicted 0 (top 3: 0 0.38, 1 0.36, 4 0.14)
9. true 9, predicted 2 (top 3: 2 0.34, 9 0.27, 3 0.23)
10. true 5, predicted 0 (top 3: 0 0.54, 5 0.44, 2 0.01)
11. true 9, predicted 1 (top 3: 1 0.77, 7 0.12, 5 0.09)
12. true 9, predicted 0 (top 3: 0 0.75, 5 0.12, 2 0.05)
13. true 9, predicted 0 (top 3: 0 0.53, 5 0.35, 4 0.09)
14. true 4, predicted 5 (top 3: 5 0.80, 4 0.09, 1 0.05)
15. true 2, predicted 5 (top 3: 5 0.29, 0 0.19, 6 0.13)
16. true 2, predicted 0 (top 3: 0 0.53, 2 0.20, 8 0.12)

[image: mistakes.png]
