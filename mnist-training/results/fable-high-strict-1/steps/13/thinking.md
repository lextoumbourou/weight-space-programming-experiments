Now I'm looking at the per-class totals and the overall accuracy, which came in around 58.3%, with the 8 class recall having risen to 640. The biggest mix-ups stand out: 7 being read as 9 and 5 most often, and 3 being read as 5.

Now I'm comparing the mistakes to the templates, checking which digit pairs keep getting confused and how the class weights should shift to correct them.

Now I'm working through the top-bar and vertical-stroke cells in the 3 and 5 templates, checking which cells the middle horizontal of a 3 lands in and whether the top vertical is what separates the two digits.

I'm weighing a slightly higher orientation penalty so the 3's top-right curve counts against 5, and the 5's left vertical counts against 3. Since 5 is already over-predicted, I'm also considering raising m_5 to push back on the 3→5 mix-up directly. Separately, 0 is under-predicted, so I'm lowering m_0 to around 0.83.

Next I'm thinking about the 1 templates: the single thin stroke is probably too light, since many real 1s are a bit thicker and have a small flag at the top-left. Adding mass there might help the 1s hold their ground without changing how the 7 template is shaped.

I'm thinking about adding a short flag at the top-left of the 1 template, since some real 1s have one and the thin stroke may be carrying too little weight. For the 7→9 confusion, I'm looking at the 9's loop, which is probably too large and too full on its left and bottom sides, so the 7's top bar and right diagonal match it too well.

I'm considering raising λ slightly, to about 0.56, so that missing strokes get penalised more, since most of the top confusions are cases where the wrong class has extra ink. That would also call for a higher m_8, because 8 is a superset of most digits and accounts for the excess predictions.

I'm weighing a uniform bump to λ of about 0.56, which would penalise both the dense and sparse classes by roughly the same proportion. I'll then need to re-tune the per-class multipliers, lowering the ones that would now over-predict and reconsidering 8, 0, and 6 with the new scale.

Now I'm weighing a uniform bump to λ and the per-class multipliers together, since 8 and 0 are over and under-predicted in ways that a global change would shift in opposite directions.

I'm settling on a uniform bump to λ of about 0.56, with the per-class multipliers adjusted to match, and a small nudge to the orientation penalty at 0.10. I'm also adding a short flag to the 1 template so those thin strokes carry a bit more weight.
