The baseline sits at 54%, and a lot of samples land on class 1. My guess is that template 1 has a small norm, so weak-feature images end up close to it by distance. The templates may be bigger than the real features, which would favor sparse templates. Normalizing the scores by template norm, or using a linear logit, could correct that, though I don't know the feature norm yet.

I'm weighing whether cosine similarity against mean-centered templates would handle the bias better than raw distance, since it removes the dependence on feature norm. I'm also considering whether to average slanted variants of the templates, but I'm wary of that since it could amount to generating samples, so I'm leaning toward just widening the blur instead.

I'm settling on cosine scoring with normalized templates, since the shared mean term drops out across classes and the feature norm no longer matters. Plain normalized templates should be enough without centering, so I'll set the logit scale around 5.
