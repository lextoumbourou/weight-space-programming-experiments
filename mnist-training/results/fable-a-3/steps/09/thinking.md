I'm decoding row 3 of H into four parity sums over the outputs, and checking class 0's first bit, b0, which comes to 16+246+268 = 530, or 53.5%. I'm now working through b1 over the same vector.

I'm working through the per-class sums for b2 and b3 over the decoded outputs, and I'm comparing the totals against their percentages for each class.

I'm checking class 4's bit sums against the same row-3 decode, landing on 59% for b1 and around 42% for b2 and 15% for b3. Class 5's b0 comes to about 68%, and I'm starting on its b1 total.

Checking class 6's bit sums against row 3, I get about 24% for b0, 94% for b1, 96% for b2, and 53% for b3. Class 7's b0 comes to roughly 3.5%, and I'm now adding up its b1 and b2 totals.

I'm finishing the class 8 bit sums for row 3 and moving on to class 9. Then I'm laying out the first three rows of the table, with class 0 at 53.5, 96.9, 88.9, 37.2, class 1 at 1.8, 3.9, 3.6, 1.1, and class 2 at 74, 94, 89.4, 73.

I'm writing out the final rows of the table for classes 3 through 9, with class 9's values still to come.

I'm weighing which single-end run pattern to drop for the V columns, either top-only or bottom-only, since single-cell runs showed up often in the H data and dropping either could lose something. Both look about equally plausible at roughly 10%.

I'm weighing whether to drop a top-only or bottom-only run pattern, or to use triples instead, since each choice loses some information about the vertical runs.

I'm weighing the vertical runs in each column now, starting with column 0 where the strokes sit mostly in the middle rows. Single-end patterns look less common for the long vertical stems, so I'm guessing the bottom-only pattern is rarer in column 0 and the top-only one rarer in column 3.

I'm now weighing the V-column run patterns: the single-end ones like top-only for column 0 where the serif of 7 sits, or bottom-only for the 2's lower-left turn, both seem roughly equally plausible at 10–20% so I'm still deciding which to drop.

I'm weighing a different approach: splitting the V patterns so that the joint bits for the lower three rows are kept exactly, and only the top bit is merged in the two cases where it's ambiguous.

I'm weighing which run pattern to drop from the vertical-column set, since the eleven patterns can't all fit into the budget. Each choice loses a bit of information, so I'm leaning toward dropping 0001 for column 0 and seeing how much that costs.

I'm weighing whether dropping a top-only or bottom-only run pattern would bias the estimates more: a top-only drop pushes those cases into 0000 and underestimates the top bit, which could matter for the 7's serif. I'm also considering dropping an isolated interior cell instead.

I'm leaning toward dropping the bottom-only pattern for column 0, since the bottom-left bits there seem rarer than the top-left serif of the 7, though I'm still weighing how much that choice would cost.

I'm settling on dropping the bottom-only pattern for column 0, since it looks rarer there than the top-left serif of the 7. For column 1, I'm sorting through which strokes land in the left-hand cells, and I'm considering whether a short top-only pattern from the 9's loop would matter enough to keep.

I'm going to drop the top-only pattern for columns 1 through 3 and the bottom-only pattern for column 0, since those single-end runs look rarest in each column. For column 3, I'm weighing whether the top-right arcs of the 2 and the stem tops of the 7 and 4 would actually produce top-only runs there.

I'm leaning toward dropping the bottom-only pattern for column 2 as well, since the bottom-end runs there look rarer than the top-only arcs near x≈17. I'm also checking how the long stem of the 7 runs through columns 1 through 3, which could make a short run at the bottom less likely there.

I'm settling the column 2 choice by dropping the bottom-only pattern there, and I'm keeping 0001 for column 1 since the stem bottoms of 7 and 9 make it plausible. For column 1's top-only case, I'm weighing the 2's short hook against the longer left-side runs of 9, 4, and 5, and I'm leaning toward dropping 1000 there. Now I'm starting the column 0 vertical-run setup with 0001 removed.

Now I'm writing out the decode rules for the last column, mapping each of the ten run patterns to its on-off bits across the four rows and setting up the four feature tuples for column 0.
