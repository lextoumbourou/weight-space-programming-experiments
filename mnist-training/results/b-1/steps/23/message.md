Step 22 of 50: training loss 1.0120, accuracy 0.7094.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   793     8    14     1     0     3    88     2    74     8
               1     0   961    78    10     0     5     2     6     1     1
               2    33    11   645   107    10    11    45    10   108    10
               3     6     5    30   691     1   183     0    11    94     9
               4     3    25     8     2   669     1    53     2    52   168
               5     4    10    17   146     0   447    69     4   216     2
               6    24    28     2    11    41    10   831     0    18     2
               7     7     6    31    32    25    41     0   809    16   123
               8     6    54   147    73     1    66    25    10   546    81
               9    23    20     1    12    89    34     9    35    36   702

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

At most 28 steps left. Reply with the complete build_weights() for step 23 in one Python code block.


Here are 16 training images your step 22 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 1 (top 3: 1 0.85, 3 0.13, 7 0.01)
2. true 7, predicted 5 (top 3: 5 0.84, 0 0.14, 9 0.01)
3. true 7, predicted 9 (top 3: 9 0.50, 8 0.28, 7 0.22)
4. true 4, predicted 9 (top 3: 9 0.57, 7 0.21, 3 0.11)
5. true 5, predicted 3 (top 3: 3 0.47, 5 0.37, 8 0.15)
6. true 8, predicted 9 (top 3: 9 0.31, 8 0.21, 3 0.18)
7. true 5, predicted 6 (top 3: 6 0.55, 3 0.29, 5 0.13)
8. true 9, predicted 1 (top 3: 1 0.60, 3 0.17, 7 0.16)
9. true 7, predicted 5 (top 3: 5 0.64, 7 0.24, 9 0.08)
10. true 3, predicted 5 (top 3: 5 0.97, 8 0.01, 3 0.01)
11. true 2, predicted 8 (top 3: 8 0.59, 3 0.23, 6 0.16)
12. true 5, predicted 3 (top 3: 3 0.52, 5 0.21, 9 0.14)
13. true 5, predicted 8 (top 3: 8 0.63, 3 0.20, 6 0.11)
14. true 9, predicted 5 (top 3: 5 0.58, 8 0.32, 3 0.05)
15. true 9, predicted 5 (top 3: 5 0.50, 4 0.32, 9 0.15)
16. true 9, predicted 3 (top 3: 3 0.46, 8 0.19, 7 0.18)

[image: mistakes.png]
