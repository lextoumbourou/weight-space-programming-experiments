The concern is that one token is getting disproportionate weight, which tilts the overall balance. Adjusting the bias terms to offset it is possible, but the size of the shift is hard to predict. A cleaner route might be to make each correction sum to zero so the total stays balanced.

I'm weighing whether to offset each class's shift by subtracting its expected feature contribution, using the hand templates as a rough proxy since I can't measure real feature values here. The scale is uncertain, so it's a guess, but it would keep the total balanced. I'm leaning toward trying ETA=1.0 with that compensation, even though each failed attempt costs steps.

I'm checking whether the compensation scale holds up, specifically whether the bias shift for class 8 is reasonable once I apply the template-based correction.
