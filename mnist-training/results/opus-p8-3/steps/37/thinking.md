I'm decoding the three bit features from the first sample, with the sums for each feature coming out to 978, 807, and 738. I'm now working through the second sample, where the first feature comes to 29 and the other two to 2.

I'm running the same sum-and-compare over the remaining samples, from the third through the tenth. Sample 9 gives F1 941, F2 629, F3 370, and comparing samples 7 and 9 shows F1 separating them much more clearly than F2.

I'm checking the F3 separations between samples 0, 2, 6, and 8, where F2 splits 0 from 2 most sharply. I'm settling on the three stroke features at λ_s=0.4 and m=1.6 in the step 34 config, and I'm leaning toward a temperature of 1.3 to offset the larger logit magnitudes.
