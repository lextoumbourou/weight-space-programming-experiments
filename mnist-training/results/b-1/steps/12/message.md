Step 11 of 50: training loss 1.8457, accuracy 0.4671.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   720     0     8     0     0     0     5     0   258     0
               1     0   755   170    30     0    22     6     0    78     3
               2    55     2   340    16     9     9   104     1   452     2
               3     6     4    39   302     1   196     0     2   460    20
               4    26    18     7     0   567     6    88     0   256    15
               5    38    32    33     6     2   343   110     0   351     0
               6    41     8     3     1    19    25   600     0   270     0
               7    40    11   212    28    34   100     0    40   135   490
               8    13     9    97     5     5    29    14     0   830     7
               9    52    11    17     2   205    56     2     0   442   174

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

At most 39 steps left. Reply with the complete build_weights() for step 12 in one Python code block.


Here are 16 training images your step 11 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 4 (top 3: 4 0.42, 9 0.38, 5 0.10)
2. true 2, predicted 8 (top 3: 8 0.83, 6 0.09, 4 0.04)
3. true 1, predicted 2 (top 3: 2 0.54, 8 0.35, 3 0.04)
4. true 2, predicted 3 (top 3: 3 0.21, 6 0.20, 8 0.14)
5. true 9, predicted 4 (top 3: 4 0.56, 8 0.30, 9 0.07)
6. true 5, predicted 8 (top 3: 8 0.75, 5 0.06, 9 0.05)
7. true 9, predicted 0 (top 3: 0 0.45, 5 0.20, 4 0.14)
8. true 4, predicted 8 (top 3: 8 0.62, 6 0.29, 4 0.07)
9. true 3, predicted 9 (top 3: 9 0.31, 8 0.27, 3 0.26)
10. true 3, predicted 8 (top 3: 8 0.52, 2 0.20, 3 0.19)
11. true 6, predicted 1 (top 3: 1 0.59, 6 0.21, 5 0.08)
12. true 3, predicted 8 (top 3: 8 0.81, 3 0.08, 0 0.05)
13. true 9, predicted 8 (top 3: 8 0.49, 4 0.21, 9 0.12)
14. true 2, predicted 8 (top 3: 8 0.40, 6 0.38, 0 0.09)
15. true 7, predicted 9 (top 3: 9 0.81, 3 0.06, 5 0.06)
16. true 2, predicted 8 (top 3: 8 0.99, 0 0.00, 6 0.00)

[image: mistakes.png]
