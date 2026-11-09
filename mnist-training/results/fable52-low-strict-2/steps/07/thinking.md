The 0 class now reads 899 after the fix, while 9 fell to 446 and the bias sits at -0.65, so I'm checking the 9 reduction. Next I'm adding weight increments to the confuser columns, starting with 2 and 6 for column 0.

Still adjusting the confuser weights column by column, now updating the entries for 9 and 7 in the last column.

I'm nudging the bias values now: raising 9's bias toward -0.3 so it recalls more of its own digit, and making small shifts to 0, 1, 4, 5, 7 and 8 based on the predicted counts. I'll also keep the existing confusers for 9 as they are, since its misses are already being covered by the columns for 7 and 4. The loss sits around 0.86 at 73% progress, which I'm content with for now.
