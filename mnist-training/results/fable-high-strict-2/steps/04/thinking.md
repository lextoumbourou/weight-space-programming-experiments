The model now sits at 56.7%, with predicted counts spread unevenly across the digits. The main errors are 9 being pulled toward 4 and 7, with only 200 correct, while 8 is under-predicted and leaks mostly into 2 and 7. There are also smaller confusions, 3 into 5 and 6 into 4.

I'm weighing the remaining confusions: 5 leaking into 7 and 6, and 0 into 6. The biases look overshot, with 4, 7, and 1 over-predicted. Next I want to sharpen the templates for 9, 8, and 4, since 9 keeps getting pulled toward 4 and the difference between their top strokes may be the key.

I'm checking why 4 keeps winning on 9s when 9's own template should match: the 4 template's features line up with much of a 9's ink, so the question is whether my 9 template is placed too low, since I shifted it down to match the center of mass.

I'm checking whether the 9 template's tail angles are right, since 9 is only getting about 200 correct and 4 and 7 keep taking its ink. I'm wondering whether the loop is too small on the grid for the orientation weights to separate it cleanly from a 4.

I'm tuning the biases now: nudging 9 up slightly, lowering 4 and 7, and bringing 8 back toward neutral since it's badly under-predicted. I'm also raising 3 and 5 a bit to ease the 3→5 confusion, and I'm turning to 6, which is over-predicted with 178 going to 4.

I'm weighing whether to add a structural change for 9 versus 4: penalizing horizontal orientation at the top cells for 4, or only penalizing unexpected orientations where the class expects ink. The second option overlaps with the ink-based negatives I already have, so the first looks more useful.

I'm weighing a structural term that penalizes orientation channels a class doesn't expect in cells where ink is expected, which might separate 4 from 9 at the top of the digit and 7 from 9 on the vertical strokes.

I'm considering a penalty for orientations a class doesn't expect in cells where it expects ink, where 7's diagonal and 9's vertical right side could conflict. The concern is steep 7s, so I'd only penalize orientations at least 60° from anything the template expects there, and I'm working out how to bin the expected orientations per cell.

I'm adding a penalty for orientations a class doesn't expect in cells where it expects ink, using a wider angular tolerance so that only clearly unexpected strokes count, and I'm planning to scale that by how much ink each cell has. Next I'm adjusting the biases, lowering 1 a little because it is over-predicted.

I'm setting the final biases: a small bump for 0, 3, 5, 8 and 9, and pulling 1, 4, 6 and 7 down, with the orientation penalty expected to shift the balance further.
