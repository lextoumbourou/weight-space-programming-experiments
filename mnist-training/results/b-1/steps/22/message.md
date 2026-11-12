Step 21 of 50: training loss 1.0690, accuracy 0.7032.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   769     9    11     0     0     1    87     0   105     9
               1     0   965    75     9     0     5     2     5     2     1
               2    31    11   625    92     4     4    49     7   153    14
               3     6     5    28   680     0   140     0     6   152    13
               4     4    25     7     2   564     1    49     1    74   256
               5     4    11    13   129     0   394    67     4   291     2
               6    23    27     1    11    27     4   845     0    26     3
               7     7    11    32    31    15    33     0   763    21   177
               8     4    52   103    54     1    35    15     5   643    97
               9    17    18     0    11    30    19    10    24    48   784

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

At most 29 steps left. Reply with the complete build_weights() for step 22 in one Python code block.


Here are 16 training images your step 21 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 8 (top 3: 8 0.68, 0 0.16, 5 0.08)
2. true 0, predicted 8 (top 3: 8 0.61, 6 0.32, 0 0.06)
3. true 9, predicted 8 (top 3: 8 0.72, 6 0.25, 9 0.02)
4. true 5, predicted 8 (top 3: 8 0.51, 6 0.38, 9 0.06)
5. true 8, predicted 2 (top 3: 2 0.62, 8 0.23, 3 0.14)
6. true 2, predicted 3 (top 3: 3 0.82, 6 0.04, 5 0.04)
7. true 4, predicted 9 (top 3: 9 0.52, 8 0.24, 4 0.17)
8. true 2, predicted 6 (top 3: 6 0.47, 8 0.44, 4 0.05)
9. true 8, predicted 9 (top 3: 9 0.38, 7 0.28, 3 0.26)
10. true 3, predicted 8 (top 3: 8 0.76, 3 0.23, 5 0.01)
11. true 0, predicted 6 (top 3: 6 0.46, 8 0.45, 0 0.05)
12. true 1, predicted 2 (top 3: 2 0.91, 1 0.08, 8 0.01)
13. true 0, predicted 2 (top 3: 2 0.58, 3 0.17, 8 0.15)
14. true 2, predicted 0 (top 3: 0 0.71, 7 0.23, 9 0.04)
15. true 3, predicted 8 (top 3: 8 0.59, 3 0.37, 9 0.03)
16. true 5, predicted 3 (top 3: 3 0.57, 8 0.26, 7 0.12)

[image: mistakes.png]
