The small +0.014 effect is near the noise floor, so nonlinear probing doesn't look worthwhile. The data may be close to linear, which points toward refining the coefficients and intercept directly. I'm planning a coordinate-wise refinement, where each coefficient's loss is approximated with a quadratic using an estimated curvature of about 0.17.

I'm estimating the curvature of the loss for each coefficient, which would let me pick a step size from a single probe per feature. The variance-based estimate gives roughly 0.2 for standardized features, and the correlations between features make that only approximate. I could instead use two-sided probes for better accuracy, though I'd spend more of my budget that way.

I'm weighing whether simultaneous random-sign perturbations would be worth it, but I'm leaning toward sticking with one coefficient at a time as my own iterative process. I'll start with the first feature and probe it at +0.3.
