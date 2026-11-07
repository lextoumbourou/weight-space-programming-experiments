I need step 28 to reach at least 73.77, since that's the bar for the run to continue, so I want step 28 to be strong no matter what. For step 27, I'm weighing the options: switching the 9 to 7 helps the 7 stem but costs the 9 stem a lot, and 0 looks worse than 3 at this sigma.

I'm weighing a combined setup for step 28: either the step 26 sigma of 3.6 or 3.9, since 3.9 pulled down the 0s. Trimming the bias for step 26 would only give about +0.1, which isn't enough to clear the +0.35 I need, and keeping the 9-for-7 anti-weighting at half strength is risky because the 9 is already under-predicted by about 200.

I'm considering whether a few template tweaks for 5 and 6 or a per-class mixture for 9 would give the gain I need. Real 5s open to the left, so a ring detector might help there, but the 9 stem variants aren't clear yet. Safest bet for the +0.35 looks like combining step 26's setup with σ 3.9, only for the classes that gained from it.

I'm settling on per-class blur: 3.9 for the 2, 3, 6 and 8 templates, and 3.6 for the rest, since those classes gained from the wider sigma in step 27. The expected gain is roughly +0.5%, which would land near 73.9. The catch is that changing a template's blur also shifts how other classes score against it, so I still need to check those cross-class effects.

I'm dropping the 9's anti-weighting on the 7 stem, since it nets out negative. Per-class blur will be 3.9 for the 2, 3, 6 and 8 templates and 3.6 for the rest, with the 0 template's ry changed to 5.5.
