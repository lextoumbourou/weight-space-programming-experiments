I've hit a limit with the features themselves: they're too coarse, and a slanted 1 gets mistaken for a 7 because its diagonal lines up with the 7's stroke. I'm thinking about whether thick, bold digits are also losing signal, since the zero-mean kernel may be suppressing them, and whether adding an ink-intensity channel would help.

I'm weighing whether a plain blur channel would help thick digits, and whether more orientations would separate slanted 1s from 7s. The 7 template's diagonal seems to dominate, so the top bar's weak contribution doesn't stop the 1 being matched to it. I'm also wondering whether a dot-product scoring is the real problem, since it ignores features the template expects but the image lacks.

I'm working out a scoring rule that works in real feature units, so a template with more ink is penalized more, which should separate thin 1s from 7s. The idea is that the squared-norm term in the score favors the lighter template for a sparse image.

I'm trying to pin down the scale of the template features against the actual pooled activations. A straight stroke through the center gives a template peak around 7.5, while the real feature is closer to 0.4 to 0.5, so I'm considering a scale factor near 0.06. With that, the score would take the form 2α·T·f minus α²·||T||², which would penalize the heavier-ink 7 template. I'm not certain the stroke coverage holds for narrower or lower-placed digits, though, so that's a risk I still need to check.

I'm working toward a distance-based score with the template scaled to real feature units, α around 0.06, so that heavier-ink templates get penalized. I still need to pick the sharpness parameter s, since the typical squared distances are uncertain, and I'm estimating the feature norm roughly before settling on a value.

I'm settling on the distance-based scoring with α around 0.06 and keeping the feature set unchanged so the effect is easy to isolate. I'll drop the bias terms for now and see how the ink-sensitive distance handles the 1 versus 7 confusion, even though it's a bit of a gamble.

I'm settling the scale now: with the distance form and α around 0.065, the score becomes a linear term in the template's dot product minus a penalty on its norm, so I still need the template norm to match it against the earlier scoring.

Writing the distance-based scoring code now...
