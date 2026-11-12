Step 22 of 50: training loss 1295.6073, accuracy 0.0936.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     0     0     9    12     6    40   430   494     0
               1    27    72     1    25   292   629     0    12     6     0
               2     3     9     8    22   178   305     4   116   345     0
               3     0     3     2     6   103   234     9   206   467     0
               4     0     1     3     3   119   147     0    94   616     0
               5     4     1     2    12   132    91     1   261   411     0
               6     1     0     0     2    45    39     1   218   661     0
               7     2    10     2    13   164   231     3   133   532     0
               8     1     1     0     3    88   342     1    67   506     0
               9     0     0     2     1    37    27     2   305   587     0

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

At most 28 steps left. Reply with the complete build_weights() for step 23 in one Python code block.


Here are 16 training images your step 22 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)
2. true 0, predicted 7 (top 3: 7 1.00, 8 0.00, 6 0.00)
3. true 7, predicted 4 (top 3: 4 1.00, 5 0.00, 7 0.00)
4. true 9, predicted 7 (top 3: 7 1.00, 8 0.00, 6 0.00)
5. true 4, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)
6. true 6, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
7. true 9, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)
8. true 2, predicted 7 (top 3: 7 1.00, 4 0.00, 8 0.00)
9. true 4, predicted 7 (top 3: 7 0.97, 8 0.03, 4 0.00)
10. true 6, predicted 7 (top 3: 7 0.98, 8 0.02, 4 0.00)
11. true 5, predicted 4 (top 3: 4 1.00, 5 0.00, 7 0.00)
12. true 0, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
13. true 7, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)
14. true 9, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
15. true 6, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
16. true 1, predicted 5 (top 3: 5 1.00, 8 0.00, 2 0.00)

[image: mistakes.png]
