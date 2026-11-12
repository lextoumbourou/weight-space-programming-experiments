Going back to the step 6 setup, since that version scored better than the newer tweak, which dropped the tips and did worse (210 to 250). I suspect the second-loop variant or the tips were the cause, so I'll restore the step 6 config exactly before trying something else.

The bigger limit is that hand-built templates with cosine similarity seem to top out around 70%, so the weights need to be more discriminative. One idea I'm weighing is pairwise adjustment: for the pairs that get confused, shift the weights of each class away from the other.

Looking at the pairwise idea more closely: with centered templates the sum over other classes collapses to a multiple of the class's own template, so only the pair-specific terms matter. That means boosting the 2-vs-3 difference in each direction. I'm also wondering whether the real bottleneck is the hole features themselves, since thick 6s with filled loops may be slipping past the detector.

I'm weighing pairwise weight adjustments for the most-confused digit pairs, since centered templates make the pair-specific terms the only ones that matter.

I'm weighing pairwise weight adjustments for the most-confused digit pairs. The idea is to shift each class's weights toward its own template and away from its confusable partner, with the step strength scaled by how often that pair is confused.

I'm thinking about the pairwise weight idea: nudging each confusable class's weights away from its partner, scaled by how often that pair gets mixed up. I also want to check whether the hole detector is missing small or filled loops in thick digits, since that could be a bigger problem than the weights.

Next I'll drop the tip channels and go back to the step 6 setup, then add the pairwise boost: for each confused pair, nudge the two classes' weights apart along their full feature difference, scaled by how often they get mixed up.
