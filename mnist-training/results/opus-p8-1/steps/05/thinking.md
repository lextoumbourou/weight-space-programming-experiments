The bias of 0.9 is shifting too many predictions, which suggests the logit margins between classes are small, so the biases dominate. Raising alpha should widen those margins, and I'll bring the biases down to something like 0.3. The loss of 1.29 at 62% accuracy looks under-confident, so I'll try alpha=15 with that lower bias.

I'm also going to change the ink channel weight to 0.2, since the features look too similar across digits and it may be dominating the cosine.
