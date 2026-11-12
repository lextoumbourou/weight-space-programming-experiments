Step 6 of 50: training loss 2.3875, accuracy 0.4751.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   842     0     0     0     0     0    18     0   130     1
               1     0   919     7     0     0     4     3    15   116     0
               2    52     4   336     8    15     1    55     0   518     1
               3     8     2    21   181     0   141     2     4   667     4
               4     4     1     1     0   430     0    22     0   489    36
               5    19     5     1     0     2   286    93     1   508     0
               6    30     7     0     0    82     1   582     0   265     0
               7    21    10   192     8    11    15     0    74   275   484
               8     9    10     9     0     1     4     4     1   968     3
               9    40     5     0     0    62    17     2     0   702   133

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078
5 | 2.7367 | 0.4958
6 | 2.3875 | 0.4751

At most 44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.


Here are 16 training images your step 6 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 8 (top 3: 8 0.82, 5 0.15, 3 0.02)
2. true 5, predicted 8 (top 3: 8 0.88, 6 0.11, 1 0.00)
3. true 6, predicted 8 (top 3: 8 0.51, 4 0.19, 5 0.12)
4. true 9, predicted 8 (top 3: 8 0.80, 9 0.18, 3 0.01)
5. true 4, predicted 8 (top 3: 8 0.78, 9 0.09, 4 0.08)
6. true 9, predicted 8 (top 3: 8 0.69, 5 0.16, 9 0.06)
7. true 2, predicted 8 (top 3: 8 0.46, 2 0.30, 0 0.18)
8. true 4, predicted 8 (top 3: 8 0.98, 1 0.01, 9 0.00)
9. true 7, predicted 2 (top 3: 2 0.87, 9 0.10, 8 0.02)
10. true 4, predicted 8 (top 3: 8 0.86, 6 0.13, 4 0.01)
11. true 9, predicted 8 (top 3: 8 0.95, 1 0.04, 7 0.00)
12. true 7, predicted 9 (top 3: 9 0.65, 5 0.31, 4 0.02)
13. true 7, predicted 9 (top 3: 9 0.89, 8 0.06, 5 0.03)
14. true 5, predicted 8 (top 3: 8 0.77, 5 0.12, 3 0.08)
15. true 9, predicted 8 (top 3: 8 0.78, 4 0.17, 5 0.02)
16. true 4, predicted 8 (top 3: 8 0.88, 6 0.11, 4 0.00)

[image: mistakes.png]
