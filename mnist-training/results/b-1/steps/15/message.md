Step 14 of 50: training loss 4.0279, accuracy 0.4305.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   820    36    64     3     0    25    20    23     0     0
               1     0  1044     4     2     0     1     0    13     0     0
               2    40   165   693     7     1    29     5    50     0     0
               3    14   185   130    65     0   241     0   394     0     1
               4    72   314    25     4   183    78    24   271     0    12
               5    39   349    49     4     0   358     2   114     0     0
               6   107   314    46    16    12   275   189     8     0     0
               7    16   119    13     1     0    15     0   922     0     4
               8    15   300   302    38     0   148    19   185     0     2
               9    45   164     5     4     6   128     2   576     0    31

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

At most 36 steps left. Reply with the complete build_weights() for step 15 in one Python code block.


Here are 16 training images your step 14 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 7 (top 3: 7 0.59, 5 0.25, 1 0.15)
2. true 9, predicted 7 (top 3: 7 0.44, 3 0.19, 9 0.16)
3. true 3, predicted 7 (top 3: 7 0.74, 5 0.18, 1 0.05)
4. true 3, predicted 7 (top 3: 7 0.47, 3 0.27, 5 0.19)
5. true 4, predicted 1 (top 3: 1 0.90, 7 0.08, 2 0.01)
6. true 6, predicted 5 (top 3: 5 0.45, 6 0.28, 1 0.11)
7. true 3, predicted 7 (top 3: 7 0.40, 3 0.30, 1 0.11)
8. true 4, predicted 1 (top 3: 1 1.00, 7 0.00, 2 0.00)
9. true 8, predicted 2 (top 3: 2 0.58, 1 0.28, 7 0.07)
10. true 8, predicted 1 (top 3: 1 0.72, 7 0.19, 2 0.08)
11. true 3, predicted 7 (top 3: 7 0.54, 5 0.29, 1 0.17)
12. true 3, predicted 7 (top 3: 7 0.31, 2 0.23, 5 0.21)
13. true 6, predicted 1 (top 3: 1 0.76, 5 0.12, 7 0.10)
14. true 4, predicted 1 (top 3: 1 0.34, 7 0.27, 2 0.17)
15. true 3, predicted 0 (top 3: 0 0.54, 5 0.37, 2 0.06)
16. true 8, predicted 1 (top 3: 1 0.51, 7 0.49, 2 0.00)

[image: mistakes.png]
