The loss is 17.3, which points to logits that are far too large, with predictions piling up on classes 5, 4, 2 and 3. I'll shrink the fc scale and correct the biases. Classes 0 and 1 look mostly fine, though 1 often gets predicted as 2.

I'm weighing a few fixes I can make without running code: shrinking the logit scale sharply so the wrong predictions stop costing so much, and nudging the class biases. The 5 and 4 biases look too high given how often they get predicted, and I'm also looking at the 1-versus-2 confusion, since 1 is being called 2 very often.

I'm considering whether the per-cell activity being positive means template mean subtraction would help, though that's hard to pin down without seeing the results. The fc is essentially a spatial occupancy classifier, which is decent but crude, and getting much better by hand would be difficult. I'm weighing channel-specific weights, since I don't yet know which conv2 channels correspond to which stroke patterns.

I'm tracing how each conv2 output channel draws on a conv1 channel and a pattern: outputs 0 to 7 take their main input from the matching conv1 channel, and outputs 8 to 15 reuse the same pattern indices with a shifted secondary channel.

I'm going through how the conv2 channels map onto the conv1 patterns, checking which ones line up on the same detector, like the vertical and horizontal strokes, and noting that channels 5, 6, and 7 are less clean matches. Rather than dig much deeper, I'm weighing whether to simply weight all the channels equally in the fc sum, since that's what it currently does.

I'm checking the per-class totals next, since class 5 and class 4 look heavily over-predicted, and I'm weighing how to set their biases once the scale is fixed.

I'm thinking about the bias values now, which feel too strong for classes 5 and 4 and may need pulling down. Once I scale the fc weights by about 0.02 instead of 0.1, the logits should shrink roughly fivefold, so the spread would fall to around 3.5, which seems more reasonable.

Now I'm picking a scale of 0.02 for the fc weights, and I'm sketching bias offsets to pull classes 4 and 5 down while nudging 0, 1 and 7 up.

I'm looking at which digits get mistaken for which, and the worst cases are 7 being called 3 and 9 being called 5 or 4. Penalizing 4 and 5 while boosting 6, 7 and 9 through biases alone won't fix everything. I'm also checking how the 3 and 7 templates overlap, since the top row that 7 has is missing from template 3.

I'm thinking about refining the templates, especially for digit 7 and the 9-versus-4 and 5 confusions. A finer representation would help, but the conv features only give a 4x4 grid, so I'm considering channel-aware weights that treat the vertical, horizontal, diagonal and blob channels differently.

I'm thinking about splitting the fc weights by stroke type, giving the direction channels more weight than the blob channel, since stroke direction separates digits like 1, 7, 4 and 2 well. Building channel-specific templates is the next step, starting with the horizontal-stroke channels.

I'm weighing whether to split the fc weights by channel direction, giving vertical, horizontal and diagonal channels their own gains. The per-direction template approach would be more work with uncertain payoff, so I'm leaning toward a simpler change: drop the fc scale to 0.02 and adjust the biases.

I'm checking whether the 1-versus-2 confusion can be fixed through the templates, since the 1 pattern sits in the centre columns and the 2 template's positive cells don't clearly rule that out.

I'm settling on a fixed bias offset for classes 1 and 2 to counter the thin-stroke digits being pulled toward 2.

I'm setting the per-class biases now: a small lift for 1, 6 and 7 since they're under-predicted, a slight pull-down for 4 and 5, and a light cut for 3.

I'm refining the template for digit 7: the top row stays fully positive, with the diagonal stroke running from top right down to the bottom-left centre.

Still refining the 6 and 9 templates, trying to tell 9 apart from 4 by how the top loop closes.

I'm settling the bias offsets now: a small lift for 1 and 6, a slight pull-down for 4 and 5, and I'll keep the logit scale at 0.02 so the wrong predictions stop dominating the loss.

Writing the full code now...
