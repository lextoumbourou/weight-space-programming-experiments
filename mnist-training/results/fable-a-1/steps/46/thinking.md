The loss is down to 0.3140, with 91.09% accuracy, a small improvement. With five steps left, I'm weighing which knobs to test: GAMMA for the hole, plus G_D and GAMMA_C. The gains per step are only around 0.003, so I want to order the tests by expected payoff, starting with G_D.

I'm weighing the remaining options: GAMMA_C at 0.25 looks like a probable small gain, while the G_HV move is a coin flip since the optimum is unknown. Given only five steps left, I'm leaning toward a deterministic bias refinement from the column sums, since that should yield a more reliable small improvement.

Working through the per-class prediction counts against the true labels, I'm computing how far each class is over- or under-predicted. Several classes are off by 30 to 45 predictions, so I'm working out small bias offsets for each class to even them out, even though that won't be exactly optimal for the loss.

Next I'll bundle the bias refinement with GAMMA_C at 0.25, then test G_D, GAMMA, and G_HV in the remaining steps before picking the best combination.
