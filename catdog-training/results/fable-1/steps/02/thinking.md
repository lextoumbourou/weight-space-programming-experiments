I've found the accuracy is 47%, so the sign looks reversed: the difference is higher for dogs. Cats are predicted more often overall, and I'm considering flipping the sign and checking the per-class counts.

The fit only gets 52.95%, so the signal is weak, and the loss gap implies a spread of around 0.15 with the mean of z slightly negative. The ear idea doesn't hold at this level, so I should try other feature families next.

I'm weighing which feature family to test next, and I'm leaning toward green regions like grass, since I'd expect them to correlate positively with the label. I still need a threshold for the green feature, so I'm estimating it from the median of its values.

I'm guessing a threshold of about 0.08 for the green feature, with a weight of 2, since the median is likely small. Once I set that, the z values should land roughly between -0.16 and 1.84. Testing every family at once would confound the effects, so I'll probe green on its own.

I'm planning to probe the remaining feature families one at a time, since combining them would muddle the effects. For the next probe I'm thinking about using a small weight so that the quadratic term stays negligible, which should let me read the loss change more cleanly even without knowing the threshold.

I'm weighing whether to probe the median directly or lean on the confusion matrix, since the accuracy still carries signal even if the split lands anywhere between 30 and 70 percent. I'm also considering a small weight so the quadratic term stays negligible and the loss change reads more cleanly.

Rather than mixing two features into one probe, I'll keep them separate: the confusion counts and the loss each carry only one feature's signal, so I'm going through the remaining families one at a time and choosing thresholds from reasonable guesses.

I'm weighing a few ways to test the remaining features, including probing a feature difference like bright minus dark, and I'm leaning toward a green probe first. Since the final choice is the lowest-loss step, pure one-at-a-time probing looks fine for now.

I'm estimating the green feature's values: indoor scenes sit near zero after the rectified green-minus-average-of-red-and-blue signal, so the median is probably around 0.03 to 0.06. For grass-heavy images it would reach 0.3 to 0.8. I'll set the threshold at 0.06 with a weight of 3.

I'm going to probe the green feature next, using channel 10 with weight 3 and the threshold I estimated, and I'll keep the rest of the model unchanged so the effect stays readable.

Just fixing the bias term for the green probe: with weight 3 and threshold 0.06, the offset comes to about -0.18.
