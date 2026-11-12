Step 18 of 50: training loss 1.0953, accuracy 0.6732.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   767     8    19     3     0     5    59     1   123     6
               1     0   957    74    18     0     5     2     6     2     0
               2    29    10   643   119    20     8    47     8    98     8
               3     5     5    38   713     2   175     0     6    82     4
               4     4    24     7     7   660     1    45     3    54   178
               5     4    14    20   139     2   413    59     4   258     2
               6    23    36     3    32    63    10   784     0    13     3
               7     9    12    35    38    24    36     0   790    18   128
               8     6    74   194   230     1    74    11    10   347    62
               9    20    25     1    42    95    35     7    45    33   658

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
13 | 1.9350 | 0.5070
14 | 4.0279 | 0.4305
15 | 1.3307 | 0.6072
16 | 1.1902 | 0.6406
17 | 1.3253 | 0.6170
18 | 1.0953 | 0.6732

At most 32 steps left. Reply with the complete build_weights() for step 19 in one Python code block.


Here are 16 training images your step 18 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 9 (top 3: 9 0.48, 3 0.15, 8 0.11)
2. true 6, predicted 1 (top 3: 1 0.90, 3 0.06, 6 0.03)
3. true 3, predicted 2 (top 3: 2 0.65, 3 0.30, 7 0.03)
4. true 3, predicted 5 (top 3: 5 0.55, 3 0.38, 9 0.03)
5. true 9, predicted 6 (top 3: 6 0.34, 9 0.26, 4 0.18)
6. true 0, predicted 8 (top 3: 8 0.45, 6 0.31, 2 0.16)
7. true 4, predicted 9 (top 3: 9 0.47, 4 0.29, 8 0.13)
8. true 2, predicted 3 (top 3: 3 0.55, 2 0.40, 8 0.03)
9. true 8, predicted 3 (top 3: 3 0.39, 8 0.35, 1 0.10)
10. true 6, predicted 9 (top 3: 9 0.41, 4 0.29, 6 0.19)
11. true 4, predicted 1 (top 3: 1 0.99, 3 0.01, 7 0.00)
12. true 7, predicted 9 (top 3: 9 0.36, 3 0.33, 4 0.14)
13. true 0, predicted 8 (top 3: 8 0.53, 6 0.34, 2 0.06)
14. true 2, predicted 8 (top 3: 8 0.54, 3 0.16, 6 0.12)
15. true 5, predicted 1 (top 3: 1 0.69, 2 0.23, 8 0.04)
16. true 1, predicted 2 (top 3: 2 0.68, 1 0.31, 3 0.01)

[image: mistakes.png]
