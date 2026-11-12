Step 9 of 50: training loss 1.9854, accuracy 0.4561.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   959    11     1     0     0     0    20     0     0     0
               1     0  1046     6     0     0     4     4     3     1     0
               2   233    96   420     1    20     2   214     2     2     0
               3   294   122    61   170     2   224    35    82    37     3
               4    65   135     2     0   577     0   188     0     9     7
               5   179   152     3     0     4   241   320     1    14     1
               6   165    46     0     0    53     0   703     0     0     0
               7   118   184   222     1    25    41     1   245     2   251
               8   369   306    66     0     4    11   150    10    89     4
               9   333   228    15     0   150    32    56     8    28   111

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

At most 41 steps left. Reply with the complete build_weights() for step 10 in one Python code block.


Here are 16 training images your step 9 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 6 (top 3: 6 0.53, 5 0.18, 0 0.16)
2. true 5, predicted 1 (top 3: 1 0.51, 6 0.25, 8 0.21)
3. true 7, predicted 1 (top 3: 1 0.51, 7 0.24, 2 0.11)
4. true 4, predicted 0 (top 3: 0 0.58, 4 0.36, 6 0.05)
5. true 2, predicted 1 (top 3: 1 0.40, 6 0.32, 2 0.21)
6. true 8, predicted 1 (top 3: 1 0.90, 7 0.08, 8 0.01)
7. true 4, predicted 1 (top 3: 1 0.38, 4 0.22, 7 0.11)
8. true 8, predicted 6 (top 3: 6 0.54, 2 0.17, 0 0.14)
9. true 7, predicted 2 (top 3: 2 0.71, 7 0.22, 9 0.03)
10. true 0, predicted 1 (top 3: 1 0.47, 6 0.23, 0 0.14)
11. true 4, predicted 1 (top 3: 1 0.42, 6 0.35, 8 0.16)
12. true 9, predicted 1 (top 3: 1 0.47, 8 0.15, 7 0.13)
13. true 4, predicted 6 (top 3: 6 0.53, 1 0.17, 8 0.10)
14. true 9, predicted 1 (top 3: 1 0.22, 8 0.20, 0 0.19)
15. true 5, predicted 0 (top 3: 0 0.69, 6 0.27, 8 0.02)
16. true 3, predicted 6 (top 3: 6 0.28, 0 0.26, 8 0.19)

[image: mistakes.png]
