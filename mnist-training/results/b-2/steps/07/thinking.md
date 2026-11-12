I'm at about 69% accuracy now and working incrementally. The biggest remaining errors are the 2-to-3 confusions (210) and 7-to-9 (191), with 3-to-5 and 5-to-3 close behind. I'm now comparing 2 and 3, looking at the bottom horizontal base and the diagonal stroke that separates them.

I'm now weighing the structural cues for telling 2 and 3 apart, such as the loop at the bottom-left and the open bay in each digit's lower region. For 3 versus 5, I'm checking whether the left vertical stroke at the top of 5 can be captured by the orientation templates. I'm also considering endpoint locations as a more discriminative feature.

I'm working out endpoint detection as a way to separate the digits, since stroke tips are very discriminative. The idea is a convolution that looks for ink below a tip with side edges below it and no ink just beneath, so a stroke end can be distinguished from a horizontal stroke's boundary.

I'm adding four endpoint detectors, one each for up, down, left, and right tips, which can tell a stroke's end from a horizontal boundary. The idea is to fire on ink below a tip with side edges under it and suppress it where ink sits just beneath, since loop tops and horizontal strokes would otherwise trigger it too.

I'm working out a way to detect stroke tips: an up-pointing endpoint would fire on ink below the tip with side walls under it and no ink just beneath, which should separate a stroke's end from a horizontal boundary.

I'm working out how to tell a stroke's tip from a horizontal boundary, using stroke edges below the tip and suppressing responses where ink sits just beneath.

I'm sketching a fourth family of features: endpoint detectors for stroke tips, one per direction. For the up-pointing tip, I'd weight the cap edges just below the tip and then reward stroke boundaries continuing downward, including the diagonal channels at half weight.

I'm writing the up-tip endpoint detector's weights: a positive cap response just below the tip, reward for stroke boundaries continuing downward, and negative weights for horizontal boundaries nearby and an empty row above, with a bias to set the threshold.

I'm checking the top-tip detector against a loop top and a horizontal bar: the cap response there gets cancelled by the boundary just below, so it stays quiet. Next I'm sketching the matching detectors for downward, left, and right tips.

Still writing the detector weights, and the right-tip detector is next, with its cap on the left edge and a negative weight on the right edge.

I'm sketching per-digit endpoint positions now, giving each digit's stroke tips a direction and a weight, for example an up tip at one spot and a down tip at another for the 1.

Still writing the per-digit endpoint weights, and I'm now fixing the tip positions for digits 4 through 9.

Still working out the 2-variant loop path, with a weighted set of points tracing the bottom loop and the base to the right.

I'm still uncertain whether the endpoint thresholds will be calibrated well: they could end up firing on nothing or on everything, and I'll only know once I run it.
