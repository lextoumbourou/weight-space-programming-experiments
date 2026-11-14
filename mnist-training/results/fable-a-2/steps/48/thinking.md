Step 47 came out worse than step 42, so I'm reverting to the step 42 config as the base. That leaves three steps (48, 49, 50), and I'm considering running step 42's config at a scale of 0.44 with scaled biases plus small bias tweaks.

I'm weighing the three remaining steps: either rerun the step 42 config at a scale of 0.44 with scaled biases and small tweaks, or tune GLINE, GAMMA, or ALPHA with single tests. I suspect the centre terms hurt because they double-count cells, which might mean the line weights are already too heavy, but earlier additions of side terms helped, so that explanation doesn't fully hold.

I'm planning the last three steps on top of the step 42 config. One option is to run it at a scale of 0.44 with scaled biases, which should be a small safe gain. The other is to spend the steps on single group-weight tests, such as raising GAMMA, and I'm weighing how to combine those with the scale change.

I'm fitting a parabola through the three scale points to locate the optimum, and solving the linear system gives A ≈ 1.945 and B ≈ −1.736, putting the best scale near 0.446.

I'm working out the fitted optimum from the three scale points: the parabola bottoms out around 0.446, with a predicted score near 0.367. Step 48 should therefore be the step 42 config at a scale of 0.445, keeping the small bias tweaks. After that, step 49 is still open: GAMMA at 0.8, ALPHA at 6, or a GLINE change at 0.7 with a scale adjustment.

I'm considering whether the loci terms are underweighted: at an effective GAMMA of about 0.27, they seem low compared with the line terms, so I'm thinking about testing GAMMA at 0 to see if the lines should give way to the loci.

I'm thinking the loci terms have been under-weighted since the line terms were added, since the overall scale dropped from 1.0 to 0.4 and dragged them down with it. Their effective weight is now about 40% of what it was when they were first set, and that setting was never tuned. The template weight may be similarly low, so the next test could go either way.

I'm considering raising GAMMA to 1.0 and ALPHA to 6 together in step 49, since the loci and template weights were set when the overall scale was higher and may now be too low relative to the line terms.

I'm weighing a combined move for steps 48 and 49: first run the step 42 config at a scale of 0.445 with GAMMA at 0.85 and ALPHA at 5.5, then compare the result against the predicted baseline of about 0.367 to isolate the effect of the group-weight changes.

I'm going with a combined move for step 48: the step 42 config at a scale of 0.445, with GAMMA raised to 0.85 and ALPHA to 5.5. Since the scale-only baseline should come out near 0.367, any deviation from that will show how much the group-weight changes help or hurt. If it comes out worse, the last two steps can fall back to the plain baseline and try the opposite direction.
