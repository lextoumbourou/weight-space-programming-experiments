Step 42 of 50: training loss 0.7842, accuracy 0.7616.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   811    14    64     0     6     6    62     0    21     7
               1     0   983    23     2    41     4     0    11     0     0
               2    43     9   660   116    38    17     7    19    60    21
               3     6     1    35   778     0   132     0    13    53    12
               4    10    23    10     0   825     4    12     3    16    80
               5     4    11     3    77     7   560    54     9   190     0
               6    42    33     2     1    56    25   787     0    17     4
               7     6     2    22    15    15    15     0   918     7    90
               8    11    51   176    17    10    62    21     9   588    64
               9    24    12     4     6    74    61    11    28    35   706

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
41 | 0.7935 | 0.7540
42 | 0.7842 | 0.7616

At most 8 steps left. Reply with the complete build_weights() for step 43 in one Python code block.


Here are 16 training images your step 42 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 1, predicted 4 (top 3: 4 0.27, 1 0.23, 3 0.13)
2. true 6, predicted 4 (top 3: 4 0.38, 1 0.31, 6 0.12)
3. true 0, predicted 5 (top 3: 5 0.41, 6 0.22, 8 0.21)
4. true 8, predicted 5 (top 3: 5 0.35, 3 0.20, 8 0.19)
5. true 6, predicted 5 (top 3: 5 0.56, 6 0.27, 4 0.10)
6. true 6, predicted 0 (top 3: 0 0.34, 9 0.26, 4 0.25)
7. true 8, predicted 9 (top 3: 9 0.43, 8 0.40, 2 0.08)
8. true 3, predicted 5 (top 3: 5 0.80, 3 0.12, 8 0.06)
9. true 5, predicted 8 (top 3: 8 0.39, 5 0.26, 6 0.16)
10. true 8, predicted 9 (top 3: 9 0.55, 3 0.18, 8 0.13)
11. true 8, predicted 2 (top 3: 2 0.83, 9 0.04, 8 0.04)
12. true 7, predicted 9 (top 3: 9 0.50, 4 0.26, 5 0.16)
13. true 2, predicted 8 (top 3: 8 0.36, 2 0.36, 9 0.10)
14. true 9, predicted 5 (top 3: 5 0.40, 9 0.24, 3 0.23)
15. true 8, predicted 5 (top 3: 5 0.34, 3 0.22, 8 0.16)
16. true 8, predicted 2 (top 3: 2 0.62, 1 0.16, 8 0.13)

[image: mistakes.png]
