Step 25 of 50: training loss 1207.0900, accuracy 0.0714.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     5     8     0   111   550    15     2   225    75     0
               1     3    20     1    47   861    81     0    51     0     0
               2    98   313     1   142   425     6     4     1     0     0
               3    23   680    81    10   183    53     0     0     0     0
               4     9   106    67    35   618   145     1     2     0     0
               5    56   410    48    40   314    44     0     2     1     0
               6     6     2     0   189   643     8     6   109     4     0
               7    11   156   182    18   530   191     0     2     0     0
               8     7    16     0    62   843    42     0    31     8     0
               9     4   141   102     5   508   201     0     0     0     0

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
24 | 1199.8983 | 0.1023
25 | 1207.0900 | 0.0714

At most 25 steps left. Reply with the complete build_weights() for step 26 in one Python code block.


Here are 16 training images your step 25 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
2. true 5, predicted 2 (top 3: 2 1.00, 1 0.00, 5 0.00)
3. true 9, predicted 5 (top 3: 5 1.00, 2 0.00, 4 0.00)
4. true 1, predicted 4 (top 3: 4 0.78, 1 0.22, 3 0.00)
5. true 9, predicted 4 (top 3: 4 1.00, 1 0.00, 5 0.00)
6. true 7, predicted 4 (top 3: 4 1.00, 1 0.00, 3 0.00)
7. true 7, predicted 5 (top 3: 5 1.00, 4 0.00, 2 0.00)
8. true 8, predicted 4 (top 3: 4 1.00, 5 0.00, 1 0.00)
9. true 0, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
10. true 2, predicted 0 (top 3: 0 1.00, 3 0.00, 1 0.00)
11. true 0, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
12. true 2, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
13. true 8, predicted 4 (top 3: 4 1.00, 5 0.00, 1 0.00)
14. true 6, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)
15. true 1, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)
16. true 8, predicted 4 (top 3: 4 1.00, 3 0.00, 1 0.00)

[image: mistakes.png]
