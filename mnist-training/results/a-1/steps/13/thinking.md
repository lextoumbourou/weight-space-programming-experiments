The bias adjustment helped and accuracy is now at 65.8%. The biggest remaining problems are 1→7 with 170 errors, plus 7→5/9, 3→5, 4→9/6, 5→3/6, and 8 still performing poorly. For 1→7, I suspect the center-of-mass shift has made the 7's stem central, and the real 1s may sit in the right place while the 1 template itself is off. The thin stroke, around width 2, may be producing a weak response, and the serif variant of the 1 could also be contributing.

Now I'm weighing whether the per-class normalization is what's skewing the templates, since their norms differ. Rather than tune blindly, I'll keep adjusting the biases and fixing the templates directly.

I'm going to adjust the class biases by small amounts, boosting classes 2, 4, 7 and 8 and lowering 3, 6 and 9, based on their column sums. I'm leaving the scale s unchanged for now so the bias changes stay isolated, and I'm holding off on template changes for the 1 class.
