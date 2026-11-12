Step 8 of 50: training loss 1.8055, accuracy 0.4696.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   927    18     2     0     0     0    44     0     0     0
               1     0  1045     6     0     0     4     4     3     2     0
               2   122    91   478     1    15     2   276     2     3     0
               3   109   135   103   215     2   293    57    86    28     2
               4    18   135     4     0   560     0   247     0     3    16
               5    76   138     5     0     4   294   381     1    15     1
               6    73    53     0     0    59     0   782     0     0     0
               7    86   191   229     1    20    25     2   240     2   294
               8   115   407   190     0     2    28   216    15    35     1
               9   141   282    23     0   225    47    91    17    15   120

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
8 | 1.8055 | 0.4696

At most 42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.


Here are 16 training images your step 8 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 1 (top 3: 1 0.45, 6 0.40, 8 0.09)
2. true 9, predicted 0 (top 3: 0 0.72, 4 0.10, 6 0.10)
3. true 2, predicted 1 (top 3: 1 0.47, 7 0.32, 2 0.20)
4. true 9, predicted 4 (top 3: 4 0.37, 9 0.30, 5 0.16)
5. true 5, predicted 6 (top 3: 6 0.43, 5 0.25, 8 0.18)
6. true 7, predicted 9 (top 3: 9 0.50, 7 0.28, 2 0.11)
7. true 2, predicted 6 (top 3: 6 0.46, 0 0.24, 2 0.17)
8. true 2, predicted 6 (top 3: 6 0.63, 2 0.11, 0 0.09)
9. true 7, predicted 9 (top 3: 9 0.75, 5 0.12, 0 0.06)
10. true 8, predicted 0 (top 3: 0 0.50, 6 0.16, 2 0.11)
11. true 8, predicted 6 (top 3: 6 0.35, 1 0.31, 8 0.21)
12. true 9, predicted 6 (top 3: 6 0.28, 4 0.26, 0 0.22)
13. true 5, predicted 1 (top 3: 1 0.38, 6 0.33, 8 0.16)
14. true 7, predicted 2 (top 3: 2 0.88, 7 0.10, 1 0.01)
15. true 8, predicted 1 (top 3: 1 0.36, 7 0.35, 2 0.23)
16. true 9, predicted 1 (top 3: 1 0.74, 8 0.14, 7 0.07)

[image: mistakes.png]
