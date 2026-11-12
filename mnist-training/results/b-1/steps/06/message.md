Step 5 of 50: training loss 2.7367, accuracy 0.4958.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   646     1     0     0     5     1    13     0   325     0
               1     0   964     6     1     0     2    15    48    27     1
               2    12     3   185    16    46     1    41     6   680     0
               3     0     8     5   259     2   126    14     7   600     9
               4     1    14     1     0   654     0     9     0   195   109
               5     4    15     0     3    16   199   230     1   434    13
               6     3    13     1     0    80     0   675     0   195     0
               7    11     5   321     4    51    12     0   141   150   395
               8     0    20     5     0     6     1     6    10   948    13
               9     9    20     6     0   258     5     3     5   368   287

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078
5 | 2.7367 | 0.4958

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.


Here are 16 training images your step 5 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 8 (top 3: 8 0.58, 0 0.35, 6 0.05)
2. true 3, predicted 5 (top 3: 5 0.90, 8 0.08, 3 0.01)
3. true 5, predicted 8 (top 3: 8 0.94, 6 0.03, 5 0.03)
4. true 6, predicted 8 (top 3: 8 0.81, 4 0.11, 6 0.07)
5. true 0, predicted 8 (top 3: 8 0.96, 6 0.04, 4 0.00)
6. true 2, predicted 8 (top 3: 8 0.93, 2 0.03, 4 0.03)
7. true 8, predicted 4 (top 3: 4 0.92, 8 0.03, 9 0.02)
8. true 3, predicted 8 (top 3: 8 0.55, 3 0.43, 5 0.02)
9. true 2, predicted 8 (top 3: 8 0.98, 6 0.02, 4 0.00)
10. true 2, predicted 8 (top 3: 8 0.99, 4 0.00, 6 0.00)
11. true 9, predicted 4 (top 3: 4 0.50, 9 0.38, 8 0.11)
12. true 6, predicted 4 (top 3: 4 0.69, 8 0.30, 6 0.01)
13. true 6, predicted 1 (top 3: 1 0.63, 6 0.34, 4 0.01)
14. true 9, predicted 8 (top 3: 8 0.57, 9 0.31, 2 0.05)
15. true 3, predicted 5 (top 3: 5 0.48, 3 0.45, 8 0.06)
16. true 9, predicted 8 (top 3: 8 0.94, 2 0.03, 7 0.01)

[image: mistakes.png]
