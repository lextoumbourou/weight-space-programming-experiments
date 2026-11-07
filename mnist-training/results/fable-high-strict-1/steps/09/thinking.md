Still getting 8 over-predicted, around 3464 predictions. Even a small shift on that class swung things a lot, and the template change for the ellipses lowers the squared norm of that template, which shrinks the penalty. Looking at the column totals across all digits, 8 stands out far above the rest, and it's clearly tied to how sensitive the result is to the offset.

I'm weighing whether 8's offset should be around 1.0 instead of 0.95, since the ellipse template has a smaller norm that shifts the predictions a lot. I'll set the multipliers back near 1.0 for most digits and lower 0 to 0.9.

Dialing back most of the multipliers to around 1.0 and pulling 0 down to 0.9 looks like the quickest fix for the calibration swings. Beyond that, the bigger gain would come from improving how well the templates separate the classes. One idea is to penalise orientation features that a digit doesn't contain: for example, a 1 has no horizontal strokes, so horizontal activity anywhere would count against it, and similar cues might separate 4 from 9 or 7 from 1. That could help discrimination, though it may also favour 8, since it has the most features and therefore the fewest penalised cells.

I'm considering normalizing each class's weights so they sum to the same constant, possibly zero, so that mass differences stop driving the predictions and only the pattern separates the classes.

I'm checking whether centring the weights across all 256 cells, rather than per map, would keep the class penalties balanced, since the offset then tracks each template's total mass differently for dense and sparse digits.

I'm weighing whether to pin the 8 multiplier near 1.0 and bring 0 down to about 0.9, since the ellipse template has a lower norm and shifts the predictions a lot. Rather than keep tuning those multipliers, I'm thinking about adding a mild penalty on orientation channels a digit lacks, though that could tilt the balance toward 8 again.

I'm thinking about whether an offset that scales with the total ink (Σx) makes the penalties too strong for thick, dense digits. A fixed bias would avoid that, though it would adapt less to each image. For the 8 over-prediction, I'm considering nudging its multiplier to about 1.03, with some risk of overshooting in the other direction.

I'm working out the offset for class 8 by interpolating on a log scale between the two earlier results, which lands at about 0.985. For class 0, the earlier step gave 667 predictions and the newer template with its larger mass gives 624, so it should come down to around 0.9.

Working out the remaining per-class multipliers by interpolating between the two earlier calibration steps: class 0 comes down to about 0.88, class 6 lands near 1.01, and class 5 near 1.02. I'm still estimating class 9 from its step-6 count of 1213 and step-8 count of 638.

Working out per-class multipliers from the last two calibration steps, I'm interpolating on a log scale toward a target of about 1000 predictions per class. Class 2 comes out near 1.044, and class 3 near 1.027. Class 4 needs to come down to about 0.93 since it's currently over-predicted.

I'm nudging the multipliers for the remaining classes toward a target of about 1000 predictions each, and class 1 holds near 0.99. I'm treating these as rough estimates, since the classes compete with each other and one change can shift the others.
