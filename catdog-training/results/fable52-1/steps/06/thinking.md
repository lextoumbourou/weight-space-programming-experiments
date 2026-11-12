I'm checking the metrics at step 5: loss is around 0.665 with accuracy near 60%, and the predicted dog fraction is a bit above half. Per-class rates and the d' score come out to about 0.5, which I'm comparing against the independent baseline. The loss sits just under the chance value of 0.693.

I'm working through the quadratic for the scale parameter, where the two roots come out near 0.56 and 0.37. The optimum sits around σ ≈ 0.47, so the current scaling is close to ideal and rescaling would only gain a tiny bit of loss. The mean offset suggests a small bias shift of about −0.08, which is also negligible. I'll move on to adding features, testing green and blue next, using this calibrated base.

I'm weighing whether to probe new features on top of the calibrated base model or test them in isolation. Adding a feature with weight ε shifts the mean and variance in predictable ways, so the change in loss and d' should tell me whether green or blue actually helps.

I'm weighing how to set up the next probe: testing features on top of the calibrated base, where the loss change tells me directly whether a feature helps, versus testing them in isolation to get their individual statistics. On-top looks more direct, though the mean and variance estimates for weak features may be noisy.

I'm settling on isolated probes for the next batch of features, green and blue among them, since the independence assumption should hold for features of different types. I'll fold the combined checks in periodically to verify each one.

I'm weighing whether to test features in isolation or add them directly to the calibrated base. Isolated probes give cleaner statistics, especially since I can't reliably guess the scale of weaker features, so I'm leaning that way for the next batch.

I'm laying out the next batch of probes: isolated tests for green, blue, dark, bright, achromatic and pink features, plus some shape and texture contrasts. With about 45 steps left, I'm budgeting roughly 18 isolated probes and 8 combined checks, keeping the rest for scale, bias and spatial profiles of the stronger features like E and W.

I'm now planning to test green next, starting with a threshold on the summed green signal, since that feature is mostly zeros and a small cutoff should split the classes.

I'm looking at the green signal next, which is mostly zeros, so a simple threshold probe on its summed value won't fit a Gaussian well. Instead of estimating its second moment from rates, I'll add green straight onto the calibrated base model with a small weight and read the change in loss directly.

I'm going to keep the base model exactly as it is and add green on top of it, so any change in loss comes purely from green. Green is sparse, with most images at zero, so testing it directly on the calibrated base is more reliable than fitting a Gaussian to it.

I'm going to add green on top of the base model, keeping the base's bias fix and using a sparse profile with weight around 0.12. Most images have little or no green, so any loss change should mostly reflect green's contribution.

I'm setting the bias for the green probe: subtracting the baseline offset, and centring green's sparse signal around a guessed mean of about 0.4, which puts the bias near −1.84.
