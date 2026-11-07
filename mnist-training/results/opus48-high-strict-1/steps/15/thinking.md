Step 14 came in at 40.48%, a bit below step 13's 40.63%, even though the loss improved. The bias shift lifted recall for class 4, but more 9s were misclassified as 4s and recall for 9 fell, so the net effect on accuracy is slightly negative. Step 13 still has the best accuracy, so I'm leaning toward it for the final scored step.

I'm weighing whether to submit step 13's exact biases or a compromise with step 14, since the two differ only slightly on classes 4 and 9. Step 13 has the best observed accuracy and is deterministic, so reverting to its weights should reproduce about 40.63% on validation, and I'll treat that as the safe choice for the final scored step.

I'm going to keep step 13's biases as the final configuration, since it has the best validation accuracy and the others would be untested gambles. I'm also considering whether a midpoint between steps 13 and 14 could do slightly better, though the class shifts between them aren't clearly in one direction.

I'm settling on step 13's biases as the final configuration, since it's the best observed result and reproducing it exactly keeps the outcome predictable.
