Step 25 of 50: training loss 0.8313, accuracy 0.7399.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   897    10     6    20     1     9     1     0    46     1
               1     0  1017    28     1     0     0     5    13     0     0
               2     9     6   691   147    44     0    33     7    53     0
               3     3    12    35   622     0   121    45    56   124    12
               4     5    45    20     4   678     0     1    14    65   151
               5    12    13    37    58     5   567    88    39    72    24
               6    34    37     6     9    70    36   741     0    34     0
               7    22     4    22    20    25    27     0   849     8   113
               8     8    69    65    12     5     9    42    94   680    25
               9    21    43     2     4    44    20     3    88    79   657

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

At most 25 steps left. Reply with the complete build_weights() for step 26 in one Python code block.


Here are 16 training images your step 25 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 7 (top 3: 7 0.81, 1 0.14, 9 0.01)
2. true 7, predicted 9 (top 3: 9 0.57, 7 0.20, 5 0.10)
3. true 9, predicted 8 (top 3: 8 0.46, 9 0.26, 4 0.06)
4. true 2, predicted 8 (top 3: 8 0.42, 4 0.22, 3 0.15)
5. true 2, predicted 4 (top 3: 4 0.40, 8 0.38, 3 0.14)
6. true 9, predicted 2 (top 3: 2 0.51, 8 0.23, 9 0.07)
7. true 2, predicted 4 (top 3: 4 0.84, 8 0.10, 9 0.02)
8. true 9, predicted 4 (top 3: 4 0.63, 9 0.17, 6 0.08)
9. true 2, predicted 8 (top 3: 8 0.71, 3 0.15, 5 0.06)
10. true 2, predicted 6 (top 3: 6 0.52, 8 0.21, 3 0.09)
11. true 8, predicted 2 (top 3: 2 0.57, 8 0.14, 7 0.13)
12. true 9, predicted 7 (top 3: 7 0.47, 1 0.34, 9 0.11)
13. true 8, predicted 1 (top 3: 1 0.57, 7 0.18, 2 0.12)
14. true 5, predicted 7 (top 3: 7 0.50, 1 0.36, 9 0.08)
15. true 9, predicted 8 (top 3: 8 0.33, 9 0.21, 7 0.18)
16. true 9, predicted 3 (top 3: 3 0.33, 9 0.27, 5 0.20)

[image: mistakes.png]
