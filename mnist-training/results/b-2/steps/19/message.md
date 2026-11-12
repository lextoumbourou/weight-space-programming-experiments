Step 18 of 50: training loss 1036.4964, accuracy 0.0562.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   380    94     3    92   263    78     1    13    67     0
               1   495    70     1    52   322    59     1    31    33     0
               2   855     7     0   105    21     0     2     0     0     0
               3   943    35     0    31    21     0     0     0     0     0
               4   491    32     1   236    75     3   112    33     0     0
               5   828    33     0    39    12     0     0     3     0     0
               6   692    75     0    75   107     0     6    10     2     0
               7   798   174     6    22    75    13     0     0     2     0
               8   788   110     2    63    45     1     0     0     0     0
               9   674   147     6    49    75     7     1     0     2     0

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

At most 32 steps left. Reply with the complete build_weights() for step 19 in one Python code block.


Here are 16 training images your step 18 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 3 (top 3: 3 0.71, 0 0.27, 4 0.01)
2. true 8, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
3. true 0, predicted 4 (top 3: 4 1.00, 1 0.00, 3 0.00)
4. true 9, predicted 1 (top 3: 1 0.95, 0 0.04, 4 0.02)
5. true 4, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
6. true 4, predicted 3 (top 3: 3 0.98, 4 0.02, 6 0.00)
7. true 4, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
8. true 8, predicted 3 (top 3: 3 0.98, 4 0.02, 0 0.00)
9. true 9, predicted 0 (top 3: 0 0.89, 1 0.10, 3 0.02)
10. true 2, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
11. true 9, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
12. true 3, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
13. true 7, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
14. true 5, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
15. true 9, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
16. true 1, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)

[image: mistakes.png]
