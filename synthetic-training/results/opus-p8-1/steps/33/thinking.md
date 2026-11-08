I'm checking the x7*x4 product value and working out the signal from its components. The covariance numbers don't reconcile yet, so I'm trying to pin down how the pair covariance relates to y.

I'm dropping the two weakest single-variable terms, |x1| and |x4|, to free up four units for probing additional pairwise interactions, since those are likely to give more gain than the terms I'm removing. I'll restore them later if the budget allows. I'm also setting the scale s to -0.9 before running the next probe.

I'm weighing whether to switch the scale and drop the two weakest terms in one step, or keep the change clean and make the base change alone. I'm leaning toward combining them anyway, since the baseline shift looks small enough to accept.

I'm estimating the gain from the new scale and from dropping |x1| and |x4|, which puts the baseline near 0.457 and the null probe cost around 0.470. I'm then settling on s = -0.8 rather than -0.9, since that sits close to the optimum and keeps the uncertainty down.
