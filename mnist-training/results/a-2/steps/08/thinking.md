Best so far is 66.4% with a loss of 1.088, so the framework looks calibrated and I can move on to improving the templates and per-class biases. The biggest error pairs are 7 to 9 (368 cases), 5 to 6 (277), and 7 to 2 (175), followed by several smaller confusions. I'm now starting to work out bias adjustments from the log ratio of predicted column sums.

Now I'm working through the per-class column sums and the log ratios that go with them, with the predicted totals running high for 1, 2, 6, 8, and 9 and low for 0, 3, 4, 5, and 7.

I'm now testing the 7-versus-9 template shapes, checking whether the loop feature in the 9 template separates them cleanly.

Looking at the 7-versus-2 confusion, the 2 template's bottom stroke at y=22.5 gives a high chance of a stroke there, and since 7s lack that stroke, the penalty is only mild, so the real cause is likely a 7 diagonal that lines up with the 2's slant. I'm not sure how much the loop feature on the 9 template will help, since the loss depends on how reliably that detector fires. Better templates probably need more accurate reference shapes, so I'll try recalling typical MNIST mean images.

I'm picturing the mean "7" as a bright top bar with a stem running down and leftward, at roughly 17 degrees off vertical. My template's stem is steeper, closer to 23 degrees, which is still reasonably close. The stem sits between the vertical and the diagonal tuning channels, so both would respond partially, and with the threshold the response probably fires for both.

I'm weighing blind template tweaks against gathering per-class statistics through probing, and the second looks more reliable than guessing at MNIST mean shapes.

I'm thinking about probing with binary-encoded logits, where a few binary features map to joint states across the ten classes, so one confusion matrix could recover several feature probabilities at once instead of one per step.

I'm weighing whether a binary-encoded probe could recover several feature statistics at once, with the prediction counting how many features are active across a chosen set, though the exact logit design still needs working out.

I'm weighing whether probing for per-feature statistics is worth the bandwidth, since each step only yields a count histogram or a joint state of a few features. Probing for loop detectors on 8, 9, 6, and 0 would be a useful diagnostic, but encoding even three features per step covers just eight combinations. I'll likely accept the current approach and make sensible template tweaks rather than rely on these probes.

I'm now considering whether the 7-to-9 errors come from the 9 template's loop detector rarely firing on real 9s, which would leave the 9 template matching mainly on orientation. Since 7s get pulled toward 9 so often, the 7 evidence may be weaker than the 9 evidence rather than the other way around.

I'm settling on bias corrections to fix the 9 over-prediction and 7 under-prediction, and I'll pair that with a few tweaks to the 7 stem, blending two slants so it sits between the vertical and the diagonal channels.

I'm weighing whether the 5-versus-6 and 3-versus-8 confusions come from the loop or the open-left shape of the bottom arc, and I'll also try a small bias correction plus a blended 7 stem, since bias alone has only helped a little.

I'm going to adjust the per-class biases to counter the over-prediction of 9 and under-prediction of 7, using the same factor as before, and also tweak the 7 template's stem. Since changing the 7 template shifts its logits, the bias correction for 7 may end up slightly off, but I'll accept that. I'll also check the regularization weight later, since λ around 0.3 might be better.
