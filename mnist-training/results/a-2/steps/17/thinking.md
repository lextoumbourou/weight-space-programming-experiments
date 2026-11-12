I'm at 71.7% and it's moving slowly, so I need a different lever. The orientation templates look like the main place to push, either by adding resolution or by swapping some of them for a shifted-grid set, though with the parts adding only about 0.5%, dropping three of them feels questionable. I'm also wondering whether the conv1 orientation channels are firing on most strokes, which would point to the NB λ and calibration settings being the real issue.

I'm checking whether the conv1 orientation channels respond to most strokes at once, since that would make my firing-probability estimates off. For a vertical stroke against the horizontal kernel, the column through the center comes out with a small positive sum, and the stroke's three columns together give a modest total.

I'm estimating the response of a horizontal detector to a vertical stroke: after normalizing by the positive kernel mass, it comes out around 0.24, and I'm now checking the aligned horizontal stroke case for comparison.

Working through the cross-talk numbers, a vertical stroke already gives the horizontal channel a clipped response of 1 once it's normalized, and a 45° stroke does the same. So each orientation channel fires on its neighbors as strongly as its own stroke, which means the cos⁴ tuning in my templates doesn't match what the filters really do.

I'm estimating the diagonal stroke case now: cells near the line u=v, using the same kernel, to see whether a 45° stroke saturates the horizontal channel too.

I'm working through the diagonal-stroke case now: summing the kernel over the cells near the 45° line, the on-diagonal and adjacent off-diagonal cells contribute positively while the farther ones pull the total down.

I'm checking the numbers on the cross-talk: the 45° and perpendicular responses both come out around 0.3, while the aligned response is near 0.96, so the neighbor channels are being driven far more than the cos⁴ templates assume.

I'm checking whether the orientation channels really fall off with angle: a 22.5° offset still looks close to full, and a 45° one drops to roughly a quarter, which is close to what my cos⁴ templates assume. So the tuning is fine for clean strokes, though thin or faint strokes would push the responses lower than I've been estimating.

I'm now looking at the digit confusions, mainly 2 versus 3 and 2 versus 8. A 2 has a horizontal bottom stroke and no right-side vertical at the bottom, which 3 and 8 both have, so I'm considering a template for that.

I'm considering whether the 2-versus-8 and 2-versus-3 confusions come from the mean 2 diagonal being off. Then I'm thinking the naive Bayes independence assumption might be the real bottleneck, so I'm weighing per-group λ, and instead I'm leaning toward feeding the 16 conv2 channels in unclipped as single-channel features, which doubles the feature count.

I'm weighing whether to scale the presence features down so they fall in a comparable range, since the raw sums can run well above one. Then I'm considering whether to expand the feature set to 16 channels or to pick eight orientations at the first layer instead.

I'm weighing an alternative to the current setup: expanding conv1 to eight orientation channels at 22.5° spacing for sharper discrimination, then feeding both those and some non-orientation features into conv2. I'm also noting that the unclipped responses would need careful scaling, so the gain is uncertain. Tuning the hyperparameters like the smoothing, baseline, λ, and saturation might be a cheaper route to try first.

I'm going to try a quick change to the λ setting, since it mostly shows up in the loss and not the accuracy. I'll also adjust the template for 2 separately, so I can tell their effects apart.

I'm going to strengthen the bottom bar in the 2 template and extend the diagonal down to it. Then I'll check whether that separates 2 from 3, since a 2 lacks the right-side vertical near the bottom that both 3 and 8 have.

I'm going to test a lower λ of 0.25, since that mostly shows up in the loss, and I'll also strengthen the bottom bar of the 2 template to see whether that separates it from 3 and 8.
