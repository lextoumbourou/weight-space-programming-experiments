Step 10 of 50: training loss 1.5914, accuracy 0.6284.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   945     5    24     0     0     0     4     5     7     1
               1     0   806    57     0     0    14     7   179     1     0
               2    37     3   715     6     4    15    67     3   133     7
               3     8     3    28   429     0   345     3    43   159    12
               4     4    31    16     0   561     7    51    12   117   184
               5     6     6     9    13     0   550    79     7   245     0
               6    86     4     2     0    43    30   739     1    59     3
               7    12     8    42     4    12    57     1   543    21   390
               8    23    44   147     0     2    48    69   101   524    51
               9    37    34     8     0    63   104    23    82   138   472

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

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.


Here are 16 training images your step 10 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 5 (top 3: 5 0.57, 8 0.33, 6 0.06)
2. true 8, predicted 6 (top 3: 6 0.37, 8 0.36, 1 0.16)
3. true 6, predicted 4 (top 3: 4 0.61, 0 0.28, 5 0.07)
4. true 7, predicted 5 (top 3: 5 0.81, 9 0.19, 3 0.00)
5. true 5, predicted 8 (top 3: 8 0.57, 5 0.41, 6 0.01)
6. true 9, predicted 8 (top 3: 8 0.63, 7 0.28, 2 0.07)
7. true 8, predicted 6 (top 3: 6 0.45, 5 0.21, 3 0.11)
8. true 8, predicted 2 (top 3: 2 0.91, 7 0.05, 6 0.03)
9. true 1, predicted 6 (top 3: 6 0.50, 5 0.28, 1 0.22)
10. true 5, predicted 8 (top 3: 8 0.93, 5 0.05, 6 0.02)
11. true 8, predicted 5 (top 3: 5 0.46, 1 0.25, 6 0.18)
12. true 3, predicted 5 (top 3: 5 0.49, 3 0.44, 9 0.07)
13. true 7, predicted 9 (top 3: 9 0.97, 7 0.02, 3 0.01)
14. true 3, predicted 8 (top 3: 8 0.60, 5 0.22, 0 0.14)
15. true 9, predicted 7 (top 3: 7 0.86, 8 0.06, 1 0.03)
16. true 1, predicted 2 (top 3: 2 0.62, 7 0.27, 1 0.11)

[image: mistakes.png]
