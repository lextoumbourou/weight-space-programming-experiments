Step 12: 44.5% accuracy, slightly below step 10's 45.5%. The biases might be slightly off.

Let me compare step 10 and step 12:

Step 10 biases: [0.1, -1.55, 0.9, 0.96, 0.5, 0.85, 0.07, 0.15, 0.5, -0.15]
Step 12 biases: [0.10, -1.65, 0.90, 0.91, 0.47, 0.95, 0.18, 0.01, 0.56, 0.05]
I'm comparing the bias values from step 10 with step 12, and the largest shifts are in classes 1, 5, 6, 7, and 9.

Still summing the per-column totals...

Now I'm checking the column totals against the per-class accuracies. Class 1 and class 7 both came out over, while classes 6 and 9 came out under.

I'm comparing the per-class accuracies now: class 7 fell from about 49.6% to 44.1%, while classes 8 and 9 each rose a little. Overall, step 12 sits just below step 10, so the bias shifts slightly hurt.

Now I'm weighing the bias values from step 10 against step 12 to see which class shifts might be behind the drop in accuracy.

Comparing the two runs, the step 12 biases look like they'm pushing class 9 and class 7 in opposite directions from what would help. Step 10 over-predicted class 7 but still got better class 7 accuracy, so a higher class 7 bias seems to be what helped there.

Trying class 7's bias back near +0.15 seems worth it, since step 10's higher class 7 bias gave better class 7 accuracy despite the over-prediction. For class 9, the +0.05 bias from step 12 raised both its predictions and its accuracy, so I'll keep that direction.

Now I'm adjusting the bias values from step 12 to bring them closer to step 10's, with class 7 nudged up to about 0.10 and class 1 pulled back toward -1.55.

I'm weighing whether to pull class 7's bias back up, since the drop in its accuracy looks like the main loss between steps 10 and 12. The class 9 shift helped a little, so I'll keep that direction while I work on the rest.

Now I'm weighing whether to nudge the class 7 bias back toward +0.10 and average the other values. I also want to check whether the waist-focused digit 8 template helps or hurts compared with the old uniform one.

Comparing the confusion numbers, the waist-focused template for digit 8 looks like a small win: class 8 accuracy edged up from 3.9% to 4.5%, and 8→7 confusion dropped from 401 to 344. I'll keep it. For the next step I'm planning to average the step 10 and step 12 biases, keep the same templates, and be careful with the remaining three steps. The biggest remaining errors are still 7→9 at 373 and 8→7 at 344.

I'm considering adding templates on channels 14 and 15, since those diagonal-edge channels combined with ink might separate the 7 stroke from the 9 loop, which is where the largest 7→9 confusion sits.

Still writing the class 7 and 9 template code...

Still writing the diagonal templates for 9...

I'm checking whether the diagonal template on channel 14 really catches the backslash stroke of a 7, since the edge detector fires along the boundary of that stroke.

I'm checking which way the digit 7's diagonal stroke runs, since the \ edge detector only fires on strokes going from upper-left to lower-right, and 7's stroke runs the opposite way.

Still writing the channel 15 diagonal templates for digit 7 and 9...

Still writing the channel 15 template for digit 9...

Still working out the diagonal template for the 7-versus-9 case, checking whether the "/" edge filter responds to the stroke direction in digit 7.

Still writing the channel 15 template for digit 7...

Still writing the channel 15 template for digit 7...

Still writing the channel 15 template for digit 7...

Next I'm adding diagonal templates on channels 14 and 15 for digits 4 and 2, and I'll average the step 10 and step 12 biases for step 13.
