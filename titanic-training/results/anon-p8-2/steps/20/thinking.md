I'm checking the values at each point (-0.25, -0.5, -0.8) to fit a parabola and estimate the slope between the first two. That gives a derivative of about -0.0024 with respect to |w|.

I'm settling on x4 = -0.4 from the zero of the fitted curve, which lands the linear model near 0.469. Real Titanic logistic models with good features usually reach about 0.42-0.44, so I need to tune the other features and add nonlinearity. The sex-by-class interaction looks like the strongest candidate, so I'm testing a ReLU term that fires only when female and the third-class indicator are both high.

I'm now working out the expected survival for each group from the model's rough logits: females in third class come out near 60%, females in first and second near 87%, and males in third class near 13%, which matches the data closely. Male first class lands around 40%, close to the observed 37%. The gap is that female third class sits too high, so I want to lower its logit and check how the female first-class case should shift.

I'm reconsidering the interaction term: a ReLU on the female and non-third-class indicator, with a negative weight on the female and third-class unit, plus a shift to x4 = -0.4. That is two changes at once, which I'm accepting for now, though I'm not yet sure x4 really is the third-class indicator.
