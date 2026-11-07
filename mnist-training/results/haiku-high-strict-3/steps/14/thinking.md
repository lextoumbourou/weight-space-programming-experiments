Step 13 came in at 36.83%, the best so far, with two steps left. I want step 15 to be the best known result, and since gains are small now, I'll try one minor tweak in step 14 and fall back to the step 13 config at step 15 if it does worse.

Now I'm tallying the per-column counts for step 13, and column 8 at 1036 is running high against the others. Column 9 is at 692, and the class 7 prediction count stands at 343.

I'm tuning step 14 by lowering the bias on class 8 to 1.1, pushing class 5 down to -2.6, and dropping class 4 to -1.9, while leaving the rest unchanged.
