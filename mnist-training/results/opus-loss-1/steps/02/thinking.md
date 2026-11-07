The model is at 51% accuracy with a loss of 2.32, so it's overconfident. Its predictions lean toward 1 and 7, the low-ink digits, while 8 almost never comes out, which points to the bias terms being too negative for the heavy digits. I'm thinking the fix is to reduce the bias magnitude or scale the features down.

I'm halving the feature magnitude (c=0.5) for the bias and weight terms, and lowering the spread with s2 around 0.2, since halving μ cuts the logit spread roughly fourfold. I'll start with one global change, c=0.5, and see how the confusions between 8, 7, 2, and 9 respond.
