Step 28 of 50: training loss 0.8638, accuracy 0.7285.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   818    11    29     0     0     3    85     1    40     4
               1     0   994    39     8     4     4     1    13     1     0
               2    37    11   645   110    22    13    26    15   100    11
               3     7     3    23   703     0   204     0    12    68    10
               4     4    32     6     2   709     0    43     4    27   156
               5     6    13    12   128     0   514    59     8   175     0
               6    33    31     2     5    45    19   799     0    30     3
               7     8     7    22    16    44    20     0   895     5    73
               8     6    65   146    62     2    81    24    13   552    58
               9    22    19     1    11   109    53    13    43    34   656

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

At most 22 steps left. Reply with the complete build_weights() for step 29 in one Python code block.


Here are 16 training images your step 28 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 9 (top 3: 9 0.67, 8 0.14, 4 0.06)
2. true 9, predicted 7 (top 3: 7 0.37, 9 0.36, 3 0.08)
3. true 8, predicted 3 (top 3: 3 0.30, 8 0.24, 5 0.13)
4. true 1, predicted 2 (top 3: 2 0.92, 1 0.04, 8 0.02)
5. true 8, predicted 3 (top 3: 3 0.30, 8 0.24, 5 0.20)
6. true 0, predicted 6 (top 3: 6 0.34, 0 0.30, 8 0.17)
7. true 5, predicted 3 (top 3: 3 0.31, 8 0.28, 5 0.23)
8. true 5, predicted 3 (top 3: 3 0.49, 6 0.17, 8 0.14)
9. true 7, predicted 9 (top 3: 9 0.40, 7 0.30, 6 0.12)
10. true 4, predicted 6 (top 3: 6 0.42, 8 0.31, 4 0.12)
11. true 5, predicted 8 (top 3: 8 0.40, 6 0.21, 3 0.14)
12. true 4, predicted 9 (top 3: 9 0.33, 6 0.22, 8 0.22)
13. true 5, predicted 1 (top 3: 1 0.36, 6 0.23, 8 0.19)
14. true 9, predicted 5 (top 3: 5 0.35, 9 0.32, 8 0.11)
15. true 3, predicted 5 (top 3: 5 0.45, 3 0.30, 8 0.16)
16. true 9, predicted 8 (top 3: 8 0.72, 9 0.16, 6 0.10)

[image: mistakes.png]
