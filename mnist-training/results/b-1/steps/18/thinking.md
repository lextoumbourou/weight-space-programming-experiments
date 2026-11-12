I'm checking how sensitive the step 16 and 17 values are: at step 16, columns 8 and 9 come in just under, and at step 17 they go just over. Linear interpolation gives a predicted count for column 8 by summing the step 16 entries, which comes to 181.

I'm tallying the per-class counts for step 16 by summing each column's entries, and the column totals come out around 850 to 1,380. I'm also setting the step 17 β values for the remaining classes so I can interpolate each one.

Now I'm tallying the step 17 column totals, which come out between roughly 280 and 2,400 depending on the class.

I'm estimating how strongly each class's count responds to its β shift, using the log of the step 16 to step 17 count ratio divided by the change in β. The slopes for classes 8, 9, 4 and 5 land around 50 to 75 per unit β, so I'm taking roughly 60 as a working average.

I'm working out target counts for each class and estimating how far each β needs to move to reach them, using a slope of about 60 per unit β. For class 0 that comes to a small upward shift, and for class 1 a small downward one.

Now I'm turning the step 9 count into a target, and running the same log-slope adjustment across each class to get the β shifts for classes 0 through 8, with class 8 coming out strongly negative.

I'm settling on the step 16 to 17 β values for the remaining classes and planning to keep the current slope for now, since the calibration depends on it. The accuracy looks limited around 66 to 68 percent, so I may need better features or templates, and I'm also weighing whether a larger scale would sharpen the logits enough to lower the loss.
