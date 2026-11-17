The loss went up by 0.0012 when I applied the −0.4 shift on the top-minus-bottom texture difference, which leaves two readings: the sign is wrong, or there's no real signal and I'm just paying a small quadratic cost. Given σ≈0.25, the size of that increase fits the no-signal case, so this looks like little or nothing to gain. I'm dropping it. Texture contrasts across the centre-border and top-bottom splits don't help either, which is fine.

Next I'll look at other candidate features that might carry signal. Since the vertical-versus-horizontal split mattered, orientation statistics seem promising, and polarity could too: a horizontal edge that is bright above and dark below may behave differently from the reverse. Vertical edges should be polarity-symmetric under mirroring. I'm also listing more candidates to test: fine spots, lines, colour families, smoothness, the reversed Λ−V contrast, and blobs.

I'm weighing a simple shortcut: test each new feature alone with a guessed threshold. But without knowing the medians, a single probe could mislead, so I'm leaning toward adding small weighted features to the combined model instead, since a small bias shift costs little. The catch is that new features have uncertain scale, which makes the loss change harder to read. I'll start with Λ−V, whose rough distribution I already know.

I'm checking whether the λ−V contrast, with its small expected gain, is really the signal or just a side effect of the vertical-versus-horizontal split, so I'll note the small linear and quadratic terms and see if it holds up.

I'm now considering whether the edge channels could be weighted individually, since orientation and polarity gave the strongest signals so far. Under left-right mirror symmetry, several of the eight directions should be equivalent, which would reduce them to about five distinct groups: vertical, horizontal bright-below, horizontal bright-above, and the diagonals.

I'm splitting the horizontal edges by polarity, bright-below against bright-above, and the diagonals the same way, since the mirror symmetry leaves only a few distinct groups to test. To see those separately I'd need to rework the third convolution layer so the channel that currently lumps the two horizontal polarities together gets broken out.

I'm reworking the third convolution so the horizontal edge channels split by polarity, with one channel for bright-below and one for bright-above, and the diagonals get a similar down-versus-up split. That makes the contrast between them directly readable. I'm planning to test the horizontal polarity difference on its own, since the scale is roughly known and a single probe would show whether it carries signal.

I'm weighing whether a coarser-scale edge feature could carry shape information the fine edges miss, since the current probes are all at the finest scale.

I'm considering whether a coarser-scale gradient, computed from pooled brightness cells, could pick up shape differences that the fine edges miss, since I'm thinking about rounder blobs versus leg-and-body outlines. I'd need to free up a few second-layer channels to hold the four directional signs before rectifying and summing them.

I'm considering whether a coarse-scale version of the vertical-versus-horizontal edge split might carry signal. I'd need to repurpose a few third-layer channels to hold the coarse directional energies, and I'm leaning toward probing coarse vertical-minus-horizontal on its own first, since it may track the fine-scale split I already saw.

I'm considering whether polarity matters here, since the horizontal edges could be bright above and dark below, or the reverse. Possible reasons include objects standing on horizontal surfaces versus lit tops, but I can't predict the direction from intuition. Because the test is zero-centred and cheap, I'll probe it first.

I'm now testing a combined vertical-polarity feature: horizontal and diagonal edges weighted by how far they point up or down, so brightness rising downward counts one way and rising upward the other. To build it I'd have to repurpose a third-layer channel to hold that weighted sum of the directional edge maps.

I'm repurposing two third-layer channels to hold the downward-gradient and upward-gradient energies, weighted so their difference tracks vertical polarity. The scale is roughly 0.34 per channel, so I'd expect the difference's spread to be around 0.08, and I'm considering a weight of 2.5.
