Step 2 of 50: training loss 1.4511, accuracy 0.5327.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   711     9     0     0     1     0    13     0   256     1
               1     0  1021     6     3     0     4    13    12     3     2
               2    14    26   398    18    23     1    53     4   452     1
               3     4    29    41   365     4   297     5    15   258    12
               4     3    48     1     0   542     0    26     0   228   135
               5     7    51     3    13     7   326   178     0   319    11
               6     9    47     1     0   102     0   695     0   113     0
               7    17    54   171     5    33    10     1   259    81   459
               8     1   163    92     3     6     7    13    19   665    40
               9    23    95     4     4   178    20    24    10   258   345

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.


Here are 16 training images your step 2 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 9 (top 3: 9 0.20, 4 0.16, 6 0.14)
2. true 7, predicted 2 (top 3: 2 0.36, 9 0.24, 7 0.13)
3. true 7, predicted 4 (top 3: 4 0.31, 8 0.24, 0 0.19)
4. true 9, predicted 7 (top 3: 7 0.29, 8 0.15, 9 0.14)
5. true 3, predicted 5 (top 3: 5 0.48, 8 0.25, 0 0.12)
6. true 3, predicted 8 (top 3: 8 0.34, 6 0.18, 4 0.13)
7. true 2, predicted 3 (top 3: 3 0.21, 6 0.18, 1 0.17)
8. true 3, predicted 8 (top 3: 8 0.38, 3 0.22, 5 0.14)
9. true 7, predicted 9 (top 3: 9 0.47, 3 0.09, 5 0.09)
10. true 3, predicted 8 (top 3: 8 0.50, 3 0.17, 6 0.11)
11. true 7, predicted 8 (top 3: 8 0.24, 9 0.24, 0 0.18)
12. true 8, predicted 2 (top 3: 2 0.29, 9 0.29, 8 0.24)
13. true 3, predicted 5 (top 3: 5 0.63, 8 0.14, 3 0.07)
14. true 8, predicted 2 (top 3: 2 0.29, 1 0.24, 7 0.17)
15. true 3, predicted 9 (top 3: 9 0.44, 8 0.15, 5 0.12)
16. true 4, predicted 8 (top 3: 8 0.35, 6 0.24, 4 0.19)

[image: mistakes.png]
