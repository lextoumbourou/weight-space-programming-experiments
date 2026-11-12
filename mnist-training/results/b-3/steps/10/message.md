Step 9 of 50: training loss 3.4269, accuracy 0.4356.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   843     4     6     0     0     1     1     1   134     1
               1     0   756    50     0     0    25     5   204    24     0
               2    13     2   485     5     0    12    18     2   449     4
               3     2     1    10    98     0   119     1    13   776    10
               4     2     8     2     0   192     3     4     0   597   175
               5     0     2     1     0     0   167    10     4   731     0
               6    27     2     2     0    18     5   270     0   638     5
               7     4     4    30     2     2    67     0   379   170   432
               8     1    17    10     0     1     3     3    16   948    10
               9    13     9     0     0     2    25     1    14   679   218

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

At most 41 steps left. Reply with the complete build_weights() for step 10 in one Python code block.


Here are 16 training images your step 9 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 8 (top 3: 8 1.00, 9 0.00, 5 0.00)
2. true 9, predicted 0 (top 3: 0 0.97, 9 0.02, 5 0.01)
3. true 9, predicted 8 (top 3: 8 0.93, 9 0.04, 4 0.02)
4. true 2, predicted 8 (top 3: 8 0.98, 0 0.02, 4 0.00)
5. true 9, predicted 8 (top 3: 8 0.68, 9 0.16, 5 0.11)
6. true 1, predicted 8 (top 3: 8 0.48, 5 0.20, 1 0.17)
7. true 5, predicted 8 (top 3: 8 1.00, 3 0.00, 5 0.00)
8. true 6, predicted 0 (top 3: 0 0.51, 6 0.31, 8 0.12)
9. true 5, predicted 8 (top 3: 8 1.00, 5 0.00, 6 0.00)
10. true 5, predicted 8 (top 3: 8 0.98, 5 0.02, 6 0.00)
11. true 6, predicted 8 (top 3: 8 0.98, 6 0.02, 0 0.00)
12. true 1, predicted 7 (top 3: 7 0.53, 2 0.39, 1 0.07)
13. true 5, predicted 8 (top 3: 8 1.00, 3 0.00, 5 0.00)
14. true 1, predicted 7 (top 3: 7 0.56, 2 0.23, 1 0.21)
15. true 9, predicted 8 (top 3: 8 0.81, 9 0.19, 5 0.00)
16. true 5, predicted 8 (top 3: 8 0.91, 5 0.09, 9 0.00)

[image: mistakes.png]
