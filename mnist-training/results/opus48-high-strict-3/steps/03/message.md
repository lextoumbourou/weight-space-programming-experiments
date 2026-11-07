Step 2 of 15: validation loss 3.3087, accuracy 0.2140.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     7     5     0     0   268     0    10     0   701     0
               1     0   878     0     0     8     0     0   168    10     0
               2     0   228     7     0   404     0     1     3   347     0
               3     0    95     0     0   761     0     1     1   172     0
               4     0     5     0     0   851     0     0     0   127     0
               5     0   111     0     0   421     0     7     4   372     0
               6     0    85     0     0   332     0    43     0   507     0
               7     0   110     0     0   958     1     0     4    13     4
               8     0   239     0     0   419     0     0     1   350     0
               9     0    16     0     0   936     0     1     0     8     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9589 | 0.1931
2 | 3.3087 | 0.2140

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
