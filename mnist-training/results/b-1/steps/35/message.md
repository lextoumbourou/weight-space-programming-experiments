Step 34 of 50: training loss 0.8805, accuracy 0.7238.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   874    18    65     0     0     3    12     0    14     5
               1     0   996    17     1    27     5     1    17     0     0
               2    70    15   651   112    12    17    15    11    76    11
               3    15     4    31   691     0   200     0    21    48    20
               4    11    53    13     1   645     0    51     4    15   190
               5    12    16     5   105     0   574    60    13   130     0
               6    83    35     4     1    39    24   762     0    17     2
               7    14     6    25    14    29    19     0   923     5    55
               8    31   114   145    17     4    61    43    20   465   109
               9    43    15     5     3    70    68    13    55    32   657

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

At most 16 steps left. Reply with the complete build_weights() for step 35 in one Python code block.


Here are 16 training images your step 34 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 2 (top 3: 2 0.59, 3 0.20, 7 0.09)
2. true 6, predicted 0 (top 3: 0 0.34, 6 0.33, 5 0.13)
3. true 8, predicted 7 (top 3: 7 0.24, 8 0.23, 9 0.22)
4. true 6, predicted 1 (top 3: 1 0.41, 2 0.19, 6 0.17)
5. true 7, predicted 3 (top 3: 3 0.39, 9 0.23, 4 0.17)
6. true 5, predicted 7 (top 3: 7 0.46, 5 0.19, 9 0.13)
7. true 4, predicted 9 (top 3: 9 0.38, 8 0.30, 4 0.13)
8. true 8, predicted 9 (top 3: 9 0.28, 2 0.24, 3 0.20)
9. true 8, predicted 9 (top 3: 9 0.35, 7 0.17, 3 0.15)
10. true 4, predicted 1 (top 3: 1 0.94, 4 0.03, 6 0.01)
11. true 5, predicted 6 (top 3: 6 0.41, 8 0.38, 5 0.04)
12. true 7, predicted 0 (top 3: 0 0.69, 5 0.13, 7 0.09)
13. true 9, predicted 7 (top 3: 7 0.27, 9 0.17, 3 0.17)
14. true 8, predicted 1 (top 3: 1 0.77, 2 0.09, 6 0.07)
15. true 3, predicted 0 (top 3: 0 0.26, 5 0.25, 3 0.18)
16. true 9, predicted 8 (top 3: 8 0.52, 6 0.18, 9 0.15)

[image: mistakes.png]
