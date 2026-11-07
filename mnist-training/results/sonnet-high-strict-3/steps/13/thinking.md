I'm seeing that the open-top 4 template is over-predicting 4s badly, and accuracy has dropped. I'm weighing reverting to the step 11 network with moderated bias corrections, and I'm leaning toward restoring the closed-top 4 template while keeping the step 12 bias adjustments, since those were computed from step 11.

I'm checking the step 12 bias on 4, which is +0.19 and worth keeping, and I've confirmed the predicted count of 1s adds up to 1181. Keeping the open-4 template and compensating is uncertain, so I'm leaning toward reverting since it's the safer option.
