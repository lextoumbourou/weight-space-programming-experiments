Step 10 came in at 33.8%, below step 2's 43.6%, because my biases shifted things too far: 8 now looks sink-like, and 7 and 9 are running high. I'm estimating the step 10 counts column by column to see where the drop comes from.

The per-column counts for step 10 are adding up, and the totals show 7, 8 and 9 have taken over as the dominant predictions while 3 and 5 have nearly vanished. The bias shifts were clearly too strong: a bias of +0.8 on 8 turned it into a sink, and a −1.0 on 5 wiped it out almost entirely.

I'm now seeing that the logits are small, on the order of ±1, which means the biases of 0.1 to 0.3 I'd need are very sensitive. Step 10 overshot because of that. With five steps left and step 2 still the best at 43.6%, I'm weighing whether to return to step 2 with much smaller biases or to scale the fc weights up so the bias adjustments actually matter.

Now I'm working out the step 10 bias values more carefully, since the 0.8 on class 8 was clearly too large relative to the logit spread. I'm trying smaller adjustments in the 0.1–0.2 range instead, starting with class 5 at −0.2 and a few others at ±0.1.

I'm checking whether a bias of −0.3 on class 5 would be enough, since −1 flipped nearly all of its 2871 predictions away, which means most of the margins sit within about one logit.

I'm checking how the bias on class 5 scales: at −1 it nearly wipes out 5's predictions, so a smaller shift around −0.5 would probably still cut them a lot, though the response is clearly nonlinear. Class 8 went from almost nothing to a sink at +0.8, so that bias is far too large. Given only five steps remain, I'm thinking a more principled adjustment could work better than trial-and-error biases.

I'm working out how to set the biases, aiming for small magnitudes around 0.3 that could still lift step 2's result. I'm estimating how many of the excess class-5 predictions a reduced bias would move elsewhere, and whether that would be enough to beat 43.6%.

I'm weighing an iterative bias update: nudge each class's bias by a damped amount proportional to the log ratio of its predicted count to a target count, using step 2's counts as the starting point.

I'm working through per-class adjustments: the sinks from step 2 can be corrected by raising biases for the under-predicted classes and lowering them for the over-predicted ones, scaled by how far off each count is.

Biases of +0.8 on classes 8 and 9 both swept almost everything into them, and +0.3 on class 7 pushed it high too. Taken together with the step 2 baseline, that suggests the logit spread is small, maybe around 0.3 to 0.5, so even modest bias changes move many predictions. I'm thinking the sensitivity per unit of log-ratio correction should be small, around 0.1.

I'm weighing whether to scale the weights up, but scaling weights and biases together leaves the argmax unchanged, so only the bias size relative to the logit spread matters. That makes me think a sensible start is to keep every bias at roughly 0.1 to 0.2.

I'm settling on a damped bias update: each class gets a shift of 0.1 times the negative log of its predicted count against a target of 1000, clipped to ±0.3. That pushes classes 0, 6, 8 and 9 up and 2, 3 and 5 down, with 7 barely moved. I'm uncertain whether 9 will stay modest with a +0.3 bias, since +0.8 blew it up to about 2382 predictions in step 10.

Now I'm comparing the per-class counts for step 10's biases against the step 2 baseline. Classes 2, 3 and 5 collapsed, while 7, 8 and 9 grew into the dominant predictions, and even class 4 dropped sharply without a direct bias change.

Checking how sensitive class 3 is: a shift of −0.5 cut its predictions from about 2132 down to 6, so most of its margins must sit within half a logit. That suggests a bias of 0.1 to 0.2 might already move 10 to 20 percent of them, which makes me wonder whether a learning rate of 0.1 per unit log-ratio is still too large.

I'm checking how sensitive class 3 is: going from −0.5 to a shift that small cut its predictions almost entirely, so most of its margins must sit within half a logit. That suggests the logit spread is tight and biases around 0.05 might be all that's needed.

I'm thinking about a damped update instead, since the bias approach looks fragile with only five steps left. I'm trying a 0.05 scale on the negative log of each class's step 2 count against 1000, clipped to ±0.15. That gives class 0 about +0.15, class 2 about −0.04, class 3 about −0.04, and classes 1 and 4 essentially zero.

I'm settling the bias for each class from its step 2 count: classes 0 and 6 get pushed up, 2, 3 and 5 pulled down, and the rest barely move. Class 7 only needs a tiny nudge upward, while class 5's shift comes out near −0.05.

Trying a smaller, damped bias update now: about 0.15 for the classes with empty or tiny step 2 counts, and slight negative nudges for the over-predicted ones. Step 10 showed these logits are tightly packed, so even small shifts could move a lot of predictions.

I'm weighing whether to drop the calibration approach and go back to the step 2 biases, which gave 43.6%, then spend the remaining steps on small adjustments. My plan for step 11 is to try a set of very small biases, with class 0 and 6 nudged up and classes 2, 3 and 5 nudged slightly down, and to revert in step 12 if it doesn't beat 43.6%.

I'm noticing that the biases I'm using are so sensitive that even small shifts move many predictions, so I'll keep them tiny. My plan is to write the network with these small offsets, using the same structure as step 2.
