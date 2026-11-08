I'm noticing accuracy shifts with the gain, since the bias stays fixed while the scale moves the threshold. A gain around 1.0 to 1.2 looks best, and I'm wondering whether the intercept should be more negative, because at gain 1.5 it predicts class 1 more often (405 versus 369). I'm now starting to think through the loss function.

The loss curve over gain is a parabola, with values at gain 1.0 and 1.5 but no third point yet. Rather than keep tuning the scale, I want to check for nonlinear structure, since that is where larger gains tend to come from. Testing it means adding a nonlinear term per feature and seeing whether the loss drops, or grouping several terms in one probe to save work.

I'm settling on a probe for nonlinearity: adding a scaled term of each feature's absolute value centred on its mean, with the coefficient set to 0.5. I'm weighing whether to test the features one at a time or as a group, since a group result could be ambiguous, and I'm leaning toward testing them individually, starting with x0.

I'm settling on the individual testing approach, since the confusion matrix isn't much help here. For each feature I'll add a |x| term, built from two ReLU units whose sum is the absolute value, with the bias offset to center it. Asymmetric nonlinearity should show up too, since the linear term already covers that side, so I'm starting with x0.
