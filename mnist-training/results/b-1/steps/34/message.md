Step 33 of 50: training loss 0.8500, accuracy 0.7380.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   801    17    34     0     0     2   105     0    26     6
               1     0  1004    14     5    16     4     1    20     0     0
               2    39    16   623   128    10     8    22    16   114    14
               3     6     3    16   743     0   171     0    11    69    11
               4     4    50     7     2   646     0    36     3    32   203
               5     5    16     3   103     1   528    63     8   188     0
               6    29    34     0     2    31    14   841     0    15     1
               7     8     8    19    13    29    16     0   897     7    93
               8     8   116   118    21     4    46    29    11   571    85
               9    21    18     2     5    60    45    12    36    36   726

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
33 | 0.8500 | 0.7380

At most 17 steps left. Reply with the complete build_weights() for step 34 in one Python code block.


Here are 16 training images your step 33 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 8 (top 3: 8 0.31, 3 0.30, 5 0.25)
2. true 8, predicted 2 (top 3: 2 0.48, 8 0.25, 6 0.17)
3. true 0, predicted 1 (top 3: 1 0.44, 7 0.29, 9 0.13)
4. true 8, predicted 5 (top 3: 5 0.33, 0 0.32, 8 0.23)
5. true 5, predicted 8 (top 3: 8 0.52, 6 0.17, 3 0.14)
6. true 6, predicted 4 (top 3: 4 0.49, 0 0.24, 9 0.13)
7. true 2, predicted 4 (top 3: 4 0.28, 3 0.21, 2 0.17)
8. true 1, predicted 4 (top 3: 4 0.31, 1 0.23, 7 0.23)
9. true 2, predicted 3 (top 3: 3 0.37, 6 0.14, 2 0.14)
10. true 5, predicted 0 (top 3: 0 0.38, 4 0.21, 8 0.09)
11. true 5, predicted 8 (top 3: 8 0.41, 5 0.26, 3 0.19)
12. true 2, predicted 8 (top 3: 8 0.34, 3 0.15, 2 0.14)
13. true 6, predicted 1 (top 3: 1 0.51, 6 0.33, 9 0.04)
14. true 2, predicted 8 (top 3: 8 0.35, 2 0.33, 3 0.18)
15. true 4, predicted 9 (top 3: 9 0.32, 6 0.21, 4 0.18)
16. true 6, predicted 0 (top 3: 0 0.40, 5 0.27, 6 0.19)

[image: mistakes.png]
