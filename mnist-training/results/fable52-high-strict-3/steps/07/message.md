Step 6 of 15: validation loss 0.9409, accuracy 0.7196.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   692     0    28     0     0    15    25     0   229     2
               1     0   820   159     1     0     5     5    21    42    11
               2    29     2   584    63     2     3     2     7   284    14
               3     3     0     6   684     0   113     0     1   221     2
               4    14     7     8     1   449    17    45     1   221   220
               5     3     1     4     5     0   778    31     5    87     1
               6    35     1     4     0     0     5   885     0    36     1
               7    17     0    28    55     4   120     0   590    73   203
               8     0     1     5     2     1     3     6     1   980    10
               9    24     0     5    24     0    57    17     4    96   734

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882
5 | 0.8736 | 0.7192
6 | 0.9409 | 0.7196

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
