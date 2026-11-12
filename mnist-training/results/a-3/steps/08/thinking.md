I'm at 72.9% and looking at what to try next, mainly using the 8 conv2 channels that aren't being used yet. One idea is a second set of edge channels with taps shifted by one pooled cell, which would offset the sampling grid by 2 px and give finer localization.

I'm weighing a second shifted set of the 8 edge channels, sampled on a grid offset by one pooled cell, as a way to add finer localization. Looking at the confusion pairs, 7 vs 9 hinges on the top loop, so edge features in that region should help separate them.

I'm adjusting the biases for the new feature set, nudging each one by a damped fraction of the log ratio between predicted and true class counts. Digit 0 comes out around 0.25, 1 near -0.38, 2 about 0.65, 3 around 0.72, and so on.

Keeping the 0.5 damping, I'm revising the remaining biases: 8 drops to about -0.52 and 9 to about -0.56. I'll also halve the temperature from 0.25 to 0.12, since 256 features will make the naive model overconfident.
