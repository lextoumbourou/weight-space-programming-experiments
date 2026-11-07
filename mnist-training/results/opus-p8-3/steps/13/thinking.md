The 9s now land on 0 (at position 172), 6s on 0 (253), and recall on 8s fell to 331. The loop features are firing, just not where I expected, since they push toward 0 and its central cells. I wonder whether the 9s and 6s are really triggering the HB2 features instead, since the 0 template has a strong HB2 component. Meanwhile 2, 3, 5 and 4 improved, with 2 at 750 and 3 at 735.

I'm checking the 6, 8 and 9 accuracy drop against the 0 template: the loop features of 6, 8 and 9 likely land on the same rows 0's template uses, so I'm considering trimming 0's small-loop features and adding HB2 for 6 and 9.

I'm now lowering the HB1 and VB1 weights on the 0 template and adding HB2 features to the 6 and 9 templates, since their loop and stroke patterns overlap with 0's rows.

I'm setting the 2 weight to 0.3, and the 6 and 9 mismatches (6 to 5, 9 to 4) are acceptable for now.
