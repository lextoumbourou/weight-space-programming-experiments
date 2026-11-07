The 0.25 learning rate overshot: the run got worse even with the bias changes, so I'm dropping back to 0.15, which is where the gain was. I'll keep the step-16 biases and half the bias corrections. I'm also thinking about adding early stopping that compares against the score from five steps back.

Now I'm weighing whether 16 at 76.19 is the reference point for early stopping, since the rule seems vague. I'll keep improving the classifier anyway. Next I want to look at why 3s and 5s get confused, and why many 5s land on 8.

I'm adding a 5 template with a bigger, slanted bowl to see if it reduces the 5-to-8 confusion. I'll run it with the 0.15 rate, the step-16 biases, and half the bias corrections.
