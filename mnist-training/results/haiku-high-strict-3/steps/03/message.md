Step 2 of 15: validation loss 3.9784, accuracy 0.3627.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   851     1    37    43    13    44     1     0     1     0
               1     0   762   285     8     3     6     0     0     0     0
               2     7     0   416   257    43   223     0     0    43     1
               3     9     5   177   604    90   129     0     0    16     0
               4     2    12     2     6   557   360     0     0    44     0
               5    51    11   140   176   114   398     0     1    24     0
               6   115    44    73   116   428   183     0     0     8     0
               7    44     9    21   605    60   256     0     9     1    85
               8     0    26   416   104    23   412     0     0    28     0
               9    18    29     3    57   357   461     0     0    34     2

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 17.3035 | 0.3631
2 | 3.9784 | 0.3627

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
