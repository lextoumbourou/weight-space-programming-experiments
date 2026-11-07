Now 8 is underpredicted, with κ somewhere around 0.35 to 0.6, perhaps 0.48. The result is very sensitive to κ, which is a concern for classes with large templates. I'm thinking the κ fix is too crude, since a scale-invariant approach with per-class bias tuning would be more robust. The loss also went up, which suggests overconfidence from larger logits, so a lower β might help. Next I'm turning to the cosine approach.

I'm weighing a cosine-based scoring, where logits depend on the normalized template and the bias term, though feature norms still vary with ink amount. I'll try κ=0.48 with β=2.0, but these small scalar tweaks are cheap and haven't broken the 67% ceiling. I'd rather combine them with a structural change, since the confusions shift a lot with κ and that makes the template diagnosis hard.

I'm settling on κ=0.47 and lowering β to 2.0, since those are quick checks. I'd still like to add something structural alongside them, though I'll keep this step simple.
