Step 2 of 15: validation loss 18.7136, accuracy 0.1463.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     0     0     0     8     0     0     0   982     1
               1     0   182     0     0   740     0     0   138     2     2
               2     0    15    14     0   579     0     1     0   319    62
               3     0     1     0     0   343     0     0     0   672    14
               4     0     0     0     0   817     0     0     0    86    80
               5     0     9     3     1   255     0     3     1   641     2
               6     0     6     0     0   425     0    10     0   517     9
               7     0     0     0     0   342     0     0     2   496   250
               8     0     5     1     0   479     0     0     1   351   172
               9     0     0     0     0   753     0     0     0   121    87

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 3.8220 | 0.2083
2 | 18.7136 | 0.1463

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
