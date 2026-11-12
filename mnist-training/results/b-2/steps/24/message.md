Step 23 of 50: training loss 1239.2741, accuracy 0.0950.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     3    99    10     1   252   449     0     9   168     0
               1   163   176     0    41   547     0     1   136     0     0
               2     2    15     0    14   770    46     1   127    15     0
               3    19   276     5     3   607   114     0     3     3     0
               4    24   216     5     8   679    39     0    11     1     0
               5    91   233     5    62   467    56     0     1     0     0
               6    10   157    16     5   519   235     0    16     9     0
               7    10   259    54     1   415   307     0    20    24     0
               8    38    61     0    21   725    15     1   135    13     0
               9    33   259     5     1   555   103     0     2     3     0

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906
4 | 1.3284 | 0.6249
5 | 1.1885 | 0.6594
6 | 1.1142 | 0.6913
7 | 1.5617 | 0.6031
8 | 1.1344 | 0.6834
9 | 1.9282 | 0.6363
10 | 0.9695 | 0.6913
11 | 0.9275 | 0.7032
12 | 1107.3885 | 0.0831
13 | 1134.8277 | 0.0887
14 | 0.8973 | 0.7265
15 | 1077.1201 | 0.0622
16 | 1075.4426 | 0.0644
17 | 1047.6190 | 0.1387
18 | 1036.4964 | 0.0562
19 | 0.8330 | 0.7360
20 | 1254.7789 | 0.1760
21 | 1244.8506 | 0.0423
22 | 1295.6073 | 0.0936
23 | 1239.2741 | 0.0950

At most 27 steps left. Reply with the complete build_weights() for step 24 in one Python code block.


Here are 16 training images your step 23 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 1 (top 3: 1 1.00, 0 0.00, 4 0.00)
2. true 0, predicted 8 (top 3: 8 0.57, 5 0.43, 7 0.00)
3. true 8, predicted 4 (top 3: 4 1.00, 7 0.00, 5 0.00)
4. true 9, predicted 4 (top 3: 4 1.00, 5 0.00, 7 0.00)
5. true 6, predicted 4 (top 3: 4 1.00, 5 0.00, 1 0.00)
6. true 1, predicted 7 (top 3: 7 1.00, 6 0.00, 4 0.00)
7. true 0, predicted 5 (top 3: 5 1.00, 8 0.00, 4 0.00)
8. true 6, predicted 1 (top 3: 1 1.00, 2 0.00, 4 0.00)
9. true 0, predicted 5 (top 3: 5 1.00, 4 0.00, 2 0.00)
10. true 7, predicted 5 (top 3: 5 1.00, 8 0.00, 4 0.00)
11. true 6, predicted 4 (top 3: 4 1.00, 1 0.00, 5 0.00)
12. true 6, predicted 4 (top 3: 4 1.00, 1 0.00, 5 0.00)
13. true 9, predicted 1 (top 3: 1 1.00, 4 0.00, 0 0.00)
14. true 2, predicted 4 (top 3: 4 1.00, 5 0.00, 1 0.00)
15. true 9, predicted 5 (top 3: 5 1.00, 4 0.00, 2 0.00)
16. true 6, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)

[image: mistakes.png]
