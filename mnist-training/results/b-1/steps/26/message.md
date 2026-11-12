Step 25 of 50: training loss 0.9104, accuracy 0.7289.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   812    12    26     0     0     3    95     1    38     4
               1     0   998    37     7     3     5     1    12     1     0
               2    37    11   632   117    19    11    30    14   107    12
               3     6     3    22   708     0   201     0    10    70    10
               4     5    34     5     1   699     0    50     4    28   157
               5     6    13    11   130     0   507    66     8   174     0
               6    26    31     1     5    40    19   816     0    26     3
               7     8     8    22    17    44    20     0   888     6    77
               8     6    70   132    65     2    74    27    12   562    59
               9    21    21     1    13   102    51    13    37    35   667

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

At most 25 steps left. Reply with the complete build_weights() for step 26 in one Python code block.


Here are 16 training images your step 25 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 8 (top 3: 8 0.57, 6 0.33, 3 0.05)
2. true 6, predicted 4 (top 3: 4 0.75, 6 0.20, 9 0.02)
3. true 6, predicted 0 (top 3: 0 0.85, 6 0.12, 5 0.02)
4. true 5, predicted 2 (top 3: 2 0.37, 8 0.36, 1 0.13)
5. true 8, predicted 5 (top 3: 5 0.80, 3 0.10, 8 0.07)
6. true 7, predicted 4 (top 3: 4 0.63, 5 0.16, 9 0.11)
7. true 0, predicted 1 (top 3: 1 0.88, 6 0.05, 8 0.03)
8. true 9, predicted 4 (top 3: 4 0.39, 9 0.34, 5 0.22)
9. true 8, predicted 9 (top 3: 9 0.53, 8 0.42, 2 0.03)
10. true 8, predicted 9 (top 3: 9 0.70, 8 0.16, 5 0.07)
11. true 8, predicted 2 (top 3: 2 0.90, 3 0.09, 8 0.01)
12. true 3, predicted 2 (top 3: 2 0.78, 3 0.21, 8 0.01)
13. true 4, predicted 9 (top 3: 9 0.46, 4 0.36, 8 0.09)
14. true 0, predicted 6 (top 3: 6 0.88, 0 0.04, 9 0.02)
15. true 5, predicted 8 (top 3: 8 0.34, 6 0.28, 5 0.25)
16. true 4, predicted 8 (top 3: 8 0.56, 9 0.36, 2 0.05)

[image: mistakes.png]
