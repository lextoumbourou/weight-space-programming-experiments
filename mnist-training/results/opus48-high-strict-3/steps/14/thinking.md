Those 1→7 and 8→7 changes roughly cancelled out, and the overall accuracy barely moved, so this anti-bottom change is a wash.

Two steps remain, with step 15 as the final one, and the best result so far is still 41.75%. Step 14 is the experiment slot, and every template edit so far has come out neutral or negative. A mild 3x3 blur on the single-pixel conv1 is one lever I haven't tried, though it's a gamble.

Still weighing whether a mild 3x3 blur on conv1 could help generalization, since the pure single-pixel delta was a big jump earlier and blur was bad then. Any combined bundle of the small tweaks looks net-neutral or slightly negative, so I'm leaning toward using step 14 for one modest experiment and setting step 15 to the best known config.

I'm going to try a temperature-style rescaling: multiplying both the weights and the bias by the same factor leaves every argmax unchanged, so accuracy stays put while the loss moves, and I'm checking what factor minimizes it.

I'm weighing a temperature-style rescale of the logits to see whether it lowers the loss, since the model looks overconfident for only about 42% accuracy. Scaling weights and bias together leaves every prediction unchanged, so I'm considering testing a factor like 1.5 in step 14 and then deciding for the final step.

I'm going to test a temperature change in step 14: keep the step-10 config and scale the weights and bias by 0.75. Argmax stays the same, so accuracy should hold at 41.75%, and I'll see whether the loss drops.

I'm going to test a temperature rescale in step 14: scale the weights and bias by 0.6, which leaves every argmax the same, so accuracy should stay at 41.75% while I see whether the loss drops.

I'm going to set step 14 to the step-10 config with every weight and the bias scaled by 0.7, which keeps the argmax fixed so accuracy stays at 41.75%, and I'll see whether the loss drops.
