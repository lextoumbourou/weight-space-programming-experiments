I'm working through step 4: the predicted-dog probabilities for cat and dog inputs come out to about 0.244 and 0.365, and converting those to z-scores gives a separation of roughly 0.35, so warm alone leans toward dog with about 56% accuracy. I'm also checking the loss difference of about −0.0016 against the expansion in terms of E[yz] and E[z²].

I'm solving the quadratic for σ from the loss difference and getting two roots, 0.516 and 0.019. I'm taking 0.516, since the smaller root would mean an implausibly tight warm-sum spread. The skew of the distribution makes the Gaussian fit rough, but the resulting class means come out near 2.9 for cats and 4.7 for dogs.

I'm checking whether an exponential-style model fits better: its log-likelihood ratio is linear in the warm sum, with weight 1/μc − 1/μd and an offset from the log of the mean ratio. That gives a threshold around 3.65, while the Gaussian weight is only about 0.068. The probe at weight 0.10 and threshold 6.5 was miscentered, so I'm leaning toward a weight near 0.08–0.10 with a threshold of roughly 3.8–4.

I'm checking the loss numbers with ε=0.1: the first- and second-order terms roughly cancel out to −0.003, which matches the earlier result. With a centered threshold of 3.8 and ε=0.09, the estimate drops to about 0.680, and I'm also looking at ε=0.068.

I'm now weighing the d' estimates for the other features: the first one near 0.4, warm at 0.35, and a third around 0.25 that is probably correlated with the first. If they were independent, combining them would push accuracy toward 62%, but I'm noting that warm and green may be negatively correlated since grass also scores positive on warm.

I'm now testing the remaining color features, with dark, bright, achromatic, and pink as the next probes. Since warm seems to push toward dog and grayness toward cat, I'm wondering whether a blue cast leans cat, which conflicts with my earlier guess. I'm also planning to try a combined linear model with the warm and E weights to see whether the signals add up.

I'm settling on E and warm as the two strongest features for step 5, with shrunk weights of 0.065 and 0.075. If they're independent, their combined separation should push the loss to about 0.657. I'm leaving the green and blue probes aside for now, so this step stays a clean two-feature check.

I'm settling the centre for the combined model: the mean of W is about 3.8, so I'll put the bias at a point that roughly zeroes the mean z, with the skew of W as a possible small shift. That gives a bias of about −1.70 from −0.065×21.7 and −0.075×3.8.
