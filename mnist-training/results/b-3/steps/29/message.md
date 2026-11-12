Step 28 of 50: training loss 0.8325, accuracy 0.7465.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   923     9     7     7     0     4     3     0    37     1
               1     0   996    45     1     1     1     3    17     0     0
               2    23     5   675   190    26     0    28     6    37     0
               3     3     6    44   668     1   136    36    39    84    13
               4     9    30    20     4   755     1     2    16    55    91
               5    19    10    51    56     6   596    78    31    49    19
               6    58    28    10    11    50    47   748     0    15     0
               7    38     2    25    27    25    40     0   821     5   107
               8    13    51   113    15     7    14    50    84   632    30
               9    32    34     4     4    67    22     2    84    61   651

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
13 | 1.0549 | 0.6888
14 | 1.0054 | 0.6912
15 | 1.3050 | 0.6310
16 | 1.0132 | 0.7045
17 | 1.2671 | 0.6900
18 | 1.0565 | 0.6974
19 | 0.9941 | 0.7178
20 | 0.9956 | 0.7153
21 | 1.0361 | 0.7076
22 | 0.8874 | 0.7288
23 | 0.8718 | 0.7277
24 | 0.8428 | 0.7345
25 | 0.8313 | 0.7399
26 | 0.8296 | 0.7406
27 | 0.8180 | 0.7502
28 | 0.8325 | 0.7465

At most 22 steps left. Reply with the complete build_weights() for step 29 in one Python code block.


Here are 16 training images your step 28 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 2 (top 3: 2 0.46, 1 0.35, 3 0.06)
2. true 7, predicted 0 (top 3: 0 0.67, 9 0.16, 5 0.14)
3. true 6, predicted 5 (top 3: 5 0.52, 0 0.21, 6 0.08)
4. true 0, predicted 3 (top 3: 3 0.75, 2 0.12, 5 0.06)
5. true 6, predicted 8 (top 3: 8 0.97, 6 0.02, 0 0.01)
6. true 7, predicted 0 (top 3: 0 0.67, 9 0.17, 5 0.08)
7. true 3, predicted 5 (top 3: 5 0.44, 3 0.37, 6 0.10)
8. true 5, predicted 8 (top 3: 8 0.51, 6 0.40, 5 0.05)
9. true 7, predicted 0 (top 3: 0 0.62, 7 0.19, 5 0.05)
10. true 3, predicted 6 (top 3: 6 0.48, 4 0.36, 3 0.09)
11. true 8, predicted 2 (top 3: 2 0.52, 7 0.25, 8 0.09)
12. true 8, predicted 1 (top 3: 1 0.50, 7 0.40, 2 0.08)
13. true 5, predicted 8 (top 3: 8 0.40, 5 0.32, 6 0.11)
14. true 7, predicted 9 (top 3: 9 0.62, 7 0.18, 5 0.11)
15. true 7, predicted 9 (top 3: 9 0.67, 5 0.11, 7 0.10)
16. true 5, predicted 6 (top 3: 6 0.49, 5 0.33, 3 0.13)

[image: mistakes.png]
