The green feature helps only a little, and the model leans too hard toward predicting cat, so I'll increase the weight and lower the bias. I want to test one more feature per step while keeping green. To balance things, I'll set the bias to 0.05 and -0.05, and raise the weight to 0.3 so the effect is bigger.

Now I'm weighing whether to test texture alongside the color change, since testing both at once would muddy which feature drives the result. I'm leaning toward keeping the test to green by rescaling the weights, even though that spends a step, and setting the bias to zero to see how the predictions split between cat and dog.

I'm weighing how far to push the bias and weight so the threshold lands near 0.02, and I'll also consider adding a texture probe alongside green, even though that would blur which change is responsible.

I'm weighing whether to add a texture probe next to green, but testing both at once would blur which feature changes the result. Since my scaling is uncertain, I'll keep this step to green alone and calibrate it carefully.
