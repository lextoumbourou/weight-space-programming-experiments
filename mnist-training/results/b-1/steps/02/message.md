Step 1 of 50: training loss 1.4479, accuracy 0.5465.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   765    17    14     0     1     1    72     1   119     1
               1     0  1049     2     2     0     4     4     3     0     0
               2    17    72   519    60    51     1   106    19   144     1
               3     4    60    58   408     7   331    22    44    84    12
               4     3   168     9     0   635     0    48    12    14    94
               5     8   206    12    28     9   391   222     3    28     8
               6    11   108     4     0   148     1   675     0    20     0
               7    18   128   161     4    38    43     6   406     4   282
               8     4   246   275    10     6    30    46    45   303    44
               9    25   206    24     1   231    39    36    39    46   314

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465

At most 49 steps left. Reply with the complete build_weights() for step 2 in one Python code block.


Here are 16 training images your step 1 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 1 (top 3: 1 0.19, 6 0.15, 4 0.14)
2. true 6, predicted 4 (top 3: 4 0.28, 6 0.21, 8 0.14)
3. true 4, predicted 1 (top 3: 1 0.32, 4 0.21, 6 0.12)
4. true 5, predicted 6 (top 3: 6 0.42, 8 0.15, 5 0.11)
5. true 0, predicted 1 (top 3: 1 0.25, 2 0.21, 7 0.20)
6. true 9, predicted 4 (top 3: 4 0.39, 9 0.16, 2 0.08)
7. true 3, predicted 8 (top 3: 8 0.25, 5 0.24, 3 0.22)
8. true 7, predicted 2 (top 3: 2 0.36, 7 0.15, 3 0.14)
9. true 4, predicted 1 (top 3: 1 0.30, 9 0.17, 5 0.17)
10. true 8, predicted 7 (top 3: 7 0.27, 1 0.20, 2 0.19)
11. true 0, predicted 8 (top 3: 8 0.30, 6 0.25, 4 0.11)
12. true 8, predicted 2 (top 3: 2 0.38, 8 0.13, 3 0.12)
13. true 2, predicted 8 (top 3: 8 0.20, 2 0.17, 0 0.16)
14. true 3, predicted 5 (top 3: 5 0.15, 3 0.14, 1 0.13)
15. true 7, predicted 9 (top 3: 9 0.43, 5 0.12, 2 0.10)
16. true 2, predicted 8 (top 3: 8 0.31, 2 0.20, 6 0.12)

[image: mistakes.png]
