Now I'm checking the column totals, and the balance looks moderate at this point. What's left are structural mismatches, mainly between 0 and 8, 6 and 8, and 7 with several other columns.

Now I'm weighing which features would help separate the confusable pairs, like 1 versus 7 and 7 versus 4. Negative orientation evidence might sharpen those boundaries, with small penalty weights on features that shouldn't be present for each class.

Now I'm weighing whether negative orientation penalties would sharpen the 1-versus-7 boundary, but adding them tends to favour denser templates, which would push the 8, 0 and 6 predictions even higher. I'm considering a small compensating bump to the class 8 offset to offset that.

I'm weighing whether to swap the shifted-copy channels for something more discriminative, like endpoint or junction detectors, though designing those within the rules is unclear. I'm also considering pooling the (3,3) tap instead, which would shift the cells down-right, but I doubt it adds much over the current geometry.

Now I'm weighing a few more feature ideas, like endpoint or junction detectors, but they're hard to design within the rules. For the remaining steps I'll keep it incremental: add small negative orientation weights and nudge the class multipliers, raising 8 slightly since it's over-predicted, and lowering 4 and 0 a bit while raising 2.

Now I'm weighing the per-class multipliers against the confusion counts, with 8 and 4 looking over-predicted and 2 under. I'm also checking whether the 3→5 errors could be cut by using the orientation negatives on the top-right of the 5 template.

Now I'm considering whether to offset the 0-versus-8 confusion with a higher ink weight, since the 8 template expects ink in the centre that a 0 lacks. Orientation penalties won't address that one directly, so I'm leaning toward nudging the ink term instead.
