The result is worse, so the optimum looks like it sits around -0.4, and I'll keep it near -0.45. With x10 and x11 as absolute values (4 units) plus the 5 linear terms (10 units), that's 14 units used and 2 left, which isn't enough for an interaction term that needs 4. I might be able to merge some terms, but that's not clear yet. Next I'm considering fine-tuning the x4 and x9 weights, possibly raising them to 0.85, and rescaling overall.

I'm trying the x4 and x9 weights at -0.85 instead of their current values, and I'll recheck the overall calibration after that.
