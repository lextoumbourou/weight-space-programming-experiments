Step 4 of 50: training loss 1.6386, accuracy 0.5078.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   705     1     1     0     1     0   115     0   168     0
               1     0   956     3     0     0     3     9    87     6     0
               2    23    20   294    45    40     0   111    28   428     1
               3     1    14    16   314     4   134    21    31   478    17
               4     1    26     8     0   598     1    63    14   157   115
               5     7    94     3     3    18   186   386     1   196    21
               6    10    25     5     0    72     1   745     0   109     0
               7    16    24   414     4    54    11     5   206    50   306
               8     2    41    86     0     4     3    25    43   777    28
               9    11    32    18     0   287     3    37    37   239   297

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.


Here are 16 training images your step 4 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 8 (top 3: 8 0.53, 6 0.16, 5 0.16)
2. true 8, predicted 2 (top 3: 2 0.46, 8 0.36, 7 0.08)
3. true 0, predicted 8 (top 3: 8 0.75, 6 0.19, 2 0.02)
4. true 7, predicted 2 (top 3: 2 0.47, 9 0.23, 7 0.22)
5. true 2, predicted 8 (top 3: 8 0.70, 2 0.17, 6 0.03)
6. true 7, predicted 8 (top 3: 8 0.40, 2 0.26, 6 0.17)
7. true 3, predicted 8 (top 3: 8 0.52, 6 0.33, 2 0.05)
8. true 2, predicted 8 (top 3: 8 0.50, 6 0.27, 2 0.10)
9. true 5, predicted 6 (top 3: 6 0.71, 8 0.23, 2 0.02)
10. true 5, predicted 8 (top 3: 8 0.39, 6 0.26, 2 0.12)
11. true 0, predicted 8 (top 3: 8 0.91, 6 0.06, 4 0.02)
12. true 2, predicted 8 (top 3: 8 0.37, 2 0.21, 4 0.18)
13. true 2, predicted 8 (top 3: 8 0.77, 6 0.10, 2 0.04)
14. true 7, predicted 9 (top 3: 9 0.58, 2 0.17, 4 0.07)
15. true 7, predicted 9 (top 3: 9 0.38, 8 0.18, 2 0.15)
16. true 7, predicted 9 (top 3: 9 0.53, 5 0.15, 2 0.10)

[image: mistakes.png]
