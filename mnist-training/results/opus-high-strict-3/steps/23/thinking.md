The result suggests the contrast direction is reversed for the 5-to-8 comparison, which is odd. The B-side regions keep winning, so I'm wondering whether my x and y indices are transposed, since that would only partly work and could explain a 70% accuracy.

I'm checking whether left-right mirroring could explain it, but the 7 at 86% argues against that. The shear offsets look fine too. The likelier culprit is blur: at 5 pixels, the B region picks up the top bar of the 5 and smears it in, which would cancel the contrast I expected.

I'm realizing the blur is what's washing out the parts, since at 5 pixels the B region picks up the 5's top bar. So I'll switch to a smaller blur for the parts, around 2.5, and recompute the pairs with that setting. I'll keep the oriented values at 0.35 and use the region version at 0.5, applying the sharper blur to the 5-vs-3 and 5-vs-8 comparisons.
