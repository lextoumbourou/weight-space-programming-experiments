The first 63.6% reading suggests the bias tweaks aren't moving much, so I'll need a structural change for bigger gains. One idea is to sharpen orientation selectivity through the conv1 bias, but I'm also wondering whether broadening the orientation blur in the templates would fit better, given that the "8 magnet" points to features that are spread out. If that's right, lowering OCUT and enlarging RAMP might match the templates to the data and reduce the coverage advantage.

I'm weighing whether to sharpen orientation selectivity or broaden the templates, and I'm checking how the conv1 response would fall off across stroke angles. With a bias of -0.2, a stroke would excite several channels, and the broader template setting would look similar. I'm also tracing the confusion pairs, especially 0→2, to see which shared stroke shapes drive them.

I'm working through why a 0 might get mistaken for a 2, and I'm checking whether my orientation convention is consistent with the kernel's, which I believe it is. The overlap seems to come from the lower-right arc of the 0 and the central diagonal of the 2 both leaning the same way under the blur. The coarse grid may be part of the problem, and I'm also considering a loop-detection feature to separate 9 from 4 and 7.

I'm now thinking the coarse grid might be the bottleneck, and I'm also considering whether digits are centered by their center of mass, which could shift a 9's loop downward within the bounding box and change where the strokes land.

I'm going to shift each template so its center of mass sits at the middle of the grid, the way MNIST digits are centered. That should matter most for 9 versus 8, since a 9's loop carries most of its ink and would otherwise sit off-center.

I'm going to recenter each digit on its center of mass, the way MNIST does, and keep the box height at about 20 pixels. Then I'll shift the strokes and recompute the weighted centroid, leaving the biases as they are for now.
