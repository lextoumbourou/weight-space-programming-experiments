Step 39 of 50: training loss 0.7984, accuracy 0.7570.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   816    13    57     0     3     3    69     2    20     8
               1     0   974    22     2    44     4     0    18     0     0
               2    31     7   664   116    47     9     6    16    79    15
               3     6     1    24   735     0   182     0    15    54    13
               4     8    28    10     0   812     3    13     3    17    89
               5     5    13     4   110     7   550    51     9   166     0
               6    41    29     4     3    48    21   801     0    18     2
               7     8     4    22    10    28    18     0   907     6    87
               8     9    64   148    14     8    59    22    12   601    72
               9    20    12     3     4    98    45     8    37    24   710

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

At most 11 steps left. Reply with the complete build_weights() for step 40 in one Python code block.


Here are 16 training images your step 39 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 6 (top 3: 6 0.35, 8 0.31, 0 0.11)
2. true 8, predicted 3 (top 3: 3 0.50, 8 0.24, 5 0.17)
3. true 0, predicted 2 (top 3: 2 0.37, 9 0.29, 8 0.18)
4. true 6, predicted 1 (top 3: 1 0.94, 2 0.02, 6 0.01)
5. true 2, predicted 1 (top 3: 1 0.49, 2 0.43, 3 0.05)
6. true 3, predicted 8 (top 3: 8 0.64, 9 0.12, 2 0.09)
7. true 2, predicted 3 (top 3: 3 0.52, 4 0.17, 2 0.16)
8. true 2, predicted 3 (top 3: 3 0.43, 2 0.17, 9 0.13)
9. true 9, predicted 4 (top 3: 4 0.56, 9 0.37, 8 0.02)
10. true 8, predicted 5 (top 3: 5 0.46, 3 0.33, 8 0.12)
11. true 1, predicted 4 (top 3: 4 0.46, 5 0.17, 9 0.12)
12. true 4, predicted 8 (top 3: 8 0.32, 4 0.21, 9 0.18)
13. true 5, predicted 3 (top 3: 3 0.59, 8 0.21, 2 0.07)
14. true 8, predicted 6 (top 3: 6 0.43, 2 0.25, 8 0.18)
15. true 6, predicted 4 (top 3: 4 0.20, 3 0.17, 8 0.16)
16. true 3, predicted 7 (top 3: 7 0.67, 3 0.25, 9 0.02)

[image: mistakes.png]
