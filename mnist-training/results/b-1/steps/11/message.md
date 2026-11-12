Step 10 of 50: training loss 1.5771, accuracy 0.5330.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   927    10     9     0     0     0    42     2     1     0
               1     0   963     5     0     0     6     5    64    21     0
               2   101    42   562     2    21     3   218    12    29     0
               3    77    27   103   277     1   268    22   123   127     5
               4    14    38     7     0   606     0   159     9   113    37
               5    60    42    12     1     2   349   259    18   170     2
               6    84    30     0     0    79     3   744     0    27     0
               7    55    52   222     3    21    23     1   349    12   352
               8    92   101   254     0     4    32    96    88   335     7
               9   115    65    34     0   197    37    38    90   167   218

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

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.


Here are 16 training images your step 10 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 5 (top 3: 5 0.78, 8 0.11, 6 0.05)
2. true 6, predicted 0 (top 3: 0 0.52, 6 0.20, 4 0.12)
3. true 7, predicted 3 (top 3: 3 0.31, 5 0.25, 9 0.13)
4. true 9, predicted 4 (top 3: 4 0.39, 0 0.38, 6 0.18)
5. true 5, predicted 1 (top 3: 1 0.67, 7 0.14, 8 0.12)
6. true 9, predicted 2 (top 3: 2 0.17, 7 0.17, 9 0.17)
7. true 3, predicted 0 (top 3: 0 0.46, 6 0.27, 5 0.07)
8. true 5, predicted 8 (top 3: 8 0.57, 1 0.21, 2 0.10)
9. true 9, predicted 4 (top 3: 4 0.49, 0 0.36, 9 0.10)
10. true 8, predicted 2 (top 3: 2 0.36, 8 0.25, 0 0.11)
11. true 4, predicted 7 (top 3: 7 0.36, 1 0.27, 8 0.19)
12. true 7, predicted 9 (top 3: 9 0.56, 5 0.30, 4 0.06)
13. true 3, predicted 7 (top 3: 7 0.43, 2 0.31, 3 0.11)
14. true 9, predicted 1 (top 3: 1 0.44, 7 0.26, 8 0.21)
15. true 7, predicted 2 (top 3: 2 0.54, 7 0.33, 1 0.06)
16. true 8, predicted 2 (top 3: 2 0.69, 6 0.13, 0 0.10)

[image: mistakes.png]
