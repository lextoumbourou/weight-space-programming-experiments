I'm sorting out which bit each flag maps to, then totaling the slot counts for class 0 across each flag's set of slots, which gives 665 for F1 and 864 for F2, and now I'm working out the total for F3.

Now I'm checking the remaining class totals, and I've got F3 for class 0 at 615.

Now I'm checking the row totals for class 7, where the counts I'm adding up come to 1090 rather than the 1028 I expected, so I suspect I've misread a column. Class 7 looks like a strong discriminator for F2 and F3 against class 9, so I'll flag the 3-versus-5 comparison for F3 next.

Next I'm picking three more stroke features to test: an upper-right vertical, a lower-left vertical, and a forward slash in the middle, with 0.8 as the cutoff. After that I'll check a few others before building the classifier on all of them.
