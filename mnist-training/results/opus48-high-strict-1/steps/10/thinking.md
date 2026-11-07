The hole detector seems to have worked: accuracy is up to 39.24% with the best loss so far. Zeros and 9s improved, but 4s are now getting predicted as 9s a lot, probably because 9s have an upper hole and 4s don't, yet some 4s seem to share that feature.

Now I'm weighing whether 4s are picking up a faint upper hole that pulls them toward 9, since 4→9 went up rather than down. Next I'll check the bias values, where 9 is penalized less than 4, which may be contributing. The 5→6 jump looks like a partial lower loop in 5s triggering the 6 template, and 8→2 is still high because the corner-hole template isn't firing on real 8s. The 1→7 increase might come from 7's high bias.

Now I'm tallying the column totals, and 9 stands out as badly over-predicted at 1665, well ahead of 1 at 1238, 4 at 1031, 6 at 1024, and 3 at 1072. Meanwhile 8, 5, 7 and 0 are all under-predicted.

Now I'm looking at 9 as the main attractor: it's over-predicted at 1665, pulling in 4s, 7s and 8s, so the hole boost went too far there. My plan is to lower 9's bias and make its upper-hole template more specific so it stops absorbing 4s.

Now I'm lowering 6's bias, since it's over-predicted and 5s are triggering its lower-hole template. I'm also reconsidering 7's bias, which looks too high and may be pulling 1s toward 7.

Now I'm recalculating the biases from the column totals, pulling down 9, 1 and 4 and nudging up 8, 5 and 7 to offset their under-prediction.

Now I'm weighing a tradeoff: 7's bias is being pushed up for balance, yet that same boost seems to be pulling 1s toward 7. I'm thinking the 1→7 mistakes come from my 7 template matching a 1's top stroke, so simply lowering 7's bias isn't obviously right. I also want to pull 9 down further than the marginal correction alone suggests, to curb the 9 attraction, and maybe ease the hole scaling a little.

I'm thinking about lowering the hole scale to 1.5 to reduce false hole matches, but that could also weaken the gain on 0s and 9s, so I'm leaning toward keeping it at 2 and correcting through the biases instead. The 4→9 confusion looks like it comes from both the ink templates overlapping and 9's hole, so lowering 9's bias should help curb that.

I'm thinking about whether the 4-versus-9 confusion is coming from the ink templates rather than the hole feature, since 4s have no hole to trigger 9's bonus. Lowering 9's bias would help, but 4's recall is already weak, so the better route is sharpening the templates: a more distinct crossbar and open top for 4, and a closed top loop for 9.

Next I'm going to stop tweaking the ink templates and adjust the biases instead, with a small change to the hole scaling to cut down the 9 and 6 over-predictions.

I'm nudging the biases toward balance: pulling 9 down, raising 8, and considering a further cut to 7 to stop the 1→7 errors.

Next I'm adjusting the biases: I'm lowering 7 to about 1.5 to ease the 1→7 mistakes, and pulling 6 down to around 0.9 to curb 5→6. I'm leaving 4 near -2.0, since raising it would push 4 over-predicted.

Now I'm lowering 9's bias to about -1.1 to rein in its over-prediction, and easing 6 and 7 down to 0.9 and 1.5 to curb the 5→6 and 1→7 errors.

Writing the bias values for the new step, keeping the templates and scales unchanged.
