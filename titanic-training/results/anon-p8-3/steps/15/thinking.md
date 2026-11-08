The model is over-predicting class 1, with 263 predicted against 230 true at a loss of 0.4735. I'm considering lowering the intercept to -0.8 and possibly making x12 negative, but I'm wondering whether changing both at once would muddy the signal, so I'm leaning toward adjusting the intercept first. The over-prediction could also come from the coefficients or from the decision threshold.

I'm going to try setting the intercept to -0.8 and see how the loss responds.
