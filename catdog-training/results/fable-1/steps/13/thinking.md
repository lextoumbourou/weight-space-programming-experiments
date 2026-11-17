The loss dipped slightly worse while accuracy edged up to 61.4%, so these changes didn't clearly help. The cause could be that the weights overshoot, or that Λ−V adds noise alongside the other features, since it may be correlated with texture. I'm now going to switch to a more disciplined coordinate search over the parameters, starting with w_T and w_VH.

I'm weighing whether the weights overshoot, since the individual optima for T and VH may overlap when combined, so I'll check the joint scale against the S9 baseline before changing anything else.

I'm checking whether the scale-up could have cost much. Along T the curvature is small, so moving 0.2 from its optimum costs only about 0.0004; along VH, moving 1.0 costs about 0.0007. Even if S9 sat right at the optimum, the weight changes can account for at most about 0.001, so the Λ−V term, adding roughly 0.0028 of variance for little gain, looks neutral to harmful. That points toward dropping Λ−V with a=3.

I'm dropping Λ−V, since the weight changes can account for only about 0.001 of the loss and the feature adds more variance than it returns. Weak features aren't helping here, so I need ones with a real independent signal. Colour statistics and background cues look like the most promising candidates, though I can't yet tell how well they'd separate the two classes.

I'm wondering if the pose matters more than I'd assumed, since dogs tend to stand upright in photos while cats lie flat, so the V/H balance might be capturing posture. Orientation energy at a coarser scale could track body shape better than the fine fur-level edges, which look fairly random. I'll build coarse orientation channels from the brightness map using a wider derivative-of-Gaussian filter.

I'm building two more scales of orientation energy: a mid-scale from the pooled brightness map and a coarser one from the conv3 polarity channels, which I can combine linearly in the final layer.

I'm setting up the mid-scale orientation channels: brightness pooled 2x2, a derivative filter with gain about 2, and the vertical and horizontal sums on the conv3 level, which should give a usable pose signal.

I'm sizing up a single-scale probe: the mid-scale orientation difference z = 2·(V_m − H_m) on its own, then the coarse one the same way, to see how much each adds beyond the fine edges.

I'm going to test the mid-scale orientation energy on its own before adding it to the model, so I can see its spread and how well it separates the classes. The plan is to build it from the conv2 gradient channels, pooled over the brightness map, and then combine the vertical and horizontal sums at conv3.

Still writing the coarse-scale orientation channels...

Now I'm planning a probe of the mid-scale orientation signal, z = 2.5·(V_m − H_m), built from the conv3 channels I identified, to see its spread and separation before adding it to the model.
