The eight class is now dominating the predictions. I think the orientation-mismatch penalty was the cause: it punished classes whose ink cells had specific orientations, while eight, with its two loops, allows nearly every orientation and so escapes the penalty. The other classes get hit by thick strokes responding across all channels and by curvature, so that penalty was a poor design in this form.

The penalty looks like the culprit: thick strokes respond strongly to every orientation filter, so most digits pick up a large deduction, while 8 has almost no disallowed orientations and comes out ahead. I'll drop the orientation penalty entirely and return to the step 3 bias setup, since step 4 isn't a fair baseline for judging the bias changes.

I'm weighing a structural fix for the 9 versus 4 confusion, since 9 shares most of its cells with 4. The per-unit weights are larger for 4 because it's sparser, and the size-normalization exponent still favors it, so I'm considering whether equal-total normalization would even that out.

I'm checking whether 9 versus 4 holds up in the sqrt normalization, where 9 actually beat 4. The distinguishing feature should be the closed top of the loop, but the left stroke of a 4 may reach the same top cells, so the template emptiness I was relying on may not be there.

I'm checking whether 9 versus 4 can be separated with a hand-added negative term. The horizontal stroke in the top-left region of the loop should be the discriminator, since a 4 has vertical-ish ink there instead, so I'm considering penalizing horizontal responses at that cell specifically for the 4 template.

I'm considering a hand-added negative term for 4, penalizing horizontal ink at the top-left cell where a 9's loop closes. For 7, a similar negative might target vertical ink at its right side. Rather than adding many digit-specific negatives, I'm also thinking about tuning the general negative-ink weight, which was 0.16 in the earlier step.

I'm checking whether 9's loop top would penalize 4 in the template comparison. The cells at the top-center give 4 little penalty, since its left stroke covers the upper cell and its right vertical covers most of the lower one, so the loop's top barely separates the two.

I'm considering a hand-added negative for 4 on horizontal ink at the top-center, since a 4 never has a horizontal stroke there. For 7, I'm wondering whether a horizontal penalty in the middle would help, though some European 7s have a crossbar, so it may be too risky.

I'm estimating how much of the step 4 blow-up was due to the penalty versus the biases, by checking how the penalty lands on 8 compared with the other digits.

I'm checking whether the orientation penalty hits 8 too, since its sides and top cells also restrict some orientations, so the swing may not be entirely from the penalty. I'll set 8's bias conservatively to 0.0 rather than pushing it further. I'm also thinking about making the orientation filters less responsive to filled blobs by moving their bias from -0.5 to -1.0, which would cut blob responses while keeping ideal strokes strong.

I'm considering keeping the orientation filter bias at -0.5 and instead tuning the hand-added negatives, since changing several things at once would make the effect hard to attribute. I'm also weighing a small negative for 4 on horizontal ink at the top center, where a 4 never has a horizontal stroke. Next I want to check why 3s get labeled as 5s, since 5's top bar and left vertical should be penalized on a 3 input.

I'm weighing the class biases next: I want to lower the bias for 5 and 4, and nudge 3 and 9 and 8 up, since 3 gets pulled into 5 and 4 is over-predicted. Some of the confusion counts (6 into 4, 2 into 4, 8 into 2) suggest a few other pairs are worth checking afterward.

I'm turning to the over-predicted 1s next, where the bias should come down to about -0.3. For the 4 template, I'm planning hand-added negative terms for horizontal ink at the top-center, since a 4 never has a horizontal stroke there and a 9's loop top would otherwise go unpenalized.

I'm adding a few hand-set negative terms for specific digit pairs, and then I'll set the remaining class biases, starting with 0 at +0.8, 1 at -0.3, and 6 at -0.5.

I'm setting the final class biases now, nudging 1 down to -0.3, 0 up to 0.8, and leaving 4, 6, and 7 at -0.5 and 5 at 1.2.
