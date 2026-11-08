Looking at a split on feature x12 at 0.475: it sends 176 samples one way (69 of them positive, about 39%) and 424 the other way (161 positive, about 38%). The rates are nearly identical, so this split looks neutral, and I'm wondering whether the relationship with age is non-monotonic.

Now I'm guessing which Titanic features the anonymous columns might correspond to, matching their survival rates against Miss, Mrs, Pclass, and Embarked groups. I'm also estimating a rough standardized logit effect for each single feature, though the x10 comparison works out to zero.

I'm estimating standardized logit effects for the remaining features, working each one out from its survival-rate gap and the spread of the binary split: x10 comes out near 1.11, x1 near 0.63, x9 near 0.66, and x4 near -0.70. Then x5 looks like roughly 0.5, and x2 comes out smaller at about 0.32.

Now I'm checking the standardized effects for the rest of the features, and most of them come out small. Sex still looks dominant, and the pclass dummies overlap, so I'd expect those coefficients to shift once they're combined.

I'm starting a combined logistic model with rough hand-picked weights: a strong positive weight on x10, negative on x4, and small values for the rest. I still need to pick an intercept so the average prediction lines up with the base rate.

Next I'm setting the weights for a combined logistic model and deciding on an intercept near -0.6. Then I'll tune each coefficient against the loss, and later use the spare hidden units to capture things like sex-by-class interactions.
