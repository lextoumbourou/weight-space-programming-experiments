I'm at 74.4% and considering two small adjustments, checking the column results so far. Next I'm thinking about adjusting the logit scale for the loss and testing s=12.

I'm weighing a scale change: setting s to 12 and multiplying the biases by 1.2 would leave the argmax unchanged while showing whether the loss improves. I'm also planning a few small bias tweaks, like lowering class 1 by 1.4 and raising 4 and 5, before running that scale experiment.
