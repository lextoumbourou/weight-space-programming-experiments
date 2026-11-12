Step 2 of 50: training loss 1.1869, accuracy 0.6212.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   889     2    63     6     0    18     6     2     5     0
               1     0   794   147     1     0    16    14    91     0     1
               2    24     4   582   102     0    18    40     3   210     7
               3     2     0    11   819     0   164     1     3    28     2
               4    13    18    50     7   298     5    79    30   246   237
               5     5     0     6   113     0   659    63     4    64     1
               6    80     1     3    17     1    60   761     0    44     0
               7    14     4    96    27     4    52     0   499    63   331
               8    10    11   106    28     0    18   155    37   605    39
               9    54     9    30     3     3   112    54    42   348   306

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.


Here are 16 training images your step 2 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 9 (top 3: 9 0.55, 8 0.26, 3 0.11)
2. true 1, predicted 7 (top 3: 7 0.68, 2 0.26, 1 0.06)
3. true 0, predicted 2 (top 3: 2 0.28, 0 0.23, 8 0.15)
4. true 2, predicted 8 (top 3: 8 0.66, 2 0.14, 3 0.09)
5. true 4, predicted 8 (top 3: 8 0.50, 9 0.12, 4 0.11)
6. true 3, predicted 5 (top 3: 5 0.56, 3 0.24, 8 0.15)
7. true 9, predicted 8 (top 3: 8 0.31, 9 0.20, 5 0.17)
8. true 3, predicted 5 (top 3: 5 0.46, 8 0.22, 3 0.21)
9. true 7, predicted 9 (top 3: 9 0.72, 5 0.18, 0 0.03)
10. true 3, predicted 5 (top 3: 5 0.67, 3 0.24, 8 0.08)
11. true 8, predicted 6 (top 3: 6 0.54, 8 0.17, 0 0.11)
12. true 1, predicted 7 (top 3: 7 0.63, 2 0.31, 1 0.05)
13. true 4, predicted 8 (top 3: 8 0.54, 2 0.22, 6 0.08)
14. true 7, predicted 9 (top 3: 9 0.84, 5 0.07, 3 0.04)
15. true 9, predicted 7 (top 3: 7 0.40, 9 0.24, 8 0.11)
16. true 0, predicted 2 (top 3: 2 0.75, 6 0.07, 0 0.06)

[image: mistakes.png]
