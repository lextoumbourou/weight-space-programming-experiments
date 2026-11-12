Step 30 of 50: training loss 0.8570, accuracy 0.7372.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   814    15    32     0     0     3    93     0    30     4
               1     0  1001    13     7    10     6     1    26     0     0
               2    40    16   633   120    12    10    24    15   108    12
               3     6     3    18   732     0   185     0    10    67     9
               4     4    46     7     1   677     0    37     4    28   179
               5     6    19     5   111     0   520    59     8   187     0
               6    30    34     0     3    35    16   831     0    17     1
               7     8    10    18    15    33    16     0   899     7    84
               8     7   116   122    38     4    59    23    11   556    73
               9    21    19     2     8    72    47    12    41    30   709

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

At most 20 steps left. Reply with the complete build_weights() for step 31 in one Python code block.


Here are 16 training images your step 30 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 9 (top 3: 9 0.36, 8 0.32, 4 0.13)
2. true 3, predicted 5 (top 3: 5 0.78, 8 0.15, 3 0.03)
3. true 7, predicted 9 (top 3: 9 0.60, 7 0.23, 6 0.07)
4. true 5, predicted 8 (top 3: 8 0.55, 3 0.24, 6 0.09)
5. true 5, predicted 3 (top 3: 3 0.37, 8 0.35, 5 0.15)
6. true 0, predicted 8 (top 3: 8 0.37, 6 0.34, 1 0.12)
7. true 8, predicted 0 (top 3: 0 0.41, 5 0.20, 4 0.15)
8. true 6, predicted 1 (top 3: 1 0.79, 6 0.12, 2 0.05)
9. true 6, predicted 1 (top 3: 1 0.41, 6 0.30, 8 0.15)
10. true 4, predicted 9 (top 3: 9 0.45, 4 0.22, 6 0.11)
11. true 8, predicted 2 (top 3: 2 0.57, 8 0.34, 9 0.03)
12. true 8, predicted 2 (top 3: 2 0.52, 1 0.36, 8 0.04)
13. true 2, predicted 3 (top 3: 3 0.38, 8 0.22, 4 0.18)
14. true 8, predicted 1 (top 3: 1 0.33, 3 0.25, 7 0.20)
15. true 0, predicted 8 (top 3: 8 0.36, 6 0.25, 0 0.13)
16. true 0, predicted 6 (top 3: 6 0.42, 0 0.12, 8 0.11)

[image: mistakes.png]
