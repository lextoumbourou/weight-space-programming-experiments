I'm thinking about adjusting the model with modest, one-at-a-time changes, since there are still 49 steps to experiment with. The confusion counts show it's slightly underpredicting survival, with more false negatives than false positives, so I'm considering raising the base a little.

I'm weighing a few small adjustments: raising the bias a little to address the false negatives, and adding a child-in-second-class feature with its own weight. I'll also scale back one existing unit's weight to keep the changes moderate.
