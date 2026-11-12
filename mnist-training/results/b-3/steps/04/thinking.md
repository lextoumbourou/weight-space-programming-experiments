The distance model looks overconfident, and the alpha guess might be off too. Hand-drawn templates feel limited, so I think the features need a more fundamental rethink. The real bottleneck is that the features are just coarse orientation density and the templates aren't learned from data; good hand features might reach 85-90%. Class 4 is the weakest by far, with only 37 correct, so its template is probably the problem. A 4 has an open top with a vertical left stroke, a crossbar, and a long right stem, while a 9 has a closed top loop, and I should build features that separate those.

I'm considering whether to keep the correlation approach as the base and add more discriminative weights, or to combine it with a partial penalty term. The last variant helped some classes and hurt others. I also wonder whether the conv1 bias and zero-mean kernel are erasing thick strokes, and I'd like to adjust the templates per class based on the confusion pairs, such as 4 versus 9 and 8 versus 6.

I'm weighing whether a discriminative weighting or a flat LDA-style scheme would help, since the plain dot product gives shared features the same weight as the ones that separate the confused pairs. I'm also checking whether the template coordinates and the feature window size are actually matching how MNIST digits are centered and scaled.

I'm weighing a mixed scoring rule that partly penalizes template norm, since the plain dot product favors high-ink templates like 8. Step 3 helped 3, 7, and 1 a little but hurt 4, 9, 5, and 2, so I'm trying to work out which part of that change caused the trade-off.

I'm noticing that the step-3 averaging probably hurt class 4, since blending its variants blurs the template and lowers the peak match. Since the classifier is linear, I can't take a max over prototypes, so I'm looking for a different linear scheme.

I'm thinking about switching to a naive Bayes style scoring, where each class gets a log-likelihood from per-feature on/off probabilities taken from the templates. That would penalize missing features as well as reward present ones, and it should handle the ink-heavy templates better. I'd need to normalize the features into [0,1] first so the probabilities behave.

I'm weighing a naive Bayes style scoring where each feature contributes a log-odds term based on template-derived on/off probabilities, scaled down since neighboring features are correlated. I'd need to rescale the features to roughly 0 to 1 and clip the probabilities so the log terms stay stable.

I'm settling on a Bernoulli-style scoring for the classes, with a damping factor around 0.2 to account for correlated neighboring features and a feature scale of 2. The next step is writing the log-odds sum over the features, and I'm treating the exact form of that code as still in progress.

I'm settling on a Bernoulli-style scoring with a damping factor, using a feature scale of about 2.5 and capping the on-probabilities at 0.8 so that dense templates like 8 aren't suppressed too hard.
