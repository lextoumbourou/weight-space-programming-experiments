I'm checking how the loss changes with scale: it's 0.5164 at 1 and 0.5242 at 1.4, so scaling up made things worse. The optimum seems to sit near 1.1, and I'm fitting a quadratic through the points, including the unknown value at zero, to pin it down.

I'm verifying the quadratic fit: solving the two equations gives c≈0.124 and b≈-0.279, putting the optimum near scale 1.12 with loss around 0.5145, which is only a marginal gain. Next I'm considering nonlinear probes on the features that looked irrelevant, like x0 with its higher-than-expected loss, and whether pairwise interactions could matter, and I'm thinking about how to probe |x| terms efficiently without the combined result becoming ambiguous.

I'm weighing a group strategy for probing the |x| terms, since probing all twelve features and then all pairwise interactions one at a time would take too many steps. Grouping the candidate features and bisecting on a significant loss change could cut that down, though mixed signs might cancel out.

I'm now weighing a group probe for the |x| terms of the six features that looked null, using a small weight so the expected effect stays readable.

I'm weighing whether to probe the |x| terms individually with a stronger weight, which would give clearer signals at the cost of more steps. I'm leaning toward a group test on the six null-looking features, then bisecting if it shows a significant change, and I'm not sure mixed signs wouldn't cancel out.
