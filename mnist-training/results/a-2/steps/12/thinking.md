Still around 70%, and the parts changes barely move the number, so the orientation features are what dominate. Getting better results probably means either improving the orientation templates or finding better features. The confusions that keep showing up are 0→2, which is surprisingly large at 217, along with 2→3/8, 3→5, 5→6, 6→4/5, 8→7/1/2, and 9→7. The 0→2 pairing is the odd one, since those digits shouldn't overlap much, so I'm wondering whether the 2 template has a top arc, a bottom stroke, and a left side that resemble a 0.

I'm checking whether the 0 template is the problem: a 0 that tilts right has its sides running along the same "/" direction as the 2's diagonal, while my upright ellipse only has vertical sides. So I'm thinking about adding slanted versions of the 0 ellipse to the template.

I'm considering whether slanted variants of each digit template would help, since many MNIST digits lean right and a shear transform could capture that. I'm weighing whether blending a sheared version into the same hand-drawn template counts as acceptable, and I'm leaning toward treating it as part of the single deterministic drawing for each class.

I'm settling on a single slanted drawing for each digit rather than generating variants: a mild shear (around 0.2) applied to the strokes, which shifts the top right and the bottom left, matching how digits like 0, 4, 7, 8, and 9 typically lean in MNIST.

I'm settling on a light, uniform slant for the digit templates: a shear of about 0.15, applied to every class except 1. I'm also lowering the saturation cap from 0.92 to around 0.85, since a high cap means a missing expected feature costs too much in the naive Bayes sum.

Dropping the shear idea: I'll settle on the light slant of 0.15 and the lower 0.85 cap, both applied as one change.
