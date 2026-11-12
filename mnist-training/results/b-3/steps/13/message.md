Step 12 of 50: training loss 1.2658, accuracy 0.6402.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   925    14    14    14     0     2     2     0    20     0
               1     0  1040    17     0     0     0     7     0     0     0
               2    11    24   731    97     2     0    64     5    49     7
               3     3    38    86   651     0    61    73    42    59    17
               4    11   139    34     6   181     0    20     3    94   495
               5    22    63   113    90     1   331   179    17    69    30
               6    34    75    10     9    16     3   755     0    65     0
               7    45    42    54    12     7    13     6   779    10   122
               8    14   174   268     9     0     2    72    56   398    16
               9    25   125    15     4     3    12    13    66    87   611

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810
4 | 2.1250 | 0.3982
5 | 1.3466 | 0.5185
6 | 1.1621 | 0.6170
7 | 1.3141 | 0.6005
8 | 1.1417 | 0.6499
9 | 3.4269 | 0.4356
10 | 1.5914 | 0.6284
11 | 4.5635 | 0.4265
12 | 1.2658 | 0.6402

At most 38 steps left. Reply with the complete build_weights() for step 13 in one Python code block.


Here are 16 training images your step 12 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 9 (top 3: 9 0.29, 5 0.23, 6 0.17)
2. true 7, predicted 9 (top 3: 9 0.21, 7 0.14, 3 0.12)
3. true 8, predicted 1 (top 3: 1 0.46, 7 0.20, 2 0.10)
4. true 5, predicted 8 (top 3: 8 0.19, 6 0.18, 3 0.14)
5. true 9, predicted 1 (top 3: 1 0.66, 7 0.17, 6 0.03)
6. true 3, predicted 1 (top 3: 1 0.34, 2 0.16, 7 0.16)
7. true 9, predicted 2 (top 3: 2 0.20, 8 0.17, 6 0.11)
8. true 3, predicted 5 (top 3: 5 0.35, 6 0.18, 3 0.18)
9. true 5, predicted 8 (top 3: 8 0.25, 6 0.16, 0 0.16)
10. true 4, predicted 9 (top 3: 9 0.28, 4 0.17, 8 0.13)
11. true 5, predicted 2 (top 3: 2 0.23, 5 0.18, 0 0.16)
12. true 4, predicted 1 (top 3: 1 0.35, 9 0.17, 4 0.11)
13. true 9, predicted 1 (top 3: 1 0.19, 6 0.17, 4 0.15)
14. true 8, predicted 0 (top 3: 0 0.21, 8 0.15, 2 0.15)
15. true 4, predicted 9 (top 3: 9 0.21, 8 0.19, 4 0.17)
16. true 3, predicted 8 (top 3: 8 0.24, 3 0.23, 5 0.20)

[image: mistakes.png]
