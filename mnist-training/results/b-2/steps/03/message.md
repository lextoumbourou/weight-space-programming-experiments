Step 2 of 50: training loss 1.6757, accuracy 0.5669.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   687     9   209     5     0    19    59     3     0     0
               1     4   889    20     0     2     0     0   149     0     0
               2    12    82   681    72    48     5    16    31     9    34
               3     7    29   110   523    15    67    22   127    14   116
               4    11   208    60     0   311     0    26   117     4   246
               5    14    18    24    27     4   517   160   133     4    14
               6    57    16    11     4     1    18   859     1     0     0
               7     5    51   102     3     4     7     0   710     0   208
               8    50   103   113    17     2     9    98   458    60    99
               9    66    35    88     9    29     3    20   279     0   432

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.


Here are 16 training images your step 2 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 9 (top 3: 9 0.60, 1 0.39, 4 0.01)
2. true 4, predicted 1 (top 3: 1 0.80, 0 0.12, 4 0.06)
3. true 7, predicted 9 (top 3: 9 0.63, 4 0.08, 3 0.08)
4. true 8, predicted 7 (top 3: 7 0.69, 6 0.28, 2 0.02)
5. true 8, predicted 1 (top 3: 1 0.90, 7 0.06, 6 0.03)
6. true 4, predicted 1 (top 3: 1 0.56, 4 0.20, 7 0.13)
7. true 0, predicted 2 (top 3: 2 0.85, 6 0.12, 0 0.02)
8. true 1, predicted 7 (top 3: 7 0.70, 2 0.29, 1 0.01)
9. true 8, predicted 6 (top 3: 6 0.38, 0 0.29, 1 0.17)
10. true 3, predicted 6 (top 3: 6 0.52, 4 0.27, 3 0.06)
11. true 7, predicted 1 (top 3: 1 0.53, 7 0.30, 2 0.10)
12. true 9, predicted 0 (top 3: 0 0.77, 9 0.19, 4 0.02)
13. true 3, predicted 7 (top 3: 7 0.78, 9 0.09, 3 0.07)
14. true 9, predicted 7 (top 3: 7 0.65, 2 0.34, 6 0.01)
15. true 3, predicted 2 (top 3: 2 0.57, 3 0.30, 9 0.09)
16. true 9, predicted 7 (top 3: 7 0.60, 2 0.29, 9 0.06)

[image: mistakes.png]
