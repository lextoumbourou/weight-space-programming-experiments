Step 35 of 50: training loss 0.8682, accuracy 0.7310.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   729    13    14     0     0     2   198     0    28     7
               1     0  1005    13     7     9     6     1    23     0     0
               2    21    19   591   127    11     3    28    19   150    21
               3     5     3    11   743     0   144     0    10   105     9
               4     2    42     6     1   647     0    33     3    35   214
               5     2    16     3   101     3   480    73     8   228     1
               6    20    34     0     2    28     9   857     0    13     4
               7     6    11    14     8    28    15     0   884     8   116
               8     4   116    92    27     3    36    29    10   610    82
               9    13    20     2     6    52    32    13    30    29   764

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

At most 15 steps left. Reply with the complete build_weights() for step 36 in one Python code block.


Here are 16 training images your step 35 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 3 (top 3: 3 0.69, 4 0.12, 8 0.10)
2. true 6, predicted 0 (top 3: 0 0.96, 4 0.02, 9 0.01)
3. true 9, predicted 4 (top 3: 4 0.55, 9 0.23, 8 0.09)
4. true 6, predicted 1 (top 3: 1 0.40, 6 0.25, 3 0.18)
5. true 5, predicted 3 (top 3: 3 0.25, 1 0.23, 8 0.15)
6. true 7, predicted 9 (top 3: 9 0.55, 7 0.31, 6 0.06)
7. true 2, predicted 8 (top 3: 8 0.46, 2 0.21, 9 0.18)
8. true 1, predicted 7 (top 3: 7 0.34, 5 0.16, 3 0.15)
9. true 8, predicted 9 (top 3: 9 0.58, 8 0.30, 6 0.08)
10. true 3, predicted 5 (top 3: 5 0.42, 3 0.38, 8 0.15)
11. true 3, predicted 5 (top 3: 5 0.63, 8 0.25, 3 0.04)
12. true 6, predicted 0 (top 3: 0 0.58, 6 0.31, 4 0.03)
13. true 5, predicted 3 (top 3: 3 0.53, 8 0.32, 5 0.07)
14. true 8, predicted 6 (top 3: 6 0.32, 8 0.24, 5 0.18)
15. true 9, predicted 4 (top 3: 4 0.49, 5 0.23, 9 0.14)
16. true 8, predicted 2 (top 3: 2 0.76, 8 0.10, 6 0.06)

[image: mistakes.png]
