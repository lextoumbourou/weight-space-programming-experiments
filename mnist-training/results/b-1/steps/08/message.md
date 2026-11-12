Step 7 of 50: training loss 5.6237, accuracy 0.2327.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   465     0     0     0     0     0    17     0   509     0
               1     0   335     5     0     0     1     0    23   700     0
               2    11     1    36     2     6     0    21     0   912     1
               3     0     0     2    18     0    14     0     0   989     7
               4     1     0     0     0   212     0     6     0   740    24
               5     6     4     2     0     3    41    50     2   807     0
               6     3     0     0     0    40     0   150     0   774     0
               7     8     0    28     4     5     2     0    11   569   463
               8     0     0     1     0     0     0     0     0  1008     0
               9     7     0     0     0    15     0     1     0   887    51

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078
5 | 2.7367 | 0.4958
6 | 2.3875 | 0.4751
7 | 5.6237 | 0.2327

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.


Here are 16 training images your step 7 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 1, predicted 8 (top 3: 8 0.92, 1 0.04, 6 0.03)
2. true 1, predicted 8 (top 3: 8 0.99, 1 0.00, 3 0.00)
3. true 0, predicted 8 (top 3: 8 0.93, 6 0.07, 0 0.00)
4. true 5, predicted 8 (top 3: 8 0.99, 6 0.01, 4 0.00)
5. true 2, predicted 8 (top 3: 8 1.00, 6 0.00, 2 0.00)
6. true 4, predicted 8 (top 3: 8 0.69, 4 0.24, 9 0.07)
7. true 7, predicted 8 (top 3: 8 0.62, 9 0.38, 4 0.00)
8. true 7, predicted 8 (top 3: 8 0.72, 3 0.16, 9 0.08)
9. true 5, predicted 8 (top 3: 8 1.00, 9 0.00, 5 0.00)
10. true 5, predicted 8 (top 3: 8 1.00, 6 0.00, 9 0.00)
11. true 0, predicted 8 (top 3: 8 1.00, 6 0.00, 9 0.00)
12. true 6, predicted 8 (top 3: 8 0.99, 6 0.01, 4 0.00)
13. true 7, predicted 9 (top 3: 9 0.96, 4 0.03, 8 0.01)
14. true 3, predicted 8 (top 3: 8 0.95, 9 0.04, 3 0.01)
15. true 5, predicted 8 (top 3: 8 1.00, 6 0.00, 5 0.00)
16. true 7, predicted 8 (top 3: 8 0.73, 9 0.27, 2 0.00)

[image: mistakes.png]
