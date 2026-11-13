I'm decoding the three features and running them through the first class's values. For class 0 I get f0 ≈ .666, f1 ≈ .995 and f2 ≈ .99. Now I'm starting on class 1's values.

Now I'm working through classes 2 through 6, computing the three feature values for each, and the last one is still in progress.

Now I'm finishing class 8's values and moving on to class 9.

Now I'm working out the final feature values for the last class and the three vectors that come out of them. Next I'm weighing how the 47 orientation features combine, since the overlapping horizontal and vertical cells may make them more correlated.

Now I'm computing the horizontal feature values across the ten classes for the new cells, and I'm moving on to the rest of them.

Now I'm computing the horizontal and vertical feature vectors for the remaining cells, going through their values across the ten classes.

Now I'm weighing the trust factors for the horizontal and vertical features against the diagonals, trying a shared weight for the now-dense set.

I'm settling on a weight of 0.45 for the horizontal and vertical features, which raises their overall influence by about 40%, and I think that's justified since the new cells carry real information. I'm keeping the other parameters as they are.
