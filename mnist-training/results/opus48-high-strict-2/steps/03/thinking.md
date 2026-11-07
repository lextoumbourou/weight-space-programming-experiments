The model has reached 29% accuracy with a loss of 2.17, but its predictions are bunched into classes 1, 4, 5, and 6, while classes 0, 2, and 7 never come up. Looking at the counts, classes 5 and 6 are being predicted far more often than the rest, so I want to dig into where the errors are landing.

Now I'm going through the per-class accuracy: 0, 2, and 7 are almost never right, and the predictions for 3, 5, 7, 8, and 9 keep collapsing onto 5, while 6 soaks up 0 and 2. I think the real problem is weak features, so I'll look at adding stronger diagonal detectors and a clearer signal for the 0 hole.

I'm weighing whether the spatial ink template is doing any real work, since it seems too blurry to separate the confused classes. Instead, I'm considering leaning on the 4x4 position information, like the strong top horizontal bar on a 7 versus the sparse bottom.

I'm going to make the orientation templates spatial as well, so each digit specifies where vertical and horizontal strokes should appear in the 4x4 grid rather than a single scalar. A 7 would get a strong horizontal bar in the top row, a 0 vertical strokes on the left and right columns with horizontal ones at top and bottom, and a 1 vertical strokes down the center.

I'm checking whether the spatial ink templates are actually separating the digits, since the 5 template's mean density looks high enough to pull in many inputs.

I'm realizing the dense templates have an edge: a template with mostly positive cells, like 5 or 6, scores high on any inky input, while sparse ones like 1 and 7 get pushed negative. So I'm thinking about normalizing each template to the same norm so the density stops deciding the winner.

I'm normalizing each centered template to unit length so that dense templates stop winning on sheer ink. The aim is a cosine-style match that treats 1 and 7 as fairly as 5 and 6, and I'm planning to apply the same normalization to the orientation features.

I'm turning to the orientation templates next, planning to give each digit spatial vertical and horizontal stroke maps rather than scalars. I'll also normalize every centered template to unit length so dense digits like 5 and 6 stop winning just by covering more ink, and I'll tune the gains per feature afterward.

Now I'm writing out the stroke layouts for digits 0 and 1 on the 4x4 grid: a ring of ink for 0, with vertical sides and horizontal top and bottom bars, and a solid center column for 1.

Still writing the stroke layouts for the digit templates...

Still writing the spatial stroke templates...

Still writing the stroke layouts for digits 4 and 5...

Still writing the stroke layouts for digits 5 through 9...

I'm settling on coarse spatial templates for the orientation features, since the 4x4 grid is too blurry for fine detail anyway, and I'm going to normalize all of them so the dense digits stop winning on sheer ink.

Still writing the stroke layouts for digit 6...

Still writing the stroke layouts for digit 7...

Still writing the spatial digit templates...

Still writing the spatial stroke templates...

Still writing the spatial digit templates...

Still writing the spatial templates and normalizing them...

I'm setting the gains for the ink, vertical, and horizontal features at 10, 8, and 8, then planning to adjust them once I see how the logits spread across the digits.

Still writing the spatial stroke templates and normalizing them...

Still writing the 4x4 template arrays for each digit, one feature map at a time.
