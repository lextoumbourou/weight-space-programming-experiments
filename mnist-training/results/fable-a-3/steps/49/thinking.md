I'm at a loss of 0.2648 and 91.89% accuracy, with the temperature change and bias adjustment having already helped. Two steps remain. Next I'll try a temperature of 1.45 while keeping the biases; if that improves things, I'll consider a further push or a bias tweak, and if not, I'll settle on an interpolated temperature around 1.35.

I'm checking T=1.45 with the biases kept. Since the extra bias is scaled along with the temperature, accuracy should stay at 91.89% and only the loss should move, which makes this a clean test.
