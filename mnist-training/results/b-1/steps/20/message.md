Step 19 of 50: training loss 1.0859, accuracy 0.6762.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   767     7    18     3     0     5    60     1   124     6
               1     0   957    74    18     0     5     2     6     2     0
               2    29    10   645   117    20     8    47     8    98     8
               3     5     5    37   713     2   175     0     6    83     4
               4     4    24     7     7   658     1    43     3    56   180
               5     4    14    20   137     2   413    60     4   259     2
               6    23    36     3    32    62     9   786     0    13     3
               7     9    12    35    38    24    36     0   788    18   130
               8     6    72   185   217     1    73    12    10   371    62
               9    20    25     1    37    94    35     7    43    35   664

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

At most 31 steps left. Reply with the complete build_weights() for step 20 in one Python code block.


Here are 16 training images your step 19 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 6 (top 3: 6 0.45, 0 0.27, 8 0.19)
2. true 8, predicted 9 (top 3: 9 0.70, 3 0.17, 5 0.05)
3. true 7, predicted 1 (top 3: 1 0.33, 3 0.32, 8 0.18)
4. true 5, predicted 1 (top 3: 1 0.61, 3 0.17, 8 0.09)
5. true 9, predicted 4 (top 3: 4 0.52, 9 0.42, 5 0.02)
6. true 0, predicted 6 (top 3: 6 0.35, 0 0.31, 8 0.14)
7. true 5, predicted 6 (top 3: 6 0.36, 9 0.33, 8 0.20)
8. true 7, predicted 2 (top 3: 2 0.86, 9 0.05, 8 0.03)
9. true 8, predicted 3 (top 3: 3 0.44, 8 0.40, 2 0.08)
10. true 8, predicted 2 (top 3: 2 0.85, 8 0.06, 1 0.04)
11. true 9, predicted 4 (top 3: 4 0.50, 9 0.34, 6 0.11)
12. true 9, predicted 3 (top 3: 3 0.45, 9 0.18, 7 0.14)
13. true 8, predicted 3 (top 3: 3 0.57, 1 0.26, 2 0.09)
14. true 7, predicted 9 (top 3: 9 0.61, 7 0.22, 5 0.06)
15. true 6, predicted 4 (top 3: 4 0.45, 6 0.27, 9 0.14)
16. true 5, predicted 8 (top 3: 8 0.51, 3 0.20, 6 0.20)

[image: mistakes.png]
