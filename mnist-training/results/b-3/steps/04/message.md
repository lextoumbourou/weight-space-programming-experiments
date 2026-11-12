Step 3 of 50: training loss 2.0915, accuracy 0.5810.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   886     0    50     8     0    17    18     2    10     0
               1     0   839    52     1     0     5     4   163     0     0
               2    24     7   502   211     0    28    68     7   143     0
               3     2     1     4   882     0    86     7     6    41     1
               4    25    62    40    29    37    42   193   109   179   267
               5     4     4     4   212     0   503    97     5    86     0
               6    59     4     1    20     0    38   807     1    37     0
               7    21     5    57    84     0    69     1   684    21   148
               8     4    20    69    42     0    20   234    89   513    18
               9    69    20    19    16     0   141    80   113   346   157

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.


Here are 16 training images your step 3 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 9 (top 3: 9 0.58, 4 0.18, 5 0.17)
2. true 4, predicted 5 (top 3: 5 0.94, 6 0.04, 3 0.02)
3. true 8, predicted 6 (top 3: 6 0.81, 8 0.18, 3 0.01)
4. true 4, predicted 9 (top 3: 9 0.48, 7 0.39, 3 0.09)
5. true 2, predicted 3 (top 3: 3 0.82, 2 0.15, 8 0.03)
6. true 9, predicted 8 (top 3: 8 0.47, 2 0.26, 3 0.12)
7. true 9, predicted 8 (top 3: 8 0.50, 3 0.36, 5 0.13)
8. true 8, predicted 1 (top 3: 1 0.61, 6 0.28, 7 0.10)
9. true 8, predicted 6 (top 3: 6 0.84, 7 0.13, 8 0.02)
10. true 9, predicted 6 (top 3: 6 0.33, 7 0.26, 1 0.19)
11. true 4, predicted 9 (top 3: 9 0.54, 8 0.42, 7 0.03)
12. true 9, predicted 3 (top 3: 3 0.67, 5 0.21, 9 0.10)
13. true 2, predicted 3 (top 3: 3 0.90, 8 0.04, 2 0.02)
14. true 7, predicted 3 (top 3: 3 0.92, 7 0.04, 5 0.03)
15. true 7, predicted 3 (top 3: 3 0.65, 7 0.28, 5 0.02)
16. true 7, predicted 9 (top 3: 9 0.53, 7 0.32, 0 0.13)

[image: mistakes.png]
