Step 13 of 50: training loss 1.9350, accuracy 0.5070.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   936     4    22     4     0     1     5     5    14     0
               1     0   941    57    27     0     5     0    34     0     0
               2   178    37   634    49     4    12    37    25    14     0
               3    83    45   122   320     0   261     7   178    14     0
               4   191   108    30    13   398    34    58   102     0    49
               5   140   158    82    61     1   380    15    72     5     1
               6   260    99    28    39    13   112   415     1     0     0
               7    85    24    49    19     8    42     0   833     1    29
               8   108    73   393   154     1   115    29    71    48    17
               9   175    40    12    20    75   143     8   321     2   165

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

At most 37 steps left. Reply with the complete build_weights() for step 14 in one Python code block.


Here are 16 training images your step 13 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 3 (top 3: 3 0.33, 5 0.16, 2 0.13)
2. true 3, predicted 1 (top 3: 1 0.90, 7 0.09, 2 0.00)
3. true 8, predicted 3 (top 3: 3 0.30, 2 0.28, 7 0.24)
4. true 9, predicted 0 (top 3: 0 0.40, 7 0.22, 2 0.15)
5. true 6, predicted 3 (top 3: 3 0.64, 6 0.14, 5 0.09)
6. true 3, predicted 5 (top 3: 5 0.69, 7 0.17, 3 0.10)
7. true 8, predicted 2 (top 3: 2 0.71, 3 0.13, 8 0.09)
8. true 9, predicted 7 (top 3: 7 0.64, 1 0.27, 5 0.06)
9. true 9, predicted 0 (top 3: 0 0.79, 5 0.09, 7 0.08)
10. true 6, predicted 0 (top 3: 0 0.68, 5 0.23, 2 0.04)
11. true 9, predicted 7 (top 3: 7 0.67, 1 0.29, 2 0.02)
12. true 5, predicted 1 (top 3: 1 0.80, 7 0.11, 2 0.08)
13. true 2, predicted 0 (top 3: 0 0.51, 2 0.46, 4 0.01)
14. true 9, predicted 7 (top 3: 7 0.50, 5 0.34, 3 0.06)
15. true 2, predicted 8 (top 3: 8 0.53, 0 0.26, 6 0.09)
16. true 9, predicted 6 (top 3: 6 0.36, 4 0.29, 8 0.17)

[image: mistakes.png]
