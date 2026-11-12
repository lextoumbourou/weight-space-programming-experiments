Accuracy has reached 71.9% with loss down to 0.969, so I need to recalibrate β again. I'm now tallying the column counts across the confusion matrix rows.

Still tallying the matrix, now on rows six through nine. I'm working out the β corrections for each class from the row-to-column ratios, and the largest adjustments land on classes four and eight.

I'm raising the small-hole weights for class 0 to 1.0 on top and 1.2 on bottom, since the 0s with interiors look like 6s near the bottom. I'm also reducing the top penalty on 6 to cut those confusions.
