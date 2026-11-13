The loss is down to 0.3499 with accuracy near 90%, and cutting the corner trust seems to have helped. I'm weighing whether to lower GAMMA_C from 0.45 to 0.33 next, or to settle the measurement question first. With 16 steps left, measuring the other-half H/V cells looks promising since orientation features are strong while corner counts are less reliable, but the features may be correlated and could stop helping.

I'm weighing whether to measure the other-half H/V cells now or keep tuning the knobs. Measuring might add around 0.7% from 16 more features but costs 6 of the remaining steps, while tuning could yield about 0.5% in the same time, so the two look roughly comparable. I'm leaning toward measuring first, since tuning depends on the feature set, and I'm also checking the confusion pairs to see whether other features would target them better.

I'm looking at the largest confusion, 7 being read as 2 (65 cases), and wondering why the bottom-right horizontal cells don't separate them better. Since 2 is a broad, multi-modal class, a 7 with a few unusual features could drop its probability quickly.

I'm checking why 7s get read as 2s so often, and suspect the naive Bayes clipping of rare pixel features makes atypical 7s look very unlikely. Clipping the rates to a wider band like 0.05 to 0.95 might soften that penalty, though I'd try it later.

I'm considering a discriminative tweak for the 7-to-2 confusion, boosting the weight on the bottom-bar features so class 2 has to show that base more strongly. The clipping at 0.98 caps how much a missing bottom bar can count against a 2, so that cap may be what's limiting the fix.

I suspect the 7s are being pulled toward 2 by a crossbar that lands in the lower row of cells instead of the bottom bar, since a crossbar near the middle of the digit would fire the bottom horizontal feature.

I'm wondering whether the crossbar-7s get pulled toward 2 because the bottom horizontal cells fire, and I'm weighing the short base of a 2 against the crossbar's stem. A pairwise tweak would need samples I don't have yet, so I'll set it aside and compare measuring against tuning the knobs.

I'm weighing a few options: lowering the corner-trust knob further, tuning the hole and bias settings, or measuring the other-half H/V cells. Tuning looks worth about as much as measuring over the same steps, so I'm planning to split the remaining budget between the two, with measurement first.

I'm going to try one knob first: GAMMA_C at 0.33, leaving the clipping range alone so the change is easy to read.
