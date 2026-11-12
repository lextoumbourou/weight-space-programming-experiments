I'm seeing the ink-only baseline at 43.7%, with the 9s almost never predicted and 8s rarely too. The 9s get guessed as 0, 1, 2, 4, and 5, which is odd for a 9 template. I'm wondering whether my coordinate mapping is flipped somewhere, since 9 and 6 would swap under a vertical flip.

I'm checking whether a transposed or flipped coordinate system could explain the 9s, but the 1s are still recognized correctly, which rules out a transpose. A vertical flip doesn't fit either, since 9s aren't being mistaken for 6s. That points to the templates themselves being weak, so I'm comparing my 9 template's loop and stem placement against typical MNIST 9 geometry.

I'm now weighing whether the 9 template is shifted by center-of-mass centering: its mass sits in the top loop, so centering would push it down, and I'm checking how far that moves the bounding box and whether the centers should be pinned to (14,14) instead.

I'm now checking whether the center-of-mass shift is the real fix, working out the target point the mass should be pinned to, roughly 13.5 to 14 in pixel-index coordinates, and noting that the conv output-to-input mapping also needs the same offset.

I'm going to try centering each template on its center of mass, since the 9's mass sits in the top loop and would be pushed down by a centering shift. That's a systematic error that would affect every template, so I'll apply it to all of them with the target point near (13.8, 13.8) and keep the k=2 ink-only setup for now, adding orientation channels back afterward.
