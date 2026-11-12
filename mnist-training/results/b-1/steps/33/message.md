Step 32 of 50: training loss 0.8597, accuracy 0.7340.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   793    18    27     0     0     2   119     0    26     6
               1     0  1006    12     5    14     5     1    21     0     0
               2    38    16   600   128     7     7    26    16   135    17
               3     6     3    15   745     0   161     0    10    76    14
               4     5    52     6     2   612     0    39     3    31   233
               5     5    17     3    97     1   518    66     8   200     0
               6    29    34     0     1    26    13   849     0    14     1
               7     8     8    17    12    28    16     0   884     7   110
               8     8   123    95    21     4    46    30     9   579    94
               9    20    18     2     4    49    38    12    31    33   754

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
24 | 0.9191 | 0.7269
25 | 0.9104 | 0.7289
26 | 0.9694 | 0.7285
27 | 0.8722 | 0.7285
28 | 0.8638 | 0.7285
29 | 0.8738 | 0.7332
30 | 0.8570 | 0.7372
31 | 0.8709 | 0.7170
32 | 0.8597 | 0.7340

At most 18 steps left. Reply with the complete build_weights() for step 33 in one Python code block.


Here are 16 training images your step 32 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 1 (top 3: 1 0.70, 7 0.14, 9 0.08)
2. true 8, predicted 2 (top 3: 2 0.71, 1 0.16, 8 0.09)
3. true 4, predicted 9 (top 3: 9 0.53, 4 0.17, 1 0.14)
4. true 4, predicted 6 (top 3: 6 0.31, 9 0.26, 4 0.18)
5. true 4, predicted 8 (top 3: 8 0.40, 9 0.31, 4 0.20)
6. true 7, predicted 4 (top 3: 4 0.26, 9 0.22, 3 0.19)
7. true 4, predicted 9 (top 3: 9 0.59, 4 0.13, 8 0.10)
8. true 8, predicted 7 (top 3: 7 0.33, 3 0.22, 8 0.17)
9. true 6, predicted 4 (top 3: 4 0.32, 6 0.25, 1 0.17)
10. true 3, predicted 5 (top 3: 5 0.58, 3 0.38, 8 0.03)
11. true 5, predicted 8 (top 3: 8 0.40, 6 0.29, 3 0.13)
12. true 8, predicted 2 (top 3: 2 0.29, 7 0.25, 3 0.18)
13. true 5, predicted 8 (top 3: 8 0.43, 3 0.35, 6 0.11)
14. true 4, predicted 9 (top 3: 9 0.42, 4 0.30, 6 0.11)
15. true 1, predicted 2 (top 3: 2 0.55, 1 0.36, 8 0.06)
16. true 5, predicted 8 (top 3: 8 0.42, 3 0.19, 5 0.15)

[image: mistakes.png]
