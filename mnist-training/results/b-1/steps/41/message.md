Step 40 of 50: training loss 0.7887, accuracy 0.7604.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   810    14    59     0     9     4    59     0    26    10
               1     0   979    22     2    48     4     0     9     0     0
               2    43     9   654   115    48    13     5    17    64    22
               3     7     1    35   790     0   116     0    11    58    12
               4     8    23    10     0   847     2     9     1    14    69
               5     3    12     3    74     9   542    47     9   216     0
               6    41    38     2     2    67    25   763     0    24     5
               7     7     2    23    20    15    13     0   891     8   111
               8    12    54   162    14    13    47    16     7   613    71
               9    23    12     4     6    87    45     6    24    39   715

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
34 | 0.8805 | 0.7238
35 | 0.8682 | 0.7310
36 | 0.8409 | 0.7319
37 | 0.8217 | 0.7448
38 | 0.8056 | 0.7534
39 | 0.7984 | 0.7570
40 | 0.7887 | 0.7604

At most 10 steps left. Reply with the complete build_weights() for step 41 in one Python code block.


Here are 16 training images your step 40 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 1 (top 3: 1 0.77, 4 0.14, 6 0.03)
2. true 7, predicted 1 (top 3: 1 0.85, 2 0.10, 7 0.04)
3. true 7, predicted 9 (top 3: 9 0.49, 7 0.20, 5 0.11)
4. true 2, predicted 3 (top 3: 3 0.36, 5 0.36, 8 0.16)
5. true 5, predicted 7 (top 3: 7 0.31, 9 0.28, 5 0.16)
6. true 4, predicted 1 (top 3: 1 0.56, 2 0.20, 4 0.10)
7. true 9, predicted 5 (top 3: 5 0.37, 9 0.22, 8 0.17)
8. true 6, predicted 4 (top 3: 4 0.42, 6 0.22, 1 0.14)
9. true 8, predicted 5 (top 3: 5 0.34, 8 0.17, 3 0.15)
10. true 3, predicted 5 (top 3: 5 0.42, 3 0.42, 8 0.10)
11. true 3, predicted 5 (top 3: 5 0.54, 3 0.39, 8 0.06)
12. true 8, predicted 2 (top 3: 2 0.36, 9 0.18, 8 0.12)
13. true 8, predicted 5 (top 3: 5 0.30, 8 0.21, 9 0.18)
14. true 5, predicted 8 (top 3: 8 0.35, 3 0.26, 5 0.18)
15. true 8, predicted 6 (top 3: 6 0.45, 8 0.32, 4 0.05)
16. true 8, predicted 5 (top 3: 5 0.39, 8 0.28, 6 0.14)

[image: mistakes.png]
