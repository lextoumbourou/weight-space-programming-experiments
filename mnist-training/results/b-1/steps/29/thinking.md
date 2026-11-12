I'm weighing whether a threshold around 0.7 is close to the best value, since the score barely changes near the minimum. Next I want to tighten accuracy on strongly slanted 1s, which the current fan template may not cover well.

I'm checking whether the 3↔5 confusions and the strongly slanted 1s are the main accuracy gaps, and I'm considering a fourth, more slanted stroke for the 1s and some reshaping of the 3 and 5 templates. Raising the orientation weight from 0.8 to 1.2 is another lever I want to test.

I'm going to test raising the orientation weight to 1.2 along with adding a fourth stroke to the 1s, and I'll need to recalibrate afterward since the change shifts how the β effect balances across both parts.
