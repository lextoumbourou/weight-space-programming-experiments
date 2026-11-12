Step 23 of 50: training loss 0.9694, accuracy 0.7188.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   762    11     8     0     0     2   159     1    41     7
               1     0  1004    32     9     0     5     2     9     2     1
               2    33    20   581   109     5     5    50    11   156    20
               3     6     3    16   713     0   157     0     6   118    11
               4     5    33     2     0   565     1    63     2    31   281
               5     5    15     7   100     0   439    88     7   253     1
               6    21    31     0     2    25     6   868     0    10     4
               7     8     9    20    14    19    11     0   825     9   175
               8     4    83    75    29     2    32    43     6   647    88
               9    17    18     0     8    33    26    16    21    38   784

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
19 | 1.0859 | 0.6762
20 | 1.0582 | 0.6870
21 | 1.0690 | 0.7032
22 | 1.0120 | 0.7094
23 | 0.9694 | 0.7188

At most 27 steps left. Reply with the complete build_weights() for step 24 in one Python code block.


Here are 16 training images your step 23 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 8 (top 3: 8 0.45, 3 0.36, 6 0.07)
2. true 7, predicted 9 (top 3: 9 0.62, 7 0.14, 4 0.12)
3. true 7, predicted 3 (top 3: 3 0.46, 7 0.23, 8 0.13)
4. true 8, predicted 2 (top 3: 2 0.77, 1 0.16, 8 0.06)
5. true 5, predicted 8 (top 3: 8 0.61, 6 0.20, 5 0.05)
6. true 8, predicted 1 (top 3: 1 0.97, 7 0.01, 9 0.00)
7. true 1, predicted 2 (top 3: 2 0.97, 1 0.02, 8 0.01)
8. true 8, predicted 9 (top 3: 9 0.64, 1 0.18, 8 0.12)
9. true 8, predicted 5 (top 3: 5 0.39, 8 0.33, 0 0.12)
10. true 0, predicted 6 (top 3: 6 0.37, 2 0.31, 8 0.15)
11. true 9, predicted 4 (top 3: 4 0.81, 5 0.12, 9 0.06)
12. true 5, predicted 3 (top 3: 3 0.47, 1 0.33, 8 0.11)
13. true 0, predicted 6 (top 3: 6 0.37, 1 0.30, 2 0.14)
14. true 7, predicted 5 (top 3: 5 0.49, 4 0.28, 9 0.11)
15. true 5, predicted 8 (top 3: 8 0.57, 3 0.19, 6 0.12)
16. true 2, predicted 8 (top 3: 8 0.47, 3 0.40, 6 0.05)

[image: mistakes.png]
