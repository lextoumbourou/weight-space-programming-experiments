I'm weighing whether the penalty for splitting the female group is too heavy, so I'm considering lighter values for units 2 and 9. The model seems to predict death too often, with far more false negatives than false positives, so I'm wondering whether shifting the bias or threshold would help the loss.

I'm thinking about nudging the overall bias up by about 0.15, since the model predicts death more often than it should. I'm weighing whether to test that alone or alongside a milder split penalty, and I'm leaning toward keeping the changes separate.
