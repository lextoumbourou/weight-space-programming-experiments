Step 4 of 50: training loss 1.3284, accuracy 0.6249.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   859    11    76     7     0    12    25     1     0     0
               1     0   891    60     0     0     0     0   113     0     0
               2    21    55   681   143    21     8     8    20     2    31
               3     7    26    27   732     1   146    14    27     6    44
               4     8   138    79     4   505     1    27    56     0   165
               5     8    12    14   126     3   564   106    74     4     4
               6   108    45    16     8     4    36   749     1     0     0
               7    14    47    39    58     3     6     0   593     0   330
               8    42   114   110    33     3    12    99   379    60   157
               9    47    30    27    44    11    14    30   143     0   615

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906
4 | 1.3284 | 0.6249

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.


Here are 16 training images your step 4 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 1 (top 3: 1 0.45, 6 0.44, 0 0.07)
2. true 6, predicted 5 (top 3: 5 0.78, 4 0.12, 6 0.06)
3. true 1, predicted 7 (top 3: 7 0.53, 1 0.41, 2 0.05)
4. true 8, predicted 9 (top 3: 9 0.92, 7 0.04, 1 0.02)
5. true 8, predicted 9 (top 3: 9 0.43, 1 0.20, 7 0.12)
6. true 9, predicted 7 (top 3: 7 0.54, 2 0.39, 3 0.04)
7. true 7, predicted 9 (top 3: 9 0.62, 7 0.30, 3 0.07)
8. true 8, predicted 1 (top 3: 1 0.55, 9 0.29, 8 0.08)
9. true 9, predicted 5 (top 3: 5 0.52, 4 0.26, 9 0.15)
10. true 5, predicted 3 (top 3: 3 0.58, 2 0.26, 7 0.13)
11. true 8, predicted 3 (top 3: 3 0.72, 2 0.10, 5 0.09)
12. true 8, predicted 1 (top 3: 1 0.78, 7 0.16, 6 0.05)
13. true 0, predicted 5 (top 3: 5 0.54, 3 0.24, 0 0.22)
14. true 7, predicted 9 (top 3: 9 0.91, 7 0.07, 1 0.02)
15. true 4, predicted 7 (top 3: 7 0.95, 2 0.04, 9 0.01)
16. true 3, predicted 9 (top 3: 9 0.53, 3 0.32, 5 0.07)

[image: mistakes.png]
