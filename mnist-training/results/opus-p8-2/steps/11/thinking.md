Feature resolution looks like the bottleneck, so I'm weighing whether finer orientation channels at 8x8 would help more than the current 4x4 setup.

I'm weighing whether the 1 template needs several slant variants, drawn as extra strokes in one template, to handle the 1→7 and 1→2 confusions, and I'm also considering whether an 8x8 orientation grid would carry more information than the current 4x4 one.

I'm weighing hand-drawn template variants per class, such as a slanted and a vertical stroke for 1, a closed and open 4, and a straighter and slanted stem for 9, to see whether that helps the 1→7 confusion. I'm also turning to the 2→3 confusion, since the difference lies in 2's diagonal and bottom bar versus 3's lower bowl and middle cusp.

I'm weighing whether a 2→3 confusion could come from how the 2 template's diagonal runs from upper-right to lower-left, since real 2s often curve that stroke more. I'm also considering whether per-cell max presence makes the two digits overlap too much, and whether a classifier that leans on low within-class variance features might separate them better.

I'm now considering endpoint counts per digit as a discriminator: 1 has two endpoints, 7 has two as well, 2 has two, 3 has three, 5 has two, and 4 has three or four. That could help separate pairs like 2 and 3 more directly than the current orientation features.

I'm checking whether endpoint counts could separate the confusable pairs: 3 has a left-middle and bottom-left end where 2 has a bottom-right one, and 7 has a top-left end that 9 lacks. Detecting an endpoint with a 5x5 conv is harder, since it needs ink at the center with ink on only one side of the ring.

I'm checking whether endpoint detection can work with a 5x5 filter: a bright center with little ink around the ring should mark an endpoint, while a mid-stroke pixel with ink on two opposite sides should not. A threshold between those responses might separate them, though corners and curves that put ink on two adjacent sides could still cause trouble.

I'm checking whether a 5x5 filter can flag endpoints: a bright center with little ink on the surrounding ring should respond, while mid-stroke pixels with ink on two opposite sides should not. I'll put that response on a free conv1 channel and pass its center tap through to the 4x4 grid on a free conv2 channel.

I'm listing endpoint locations for each digit's template strokes, starting with 1's two ends and 2's arc start and bottom-right end. For 3 I'm placing the top-left and bottom-left ends, and wondering whether the middle cusp should also count as an endpoint.

I'm listing where each digit's endpoints fall: 4 gets four, 5 gets two near its top-right and bottom-left ends, 6 one at the top, 7 two, and 9 one at the bottom, with 0 and 8 having none. I plan to mark each endpoint as a soft cell membership at weight 1.0, the same way I handled holes, and then see how the pooled response behaves.

Adding a soft endpoint weight with a small negative bias for the zero-endpoint digits, and I'm leaving the stray-endpoint case alone for now.

I'm settling on the endpoint filter's weights: core +1, ring -1, bias -1.5, so a true endpoint scores around 1 while thick strokes score higher. Before settling on that, I want to check that a straight stroke crossing the 5x5 ring doesn't count too much ink to stay below threshold.

I'm checking that a straight stroke crossing the ring doesn't add enough ink to cross the threshold, and that stroke ends with the center on the stroke give a response of roughly 0 to 1.5. I'm also considering adding 1-template variants with slanted strokes.

I'm weighing a wider 1 template built from several slanted strokes, but a broad union could let 1 pull probability away from 7, so I'll skip the variants for now and focus on endpoints.
