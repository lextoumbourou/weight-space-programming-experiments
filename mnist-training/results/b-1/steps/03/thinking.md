I'm weighing whether to subtract the class mean from the normalized templates to make the weights discriminative, but I realize that difference only cancels a term common to every class, so it ends up equivalent to cosine similarity.

I'm trying centered features next: score each class by the dot product of the centered input with its centered template, normalized by that template's length. The catch is that the magnitude of the real features may not match the templates, and the distance approach has the same scaling problem. I'm also starting to suspect the bigger issue is that the features are too blurry from max pooling, so a finer-resolution pixel template may matter more.

I'm settling on centered cosine scoring, where each class weight is the centered template scaled by its norm, with a matching bias term. I'm also considering whether softening the template positions would help, since the 8 template's loops look too wide compared with real digits. The open question is how to choose the scale factor, since the magnitudes of the features and centered templates may differ.

I'm settling the scale at s = 2, and I'm also trying a narrower 8 template, with the top ellipse at (14, 9, 4, 4.3) and the bottom at (14, 18.5, 4.8, 5), leaving the other templates as they are.
