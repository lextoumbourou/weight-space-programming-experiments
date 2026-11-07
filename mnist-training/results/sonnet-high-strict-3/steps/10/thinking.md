I'm checking the prediction counts per class, which add up to 1442, 1287, 2135, and 1200 for the four labels. I'll then consider a damped class-bias adjustment and maybe a few more discriminative features.

I'm working through the per-class bias numbers now, estimating how much each class should shift using a damped log-scale, with the rarest class getting the biggest boost and the most common getting pulled down slightly.

I'm noticing my template for the digit 4 is weak, since real 4s often have an open top, and I'm wondering whether the 9 confusions with 5, 0, and 1 point to something similar. I don't want to dig too deep, so I'll keep it to a bias adjustment rather than changing the features.
