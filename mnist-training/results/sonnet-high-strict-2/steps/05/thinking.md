I'm working out how the scoring treats digit 1: its template is small, so the mean in-template ink ends up high whenever there's ink in the center column, which is common. The out-of-template penalty uses a large area, so its contribution stays small. I'm also weighing whether to raise that penalty to balance the in-mask cells against the roughly 60 cells outside.

I'm checking the out-of-mask penalty for digit 1: its in-mask average comes out around 0.4, with about 0.2 ink outside, which gives a score near 0.26 scaled, comparable to 3's own template. I'm weighing a larger out-penalty weight of λ=1.5, which seems to separate 1 from 3 better, and also considering scaling the features up to lower the loss.

I'm also weighing a per-class bias to correct the over-prediction of class 1, since its count is far above the others. The confusion counts could guide that, but changing the bias alongside the penalty weight would mix two effects, so I'm leaning toward adjusting only λ for now.

I'm settling on λ=1.5 and a scale of s=15, since those should separate 1 from 3 better and keep the loss from being driven by low confidence.
