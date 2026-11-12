Step 29 of 50: training loss 0.8738, accuracy 0.7332.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   804    17    25     0     0     3   110     0    27     5
               1     0  1007    10     8     8     6     1    24     0     0
               2    40    18   619   125    11     8    30    15   111    13
               3     6     3    16   743     0   177     0    10    65    10
               4     4    49     5     1   636     0    47     3    24   214
               5     6    19     5   114     0   513    65     8   185     0
               6    29    35     0     2    31    14   839     0    16     1
               7     8    12    17    17    31    16     0   881     7   101
               8     7   133    99    42     4    54    25    10   551    84
               9    22    20     2     7    58    40    11    35    27   739

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

At most 21 steps left. Reply with the complete build_weights() for step 30 in one Python code block.


Here are 16 training images your step 29 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 7 (top 3: 7 0.72, 9 0.11, 3 0.08)
2. true 0, predicted 6 (top 3: 6 0.70, 0 0.13, 8 0.08)
3. true 8, predicted 3 (top 3: 3 0.34, 9 0.33, 8 0.13)
4. true 5, predicted 6 (top 3: 6 0.78, 3 0.07, 1 0.05)
5. true 9, predicted 1 (top 3: 1 0.71, 7 0.12, 9 0.07)
6. true 5, predicted 6 (top 3: 6 0.48, 8 0.31, 5 0.11)
7. true 8, predicted 1 (top 3: 1 0.65, 2 0.19, 8 0.06)
8. true 8, predicted 4 (top 3: 4 0.92, 3 0.04, 5 0.02)
9. true 7, predicted 4 (top 3: 4 0.44, 5 0.20, 9 0.20)
10. true 8, predicted 2 (top 3: 2 0.84, 1 0.10, 8 0.03)
11. true 2, predicted 8 (top 3: 8 0.54, 3 0.22, 4 0.11)
12. true 8, predicted 9 (top 3: 9 0.80, 8 0.08, 3 0.04)
13. true 3, predicted 8 (top 3: 8 0.59, 3 0.26, 6 0.06)
14. true 3, predicted 5 (top 3: 5 0.48, 3 0.40, 8 0.10)
15. true 6, predicted 5 (top 3: 5 0.48, 6 0.25, 0 0.21)
16. true 1, predicted 7 (top 3: 7 0.47, 3 0.25, 4 0.08)

[image: mistakes.png]
