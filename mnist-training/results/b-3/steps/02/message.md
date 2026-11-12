Step 1 of 50: training loss 1.5011, accuracy 0.5277.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   637     4    49     1     0    48   224     3    25     0
               1     0   859    80     0     0     0    12   105     8     0
               2     9     7   390    95     0     2    54     8   422     3
               3     2     1     4   674     0    94    11    11   233     0
               4    10    37    13     2    34     0   141    66   427   253
               5     5     1     2    86     0   334   142     4   340     1
               6    31     3     1     8     0    15   796     0   113     0
               7     5    11    32     5     0    22     1   652   109   253
               8     5    24    51     5     0     0   168    66   676    14
               9    25    22    11     0     0     9    84    66   519   225

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277

At most 49 steps left. Reply with the complete build_weights() for step 2 in one Python code block.


Here are 16 training images your step 1 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 8 (top 3: 8 0.54, 5 0.18, 3 0.17)
2. true 8, predicted 6 (top 3: 6 0.52, 8 0.38, 3 0.07)
3. true 9, predicted 8 (top 3: 8 0.62, 9 0.15, 5 0.09)
4. true 5, predicted 6 (top 3: 6 0.86, 8 0.09, 5 0.04)
5. true 4, predicted 6 (top 3: 6 0.64, 2 0.09, 7 0.09)
6. true 7, predicted 9 (top 3: 9 0.30, 5 0.27, 8 0.26)
7. true 3, predicted 5 (top 3: 5 0.50, 8 0.25, 3 0.21)
8. true 5, predicted 8 (top 3: 8 0.57, 3 0.16, 6 0.14)
9. true 2, predicted 8 (top 3: 8 0.55, 3 0.23, 5 0.14)
10. true 9, predicted 8 (top 3: 8 0.52, 9 0.20, 5 0.18)
11. true 2, predicted 3 (top 3: 3 0.30, 8 0.23, 2 0.18)
12. true 4, predicted 8 (top 3: 8 0.44, 9 0.23, 4 0.23)
13. true 3, predicted 8 (top 3: 8 0.37, 3 0.27, 6 0.18)
14. true 0, predicted 6 (top 3: 6 0.47, 0 0.40, 7 0.05)
15. true 4, predicted 9 (top 3: 9 0.46, 8 0.16, 6 0.11)
16. true 4, predicted 6 (top 3: 6 0.38, 7 0.21, 8 0.11)

[image: mistakes.png]
