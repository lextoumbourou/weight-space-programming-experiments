Step 3 of 50: training loss 1.6403, accuracy 0.4871.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   838    49     0     0     1     0    93     0     9     1
               1     0  1055     2     0     0     1     3     3     0     0
               2    57   213   441     8    54     0   161    36    20     0
               3    27   195    48   232    10   348    57    84    18    11
               4     8   311     1     0   586     0    26     9     0    42
               5    24   326     1     2    14   331   207     3     4     3
               6    24   173     2     0   153     0   614     0     1     0
               7    43   307    70     0    39    18     2   456     0   155
               8    38   459   166     1    14    15    64    41   175    36
               9    42   429     3     0   256    25    28    32     3   143

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.


Here are 16 training images your step 3 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 4 (top 3: 4 0.35, 9 0.14, 8 0.12)
2. true 7, predicted 9 (top 3: 9 0.36, 7 0.17, 1 0.16)
3. true 7, predicted 9 (top 3: 9 0.46, 0 0.30, 2 0.06)
4. true 2, predicted 1 (top 3: 1 0.40, 6 0.20, 7 0.09)
5. true 4, predicted 1 (top 3: 1 0.27, 4 0.26, 6 0.19)
6. true 9, predicted 2 (top 3: 2 0.30, 0 0.28, 6 0.10)
7. true 3, predicted 4 (top 3: 4 0.39, 5 0.22, 9 0.15)
8. true 9, predicted 4 (top 3: 4 0.33, 9 0.16, 1 0.13)
9. true 9, predicted 4 (top 3: 4 0.79, 0 0.08, 6 0.05)
10. true 9, predicted 1 (top 3: 1 0.41, 9 0.15, 5 0.14)
11. true 8, predicted 0 (top 3: 0 0.22, 9 0.19, 4 0.16)
12. true 9, predicted 4 (top 3: 4 0.53, 9 0.26, 6 0.06)
13. true 9, predicted 1 (top 3: 1 0.65, 7 0.12, 6 0.10)
14. true 7, predicted 1 (top 3: 1 0.24, 9 0.22, 4 0.19)
15. true 9, predicted 1 (top 3: 1 0.78, 7 0.19, 2 0.01)
16. true 3, predicted 1 (top 3: 1 0.37, 3 0.20, 5 0.16)

[image: mistakes.png]
