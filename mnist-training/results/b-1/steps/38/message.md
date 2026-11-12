Step 37 of 50: training loss 0.8217, accuracy 0.7448.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   803    14    39     0     8     3    93     0    26     5
               1     0   974    16     1    60     3     0    10     0     0
               2    36    12   603   103    98     4     7    16   103     8
               3     6     3    16   728     0   173     0    11    81    12
               4     6    26     4     0   878     2     8     2    17    40
               5     4    13     3    86    10   521    52     8   218     0
               6    31    30     1     1    76    16   789     0    22     1
               7     8     8    20     9    47    17     0   877     9    95
               8     8    83    92    12    15    44    21     9   668    57
               9    20    14     2     4   204    41     8    28    33   607

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

At most 13 steps left. Reply with the complete build_weights() for step 38 in one Python code block.


Here are 16 training images your step 37 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 9 (top 3: 9 0.49, 8 0.17, 7 0.14)
2. true 9, predicted 4 (top 3: 4 0.42, 9 0.31, 0 0.10)
3. true 3, predicted 5 (top 3: 5 0.60, 3 0.25, 8 0.12)
4. true 9, predicted 2 (top 3: 2 0.40, 8 0.32, 6 0.15)
5. true 8, predicted 2 (top 3: 2 0.44, 8 0.33, 6 0.13)
6. true 0, predicted 2 (top 3: 2 0.78, 6 0.09, 1 0.04)
7. true 2, predicted 9 (top 3: 9 0.34, 4 0.14, 0 0.10)
8. true 3, predicted 5 (top 3: 5 0.46, 3 0.19, 8 0.18)
9. true 3, predicted 5 (top 3: 5 0.42, 3 0.25, 8 0.21)
10. true 0, predicted 1 (top 3: 1 0.31, 4 0.22, 6 0.14)
11. true 8, predicted 2 (top 3: 2 0.28, 8 0.21, 3 0.15)
12. true 9, predicted 4 (top 3: 4 0.66, 9 0.29, 7 0.02)
13. true 2, predicted 8 (top 3: 8 0.34, 4 0.28, 6 0.15)
14. true 3, predicted 9 (top 3: 9 0.35, 8 0.33, 3 0.17)
15. true 3, predicted 8 (top 3: 8 0.50, 2 0.37, 3 0.09)
16. true 9, predicted 5 (top 3: 5 0.23, 9 0.21, 8 0.18)

[image: mistakes.png]
