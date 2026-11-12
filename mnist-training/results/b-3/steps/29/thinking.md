The new variants made things worse, with loss at 0.8325 and more 7s being pulled into 0. I'll revert both of them but keep the new biases, since those came from the step 27 counts and should help. After that I want to look at 7→9 (104), where 7 has a top-left endpoint and 9 has a loop on its left side.

I'm going to keep the new biases and undo the two variants, since they're what made the loss worse. I also want to nudge the endpoint penalty for 0 and 8 up from 0.3 to 0.45, because that affects the 3→8, 5→8, and 2→8 confusions.
