The accuracy only moved to 0.72 from +0.016, which looks like noise or a slight negative effect. I'm checking the expected size of the irrelevant-feature penalty from the interaction term, and it comes out around 0.01, so that doesn't explain much. These probes are also slow, so I'm considering a different approach.

I'm moving on to tuning per-feature weights, since the probes are slow and the remaining error might just be label noise. I'll try raising x1 to 1.0 while keeping the others at 0.7, and maybe test x11 at +0.35 as well.
