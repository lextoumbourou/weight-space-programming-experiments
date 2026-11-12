I'm checking whether the bias change for class 8 should have raised its predictions, since the total still sits near 570. I'm suspecting the A_loop increase pushed class 8's penalty up enough to cancel the bias gain.

I'm working out whether the 8-loop penalty grows enough to cancel the bias gain, roughly 0.44 against the boost. That offset would explain why the 8 predictions barely moved. I suspect the loop features rarely fire on 8s at all, since their holes are often only 3-4 px. Small holes may vanish under the blur and max-pooling, so I'm considering a finer-scale hole detector in conv1.

I'm considering a finer-scale loop detector in conv1: a 5x5 kernel with an empty center and a mostly inked border ring, since small holes of about 3 px would otherwise disappear under the blur and pooling. I'm weighing how a threshold on the ring against the center would separate loops from crossing strokes, and that a medium hole of 4-6 px would need a larger ring than conv1 can cover.

I'm weighing a raw, unblurred ink channel in conv1 with a plain center tap, since the blur is washing out the small holes. I'm also considering a 3x3 ring of cells at distance one in conv2, with a negative center, to catch holes around radius 3.

I'm sketching a small-loop detector for conv2: a 3x3 ring of cells with a negative center, sized to fire on holes of about radius 3. Thick strokes that fill the center would suppress it, which seems right, and I'm now wondering how it handles two parallel strokes a few pixels apart.

I'm settling the remaining details of the small-loop channel: which digits get how many loops, and whether to keep the A_loop weight at 1.5 and the same biases as before.
