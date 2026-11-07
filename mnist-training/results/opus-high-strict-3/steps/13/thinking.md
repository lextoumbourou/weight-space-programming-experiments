I'm weighing blur 5.0 against the 5.5 setting: accuracy is about the same, but loss is lower at 5.5, and only three steps remain. I'm going to settle on blur 5.0 as the safer improvement. I'm also looking at the biases, where column 1447 is shifting even further, and checking the 4→1, 8→1, and 6→1 values.

I'm adjusting the per-class biases now: lowering class 1 to -1.2, nudging 3 up to 0.35 and 9 down to -0.35, and making smaller tweaks to 8, 7, 6, 0, 2, and 4.
