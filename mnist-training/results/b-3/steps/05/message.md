Step 4 of 50: training loss 2.1250, accuracy 0.3982.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   775     0    10     0     0     1     8     0   196     1
               1     0   770    85     1     0    10    30   162     4     2
               2     7     0   347    21     0     4    43     0   567     1
               3     1     0     3   156     0    11     2     2   855     0
               4     4     3     7     1     1     1    54    10   786   116
               5     5     0     1    20     0    35    57     3   793     1
               6     9     1     1     0     0     4   638     0   314     0
               7    12     2    71     6     0     9     0   242   256   492
               8     4     1    20     5     0     2    64     5   902     6
               9     9     3     5     0     0     7    29    14   778   116

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810
4 | 2.1250 | 0.3982

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.


Here are 16 training images your step 4 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 6 (top 3: 6 0.42, 8 0.34, 0 0.11)
2. true 3, predicted 8 (top 3: 8 0.55, 3 0.35, 5 0.05)
3. true 5, predicted 8 (top 3: 8 0.94, 3 0.02, 5 0.02)
4. true 5, predicted 8 (top 3: 8 0.85, 3 0.08, 5 0.06)
5. true 4, predicted 8 (top 3: 8 0.86, 6 0.09, 3 0.03)
6. true 4, predicted 8 (top 3: 8 0.95, 9 0.03, 6 0.01)
7. true 5, predicted 8 (top 3: 8 0.90, 5 0.05, 3 0.04)
8. true 7, predicted 9 (top 3: 9 0.46, 8 0.29, 7 0.13)
9. true 3, predicted 8 (top 3: 8 0.90, 3 0.10, 5 0.00)
10. true 3, predicted 8 (top 3: 8 0.64, 3 0.32, 5 0.02)
11. true 3, predicted 8 (top 3: 8 0.77, 3 0.20, 5 0.03)
12. true 5, predicted 8 (top 3: 8 0.93, 3 0.04, 5 0.03)
13. true 2, predicted 8 (top 3: 8 0.51, 2 0.21, 3 0.13)
14. true 5, predicted 8 (top 3: 8 0.74, 3 0.18, 5 0.08)
15. true 1, predicted 7 (top 3: 7 0.61, 2 0.24, 1 0.13)
16. true 6, predicted 8 (top 3: 8 0.92, 6 0.05, 3 0.02)

[image: mistakes.png]
