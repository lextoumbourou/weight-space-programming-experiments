Loss has dropped to 0.99, and the endpoints seem to be helping. Now I'm checking how the class balance has shifted by summing the prediction columns, and column 3 is clearly the heaviest.

Now I'm working through the per-column totals and the log ratios of true to predicted counts. Column 8 and column 9 come out the most underpredicted, so I'm considering whether to raise the endpoint weight and nudge the bias.

I'm settling on a final set of weights: endpoints up to 0.8, holes up to 1.3, and the bias update applied alongside them.
