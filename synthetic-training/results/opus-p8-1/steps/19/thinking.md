I'm dropping x9, since 0.5198 against 0.519 is a null difference and the marginal effects look small. Next I want to check interactions, using a product approximation on the uncorrelated standard normals and looking at how the absolute-value terms covary with ab.

I'm checking the covariance of the interaction probe with ab: the term works out to about 1.128, and with its variance of 1.45 the correlation with ab comes to roughly 0.94. Next I'm planning a group test over the pairs, since the six null features might hide an XOR-type interaction.

I'm planning to test the null features in groups of pairs, since a single strong XOR-type interaction could hide among them. I'll hold off on the exact weights until I've settled the pairing.

I'm weighing a group test over the six null features, with random sign weights, instead of checking all 15 pairs one by one. I expect the group version to dilute each pair's signal, so the cost savings come with some loss in sensitivity.

I'm weighing a group probe on all twelve free features with unit weights, but the dilution across 66 pairs makes that look weak. I'm leaning toward a single group test on the six null features with all weights set to one, accepting that its effect on any one pair is about a third of a direct probe.

I'm settling on a single group probe over the six null features with alternating signs, and I'll compare the loss between the two sign patterns to see if any pair stands out. I'm keeping the scale at 0.7 so the quadratic cost doesn't swamp the signal.

I'm scaling the group probe by 0.7 so its signal stays visible against the quadratic cost.
