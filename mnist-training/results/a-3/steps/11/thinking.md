Reverting didn't fix the 8s and 9s, so the new 7 template, or the signature change, seems to be pulling them in. Both 8 and 9 are still landing closer to 7 than they should. I'm comparing the new 7 shape, a top bar with a curved stem, against the earlier 7 template and checking how close the stem endpoints are.

I'm working out per-digit bias adjustments from the prediction counts, and the 7 correction is looking too large since removing that variant will also pull 7's predictions down. So I'm going to take a smaller step on 7 than the raw calculation gives.

I'm weighing whether to revert the signature to 2.2, since that's the setting from the best-scoring step, though that would mix several changes together. The per-digit bias values I'd tuned back then were calibrated for the old templates, so they may not carry over cleanly.

I'm going with signature 2.2 and dropping the 7 variant, then applying the computed biases with 7 set to 0.15 so it doesn't overcorrect.
