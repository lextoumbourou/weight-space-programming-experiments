Step 13 of 50: training loss 1134.8277, accuracy 0.0887.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   133    60    35   154   220   144     8    92   145     0
               1    97    68     4    95   681    54     3    50    12     0
               2     7    16     4    45    54    27   490   273    74     0
               3     1    29   175     6    66   390     2    41   320     0
               4    57   269   274    18   115   215     2    13    20     0
               5    36    74   199    33   108   368     6    17    74     0
               6   298    72     6   326   239    15     6     5     0     0
               7    15   119   141    23   147   221     9   175   240     0
               8   124   222    61   133   383    25    24    25    12     0
               9    45   275   351     7   122   105     3    26    27     0

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

At most 37 steps left. Reply with the complete build_weights() for step 14 in one Python code block.


Here are 16 training images your step 13 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 0, predicted 3 (top 3: 3 0.76, 4 0.12, 0 0.10)
2. true 1, predicted 4 (top 3: 4 1.00, 1 0.00, 5 0.00)
3. true 7, predicted 4 (top 3: 4 1.00, 1 0.00, 3 0.00)
4. true 4, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
5. true 0, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
6. true 5, predicted 8 (top 3: 8 1.00, 5 0.00, 2 0.00)
7. true 4, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
8. true 9, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
9. true 2, predicted 6 (top 3: 6 0.98, 7 0.02, 8 0.00)
10. true 9, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
11. true 1, predicted 4 (top 3: 4 0.60, 7 0.40, 3 0.00)
12. true 3, predicted 5 (top 3: 5 1.00, 2 0.00, 8 0.00)
13. true 9, predicted 2 (top 3: 2 0.98, 5 0.02, 1 0.00)
14. true 3, predicted 8 (top 3: 8 1.00, 5 0.00, 2 0.00)
15. true 1, predicted 5 (top 3: 5 0.58, 4 0.42, 8 0.00)
16. true 7, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)

[image: mistakes.png]
