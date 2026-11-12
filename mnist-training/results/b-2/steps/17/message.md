Step 16 of 50: training loss 1075.4426, accuracy 0.0644.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   125    18     4   151    52    10   296   267    68     0
               1    71    65     1    23   437   154     4    68   241     0
               2   298   135    14   276    78     5   144    39     1     0
               3   464   147    18   219   115    18    28    21     0     0
               4    22   165   368    13    73   274     2    18    48     0
               5   329   129    26   198   155    20    10    35    13     0
               6   465   109     1   173   183    14    10    11     1     0
               7    46   126   202    40   174   181    10   116   195     0
               8   143   370   138    45   201   106     0     4     2     0
               9    65   275   343    20    95   139     6     8    10     0

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

At most 34 steps left. Reply with the complete build_weights() for step 17 in one Python code block.


Here are 16 training images your step 16 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 2 (top 3: 2 0.98, 5 0.02, 8 0.00)
2. true 9, predicted 5 (top 3: 5 1.00, 2 0.00, 4 0.00)
3. true 2, predicted 3 (top 3: 3 0.98, 4 0.02, 6 0.00)
4. true 6, predicted 4 (top 3: 4 1.00, 3 0.00, 1 0.00)
5. true 8, predicted 4 (top 3: 4 1.00, 3 0.00, 1 0.00)
6. true 7, predicted 4 (top 3: 4 0.96, 5 0.04, 7 0.00)
7. true 2, predicted 1 (top 3: 1 0.89, 4 0.11, 2 0.00)
8. true 7, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)
9. true 4, predicted 2 (top 3: 2 0.98, 5 0.02, 8 0.00)
10. true 6, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
11. true 0, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)
12. true 3, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
13. true 6, predicted 5 (top 3: 5 0.63, 4 0.37, 2 0.00)
14. true 4, predicted 5 (top 3: 5 1.00, 2 0.00, 8 0.00)
15. true 7, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
16. true 9, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)

[image: mistakes.png]
