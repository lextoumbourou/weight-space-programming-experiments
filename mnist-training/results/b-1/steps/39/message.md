Step 38 of 50: training loss 0.8056, accuracy 0.7534.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   809    15    51     0     4     3    83     0    19     7
               1     0   976    20     1    49     4     0    14     0     0
               2    33     9   645   116    64     5    12    15    77    14
               3     6     3    22   739     0   180     0    11    56    13
               4     7    27     8     0   840     2    11     3    14    71
               5     5    13     4   110     9   547    52     9   166     0
               6    36    28     3     1    63    17   799     0    18     2
               7     7     7    21    10    36    19     0   883     7   100
               8     7    77   125    13    10    59    23     9   607    79
               9    19    13     2     4   129    41     8    32    24   689

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

At most 12 steps left. Reply with the complete build_weights() for step 39 in one Python code block.


Here are 16 training images your step 38 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 4 (top 3: 4 0.52, 9 0.41, 6 0.02)
2. true 5, predicted 3 (top 3: 3 0.49, 8 0.22, 5 0.14)
3. true 9, predicted 4 (top 3: 4 0.61, 9 0.34, 5 0.02)
4. true 5, predicted 3 (top 3: 3 0.38, 5 0.29, 8 0.28)
5. true 9, predicted 7 (top 3: 7 0.74, 1 0.12, 9 0.07)
6. true 5, predicted 8 (top 3: 8 0.34, 6 0.24, 1 0.14)
7. true 9, predicted 7 (top 3: 7 0.73, 9 0.20, 4 0.02)
8. true 7, predicted 9 (top 3: 9 0.52, 7 0.28, 4 0.09)
9. true 2, predicted 3 (top 3: 3 0.46, 9 0.15, 8 0.11)
10. true 2, predicted 1 (top 3: 1 0.85, 4 0.10, 2 0.02)
11. true 8, predicted 2 (top 3: 2 0.52, 8 0.31, 3 0.09)
12. true 6, predicted 4 (top 3: 4 0.24, 1 0.23, 6 0.21)
13. true 9, predicted 4 (top 3: 4 0.44, 9 0.24, 5 0.23)
14. true 5, predicted 8 (top 3: 8 0.41, 6 0.32, 3 0.11)
15. true 8, predicted 2 (top 3: 2 0.73, 8 0.22, 6 0.02)
16. true 8, predicted 5 (top 3: 5 0.49, 8 0.14, 6 0.12)

[image: mistakes.png]
