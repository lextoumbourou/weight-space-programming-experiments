Step 1 of 50: training loss 1.6349, accuracy 0.3786.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   538     0    26     5     0     9   218     0   195     0
               1    16   717    60     0     0     0    68   181    16     6
               2     0     2   170    55     0     0    23     3   726    11
               3     1     0     2    98     0     5     0     1   918     5
               4    16     1     3     0    15     0    77     6   748   117
               5     2     0     0     4     0    87    52     7   761     2
               6    10     0     1     0     0     1   750     0   205     0
               7     6     2   117    19     0     7     6   330   244   359
               8     5     3     5     0     0     0    70    14   906     6
               9    31     1    13     1     0     1    51    16   672   175

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786

At most 49 steps left. Reply with the complete build_weights() for step 2 in one Python code block.


Here are 16 training images your step 1 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 8 (top 3: 8 0.56, 9 0.24, 4 0.08)
2. true 7, predicted 9 (top 3: 9 0.70, 8 0.14, 3 0.09)
3. true 6, predicted 8 (top 3: 8 0.72, 5 0.16, 6 0.08)
4. true 3, predicted 8 (top 3: 8 0.67, 6 0.13, 3 0.11)
5. true 5, predicted 8 (top 3: 8 0.48, 6 0.27, 0 0.10)
6. true 6, predicted 8 (top 3: 8 0.40, 3 0.29, 6 0.21)
7. true 0, predicted 8 (top 3: 8 0.38, 6 0.37, 2 0.13)
8. true 6, predicted 8 (top 3: 8 0.39, 0 0.27, 6 0.22)
9. true 4, predicted 8 (top 3: 8 0.47, 6 0.21, 2 0.19)
10. true 2, predicted 8 (top 3: 8 0.64, 3 0.10, 5 0.09)
11. true 4, predicted 8 (top 3: 8 0.43, 6 0.26, 7 0.10)
12. true 2, predicted 8 (top 3: 8 0.59, 3 0.25, 2 0.06)
13. true 5, predicted 8 (top 3: 8 0.40, 6 0.28, 7 0.09)
14. true 0, predicted 6 (top 3: 6 0.53, 0 0.30, 8 0.13)
15. true 5, predicted 8 (top 3: 8 0.38, 5 0.32, 3 0.09)
16. true 9, predicted 8 (top 3: 8 0.41, 9 0.24, 0 0.11)

[image: mistakes.png]
