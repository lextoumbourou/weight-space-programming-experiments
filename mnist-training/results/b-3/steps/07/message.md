Step 6 of 50: training loss 1.1621, accuracy 0.6170.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   854     8    88     4    13    14     2     5     0     3
               1     0   836    55     0    30     0     0   142     0     1
               2    10     6   567    20   177     3    11    10    70   116
               3     5     1    47   722    13   195     2    18     7    20
               4     4    25    50     0   805     0     2    54     4    39
               5     5     3    11   176    18   584    47     8    61     2
               6    61    19    13    33   178    42   601     9    10     1
               7     3    14    59     4    68     6     0   552    15   369
               8    14    49   160    15    36    14   127   109   343   142
               9    23    24    40     0   392    33    11    68    64   306

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810
4 | 2.1250 | 0.3982
5 | 1.3466 | 0.5185
6 | 1.1621 | 0.6170

At most 44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.


Here are 16 training images your step 6 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 1, predicted 2 (top 3: 2 0.38, 7 0.33, 1 0.25)
2. true 9, predicted 0 (top 3: 0 0.77, 4 0.06, 5 0.05)
3. true 9, predicted 4 (top 3: 4 0.30, 5 0.21, 8 0.16)
4. true 9, predicted 7 (top 3: 7 0.36, 9 0.21, 2 0.11)
5. true 8, predicted 9 (top 3: 9 0.19, 2 0.16, 7 0.13)
6. true 0, predicted 2 (top 3: 2 0.42, 0 0.23, 8 0.08)
7. true 7, predicted 1 (top 3: 1 0.32, 7 0.27, 4 0.17)
8. true 2, predicted 8 (top 3: 8 0.39, 2 0.20, 5 0.15)
9. true 2, predicted 4 (top 3: 4 0.38, 8 0.29, 5 0.13)
10. true 3, predicted 5 (top 3: 5 0.33, 3 0.23, 4 0.16)
11. true 2, predicted 9 (top 3: 9 0.48, 0 0.30, 3 0.06)
12. true 7, predicted 9 (top 3: 9 0.52, 0 0.19, 5 0.12)
13. true 2, predicted 0 (top 3: 0 0.69, 9 0.10, 8 0.09)
14. true 7, predicted 2 (top 3: 2 0.25, 7 0.18, 9 0.13)
15. true 8, predicted 9 (top 3: 9 0.43, 7 0.21, 2 0.09)
16. true 8, predicted 2 (top 3: 2 0.73, 7 0.12, 1 0.06)

[image: mistakes.png]
