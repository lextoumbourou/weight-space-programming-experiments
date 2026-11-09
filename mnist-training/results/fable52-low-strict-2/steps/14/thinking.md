I'm weighing the gain values here: a gain of 6 seems to slightly raise accuracy but also pushes the loss up, while 11 looked bad too, so I'm narrowing in on something around 8 to 9 and checking that with a rough quadratic fit on the loss numbers.

I'm fitting a parabola to the loss values around the gain setting, and the vertex lands near 7.3, so 7.5 looks like a reasonable pick since the curve is nearly flat there. Next I'm checking the per-class prediction counts against the true counts, where class 1 has the largest excess and class 4 the largest deficit.

I'm settling on a gain of 7.5 and making small per-class bias adjustments, nudging class 4 up and a few others slightly, then scaling those values by gain over 8 to match the new setting. That seems like a safe step, and I'll pick the better option from there next.
