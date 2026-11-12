Still stuck near 53%, so the core needs rethinking. I'm looking for an approach that could realistically get past 85%, maybe a discriminative design built on how digits are structured. Pairwise difference templates seem promising: for 7 versus 9, the loop at the top left of a 9 is the key local contrast, and for 3 versus 5 it's the ink position at the top right versus the top left.

Blurring the templates a bit more, with a wider kernel and softer edges, should make them tolerate the 2-3 pixel shifts from slant and position. The features are already coarse, so I need templates that look like the true class means and a distance that is scaled correctly, perhaps with a free global scale.

I'm settling on a nearest-centroid setup with a free scale k on the templates, since the bias term depends on how big the template is. I'll treat k as a tunable value and try a few, with step-7's result suggesting the real features run around 1.5 times the template magnitude, so I'll start there.

I'm now weighing a template scale of about 1.5, with the logit scored as a scaled dot product against the templates minus a norm penalty, and I'm also considering whether to keep the hole channel and sharpen the 9's loop and stem position.

Still working through the digit templates, so I'm checking the rough stroke layouts for the remaining classes and how the slant shows up across them.
