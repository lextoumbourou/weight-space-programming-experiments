I'm at 74% and the gains are slowing. The digit 2 is the weakest class at 562 errors, spread across many confusions, so I'm going to improve its template drawing. I'm adding a narrower variant with a smaller top arc to see whether it matches real 2s better.

I'm weighing whether to boost the confusable digits by drawing their key strokes twice, since the tanh scaling may already saturate on a single stroke.

Still writing the emphasis strokes...

Still weighing confusion pairs: the 2 row has a few higher-count confusions, so I'll bump its weight a bit and also raise the weight on 3's and 1's confusions from column 2.

Now I'm setting the confusion-pair weights: boosting 2 against 3 and 1, 3 against 5, and 5 against 6, while lowering the 8 bias to 1.0. I'm also adjusting 9, 7 and 4 for the 7/9 and 4/9 pairs, and the predicted counts per digit come out to roughly 830 to 1230.

Still setting the bias values: I'm lowering 1 to -0.7, raising 4 and 5 slightly, and nudging 8 down to 1.05, with 2 left at zero.
