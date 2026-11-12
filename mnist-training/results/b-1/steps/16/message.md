Step 15 of 50: training loss 1.3307, accuracy 0.6072.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   647     1     5     4     0     0    35     0   297     2
               1     0   963    48    39     0     3     4     3     4     0
               2    17    12   613    67     4     5    86    12   165     9
               3     2     8    54   540     0   151     9    12   247     7
               4     4    15     4     9   268     0   141     2   121   419
               5     4    33    27    73     0   296   100     3   374     5
               6    13    40     3    26    30     1   821     0    25     8
               7     8    18    37    28    11    31     0   718    51   188
               8     3    76   118   150     0    40    33     4   540    45
               9    15    29     0    34    12    26    16    35   128   666

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
9 | 1.9854 | 0.4561
10 | 1.5771 | 0.5330
11 | 1.8457 | 0.4671
12 | 2.1344 | 0.4372
13 | 1.9350 | 0.5070
14 | 4.0279 | 0.4305
15 | 1.3307 | 0.6072

At most 35 steps left. Reply with the complete build_weights() for step 16 in one Python code block.


Here are 16 training images your step 15 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 1 (top 3: 1 0.76, 3 0.10, 8 0.07)
2. true 3, predicted 2 (top 3: 2 0.98, 3 0.01, 1 0.01)
3. true 8, predicted 9 (top 3: 9 0.26, 8 0.22, 2 0.20)
4. true 4, predicted 9 (top 3: 9 0.39, 4 0.24, 6 0.21)
5. true 2, predicted 8 (top 3: 8 0.39, 9 0.18, 4 0.18)
6. true 4, predicted 8 (top 3: 8 0.31, 4 0.30, 6 0.17)
7. true 5, predicted 3 (top 3: 3 0.37, 8 0.26, 6 0.21)
8. true 1, predicted 3 (top 3: 3 0.51, 1 0.36, 7 0.05)
9. true 4, predicted 9 (top 3: 9 0.45, 7 0.26, 3 0.13)
10. true 4, predicted 9 (top 3: 9 0.36, 6 0.29, 8 0.22)
11. true 5, predicted 2 (top 3: 2 0.52, 3 0.18, 8 0.14)
12. true 5, predicted 8 (top 3: 8 0.46, 6 0.27, 1 0.08)
13. true 3, predicted 5 (top 3: 5 0.69, 8 0.14, 3 0.13)
14. true 5, predicted 6 (top 3: 6 0.43, 8 0.41, 5 0.09)
15. true 4, predicted 8 (top 3: 8 0.31, 9 0.28, 6 0.20)
16. true 5, predicted 8 (top 3: 8 0.63, 1 0.19, 2 0.08)

[image: mistakes.png]
