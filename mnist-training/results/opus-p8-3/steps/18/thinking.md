I'm working out which loop type dominates: the long-range loop (LOOP_l, cols 4-7) seems to fire far more often than the short one. Several rows show it firing, including some for the digit 3, which I don't expect to have loops at all, so I'm checking those specific rows.

I'm wondering whether LOOP_l also fires in the cavities, since the far left tap reaches about 7.5 px and a 3's arm ends might extend that far. That would make it unreliable there. The 7s in row 1 are odd too, possibly because the stem slants and the bar's left end droops. LOOP_s rarely fires, and since LOOP_l wins whenever both are active, I can't judge LOOP_s well yet. It does show up in a few 3s, an 8, and a 3 in row 3.

I'm going through the per-class location counts for LOOP_l, and the 0s are the odd case since so many of them show no loop at all. The rows where it fires for 6 and 9 are also off from what I'd assumed.

I'm checking whether the loop positions are systematically shifted: the 9's loop may sit lower in the frame than I'd assumed, around y≈11-12 rather than 9-10, since the mass of a 9 is weighted toward its top loop.

I'm fitting per-class LOOP_l templates from the row-by-column counts, with the 9's loop sitting in row 1 and the 7's in row 1 as well, which could help separate 7s from 2s. LOOP_s is still mostly unknown, so I'm leaning toward shifting its guesses down a row with less weight. I'm also wondering whether to probe the other detectors next.

I'm planning a combined probe: OPEN_L, OPEN_R, OPEN_U and OPEN_D, each split into a top half and a bottom half, so eight slots plus none. Since those directions are mostly mutually exclusive at a given location, one pass should show cavity structure without needing separate probes for each detector.

I'm thinking about whether the remaining detectors, HB_s, VB_s, HB_l and VB_l, are worth probing later on.
