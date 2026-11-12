Step 39 of 50: training loss 0.7872, accuracy 0.7655.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   878     6    42    27     0    13     5     0    18     2
               1     0   938    43     1     0     1     0    81     0     0
               2    14     4   701   173    36     0    11     9    39     3
               3     5     0    48   688     1   105    39    29   104    11
               4    10    24    22     6   759     1     2    19    21   119
               5    12     5    32    59     5   630    87    36    37    12
               6    35    23    27     9    60    36   766     3     8     0
               7    22     1    22    35    26    44     0   872     0    68
               8    16    34    66    16     3    14    44    94   677    45
               9    23    15     5     7    29    29     0    74    33   746

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
29 | 0.8148 | 0.7511
30 | 0.7942 | 0.7599
31 | 0.7960 | 0.7635
32 | 0.7836 | 0.7617
33 | 0.7867 | 0.7635
34 | 0.8062 | 0.7472
35 | 0.7829 | 0.7638
36 | 0.7809 | 0.7660
37 | 0.7774 | 0.7684
38 | 0.7774 | 0.7669
39 | 0.7872 | 0.7655

At most 11 steps left. Reply with the complete build_weights() for step 40 in one Python code block.


Here are 16 training images your step 39 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 8 (top 3: 8 0.36, 0 0.22, 5 0.21)
2. true 6, predicted 5 (top 3: 5 0.35, 8 0.25, 0 0.17)
3. true 5, predicted 0 (top 3: 0 0.44, 5 0.29, 7 0.14)
4. true 0, predicted 3 (top 3: 3 0.50, 2 0.31, 5 0.09)
5. true 2, predicted 6 (top 3: 6 0.58, 2 0.19, 8 0.19)
6. true 5, predicted 0 (top 3: 0 0.41, 5 0.37, 8 0.11)
7. true 3, predicted 8 (top 3: 8 0.78, 6 0.12, 3 0.09)
8. true 4, predicted 9 (top 3: 9 0.77, 4 0.14, 8 0.04)
9. true 8, predicted 2 (top 3: 2 0.56, 8 0.24, 0 0.07)
10. true 9, predicted 0 (top 3: 0 0.79, 8 0.12, 5 0.04)
11. true 5, predicted 6 (top 3: 6 0.54, 8 0.26, 5 0.16)
12. true 2, predicted 4 (top 3: 4 0.74, 2 0.15, 3 0.09)
13. true 4, predicted 7 (top 3: 7 0.38, 9 0.21, 8 0.17)
14. true 3, predicted 8 (top 3: 8 0.53, 3 0.24, 5 0.19)
15. true 3, predicted 8 (top 3: 8 0.84, 3 0.07, 0 0.03)
16. true 6, predicted 7 (top 3: 7 0.37, 1 0.28, 2 0.12)

[image: mistakes.png]
