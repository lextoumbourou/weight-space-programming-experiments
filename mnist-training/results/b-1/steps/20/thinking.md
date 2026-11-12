I'm checking whether the detection thresholds are too strict. Center pixels on strokes sit around 0.8 to 1, so a cell touching a stroke should usually max out near 0.9. Detector A needs a 2x2 empty hole with all four neighbors inked, and it also requires the center to be empty.

I'm going to loosen the thresholds, since a center pixel with antialiasing can kill detector A even inside a real hole. I'm lowering the center penalty and the bias for A, and I'm reducing the interior penalty for B. I also want the hole weights to count for more.

I'm settling the bias and weight values for the remaining detectors, with a bias of -3.0 and hole scale hs at 1.0, and I'm leaving the beta calibration alone since the changes were small.
