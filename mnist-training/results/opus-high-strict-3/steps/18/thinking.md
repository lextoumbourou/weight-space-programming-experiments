I'm looking at how the change backfired: digit 5 got worse, with 5 becoming 3 at 159 up from 134, while 3 going to 5 dropped to 125 even though 3 itself improved to 809. The 7-to-9 confusion rose to 158 from 96, and 4 being read as 9 jumped to 183 from 53, even though I never touched 4. My guess is that the extra loop term added to Wt[9] also fits 4, since closed-top 4s have a loop-like left side. Digit 6 improved to 819.

The pattern holds across all four pairs: the B class gains and the A class loses. My guess is that compact templates just have larger dot products with the input, and the 5 and 7 parts I drew are weaker than the B parts in the real data. The effect is strong even at a=0.06, so the sensitivity is high, but flipping the sign would just be wrong.

I'm weighing whether to stop here: reaching a 0.4pp gain at step 18 looks hard, and the bias tweaks only helped slightly. The sensitivity to a tiny weight change suggests the logit margins are small relative to the part responses, so I'm considering balancing the parts by normalizing with L1 instead of L2, since that gives an exact zero difference for uniform ink.

I'm weighing an L1-balanced version of the parts for step 18, since that would make the uniform-ink response exactly zero. It's risky as a final step, so I'm also considering the safer route of returning to step 15 with small bias tweaks, which would likely land near 74.6%.

I'm weighing whether bias-only adjustments from step 15 are more reliable than the risky L1 experiment, since the 1 column still sits high and the 4 column sits low.

I'm now tuning the bias terms: lowering class 1 slightly, raising 4 and 2, and nudging 0, 6 and 9 a little. I expect a small gain of a couple tenths of a point. I'm also wondering whether blending L1-balanced parts with a small weight would help, but I'd need to estimate that scale first.

I'm weighing whether to finish these bias tweaks, lowering class 1 and raising 4, or to gamble on the L1-balanced parts, since their placement might be off.

I'm going to try L1-balanced parts only for the 3/5 and 7/9 pairs at a=0.08, along with the bias tweaks, since the 3↔5 confusion is the largest error at 351 total.
