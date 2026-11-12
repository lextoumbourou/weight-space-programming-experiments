Step 20 of 50: training loss 1.0582, accuracy 0.6870.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   766     7    16     3     0     3    62     1   127     6
               1     0   957    74    18     0     5     2     6     2     0
               2    30    10   638   107    19     8    49     8   112     9
               3     5     5    38   691     2   169     0     6   106     8
               4     4    22     7     6   643     1    44     3    67   186
               5     4    13    19   136     2   408    61     4   266     2
               6    23    31     2    19    53     7   809     0    19     4
               7     9    12    35    38    24    36     0   778    19   139
               8     6    63   161   141     1    62    11     7   488    69
               9    20    22     0    21    88    29     5    35    49   692

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

At most 30 steps left. Reply with the complete build_weights() for step 21 in one Python code block.


Here are 16 training images your step 20 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 2 (top 3: 2 0.50, 3 0.21, 8 0.15)
2. true 9, predicted 8 (top 3: 8 0.38, 9 0.35, 6 0.13)
3. true 5, predicted 8 (top 3: 8 0.62, 5 0.17, 3 0.12)
4. true 5, predicted 3 (top 3: 3 0.47, 8 0.45, 2 0.05)
5. true 2, predicted 5 (top 3: 5 0.32, 6 0.29, 3 0.26)
6. true 8, predicted 3 (top 3: 3 0.33, 8 0.24, 2 0.21)
7. true 9, predicted 7 (top 3: 7 0.45, 3 0.24, 9 0.14)
8. true 3, predicted 8 (top 3: 8 0.71, 9 0.09, 5 0.08)
9. true 9, predicted 4 (top 3: 4 0.44, 8 0.30, 5 0.11)
10. true 9, predicted 8 (top 3: 8 0.56, 3 0.25, 9 0.09)
11. true 8, predicted 3 (top 3: 3 0.54, 8 0.35, 6 0.06)
12. true 7, predicted 9 (top 3: 9 0.38, 8 0.28, 4 0.18)
13. true 6, predicted 4 (top 3: 4 0.69, 6 0.22, 9 0.04)
14. true 5, predicted 8 (top 3: 8 0.39, 5 0.37, 6 0.11)
15. true 8, predicted 3 (top 3: 3 0.39, 8 0.28, 5 0.15)
16. true 8, predicted 2 (top 3: 2 0.96, 8 0.03, 3 0.01)

[image: mistakes.png]
