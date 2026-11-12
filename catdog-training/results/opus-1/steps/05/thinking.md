The predicted cat share is now 73%, which is too much cat. The earlier centering step was balanced with a cat-leaning texture shift and a small dog-ward bias difference, but the bias difference has now swung to +0.5, pushing things toward cat. I'll bring the bias difference back to 0 to rebalance.

I'm nudging the bias difference from 0.5 down to about 0.4, since my rough estimate puts the balance point there. I'm also thinking about raising the texture weight to 0.1, which would shift the balance further toward dog, so I'd need to recenter the bias to offset it.

I'm weighing whether to probe edge channels or red-blue colour as well, but I'll stick with one change at a time and keep the current plan.
