I'm at about 75.7% accuracy with a loss of 0.798, and the balance looks reasonable with 11 steps left. Next I want to make template edits aimed at the biggest confusions, especially 3→5 and 5→8. Since the earlier edit to the 4 template gave a gain, I'll try reshaping the 5 and 3 templates to better match how they actually look in MNIST.

I'm checking the 5 template against real examples: the top bar, the left vertical, and where the bowl bulges. For 3, I'm comparing the upper arc and its cusp, and I notice the main difference from 5 sits in the upper-right and upper-left areas, while both share the lower bowl. That suggests giving the upper rows more weight so the discriminating parts count for more.

I'm going to try weighting the top rows of the templates more heavily, on the reasoning that the upper half carries most of what separates 3 from 5, 4 from 9, and 7 from 9. I'm not sure the bottom-half cases like 2 versus 3 would benefit, but it's worth testing.

I'm going to scale the template rows by weights that favor the top half, normalizing each class template after the weighting so the cosine comparison reflects the emphasis. The offsets need the same treatment, and I expect the class balance to shift a bit, but not much. The row weights I'll start with are 1.2, 1.1, 0.95, and 0.85.
