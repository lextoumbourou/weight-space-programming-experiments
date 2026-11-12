Testing the +0.07 step with the ^ term added, the loss rose from 0.6587 to 0.6608, so the ^ direction makes it worse. The predicted-dog fraction moved from 50.1% to 52.2%, which is a small bias shift whose effect on loss is negligible at about 0.0001. The quadratic model L(ε) = L0 − gε + ½hε is what I'm checking this against.

Ruling out the ^ direction now: its residual effect on loss, once energy is accounted for, is tiny, so I'll drop it. The lesson is that energy-like features are redundant, and I need to look at different feature families next, such as color, brightness, and spatial distribution.

Next I'm weighing whether to probe blue, dark, or bright luminance features, with a leaning toward dark since indoor flash shots might fit a cat-like pattern. For the probe itself, I'd rather apply a uniform blue weight across the whole image than a sparse top-row patch.

Next I'm weighing a dense probe on dark luminance: I'd apply it at a small weight on top of the current model, since that makes the bias shift easy to correct and any loss change directly shows whether it helps.

Weighing whether to probe the dark luminance feature next, since it might separate the classes, though I'm not sure which direction it would point. Testing it on top of the current model at a small weight would reveal the sign and whether it helps, at the cost of possibly needing a follow-up step to flip it.

I'm weighing whether to test the dense features on top of the current model, since the bias shift can be corrected afterward, or to probe each one in isolation first to get its mean and variance. Isolated probes would take more steps per feature, but with 43 steps left and roughly a dozen candidates, I'm leaning toward the faster on-top approach and only computing the gradient from the loss change if it goes the wrong way.

Now I'm thinking about whether to rely on the on-top approach for the remaining dense features, since each one needs only a step or two, and then spending the leftover steps on tuning the main features and trying a clipped version of the strong ones.

I'm now weighing a luminance probe on the dark features, guessing that darker images lean cat, and I'd test it with a small negative weight on top of the current model.

I'm weighing a luminance probe that pairs dark and bright features, on the guess that dark leans cat and bright leans dog, with the bias shift left to be sorted out afterward. Then I'm dropping the ^ term and resetting to the step-6 base, where the loss sat at 0.6587 and the dog fraction was 50.1%.
