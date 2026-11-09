I'm checking the predicted totals per digit, and sigma 3 keeps the balance about the same. Digit 1 still comes out too high, even with a bias of -0.3, though its recall holds up, and I'm weighing the false positives from 4, 8 and 6 that come with that.

I'm weighing whether to keep sigma at 3 or drop to 2.5, since 2.5 seems slightly better on loss even though the results are mixed. The stubborn 4→1 and 8→1 confusions probably trace back to the slant variant, so I'm considering a larger bias on 8 and a switch to the step-6 template with the narrow loops and crossing, which helped 8's recall before.

I'm weighing a small gain from a wider 0 template (rx 0.33) against the extra 2→0 confusions it brings, and I'm leaning toward taking it anyway.
