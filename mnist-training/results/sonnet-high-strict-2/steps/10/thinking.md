I'm checking the column sums and seeing that column 8 is now over target at 2843. The biases are very sensitive, so I'll need smaller adjustments, and I'm going to lower column 8's bias by about 0.7. Next I'm working through the sums for the other columns, starting with column 1.

I'm going through the column sums for the remaining columns, and they're all in a reasonable range except column 8, which is still well over. Since the biases are so sensitive, I'll take a smaller step on column 8, and I'm also looking at the slant of the 1 strokes, which seem to be getting confused with the 7 template.

I'm reworking the slant of the 1 stroke so it leans about 15° from vertical, running from around column 5.5 at the top down to 3.3 at the bottom. Then I'll update the ASCII template for the 1 to match that tilted band.

Still working out the ASCII template for the 1, filling in each row as the slanted band shifts left.

I'm checking the new column 8 sum against the template idea, and the remaining question is whether the slanted 1 template actually separates the 1s from the 7s. I'm also wondering whether the 7 template is the real problem, since 7s keep getting read as 9s.

I'm now looking at why the 9 template is absorbing the 7 images: the 7's ink sits entirely inside the 9's mask, so the penalty barely registers. I'm considering a stronger penalty on the 9's loop interior to separate them.

I'm making the 9 template's loop interior wider, with the middle rows of its hole marked as '-' across cols 3–5, so the 7s stop slipping through. I'll apply a similar wider hole to the 8 template as well.

I'm going to drop column 8's bias by 0.8 so it lands near -0.4, since it's the only column still well over target. I'll also adjust the slant of the 1 template and widen the hole in the 9 template so the 7s stop slipping through.
