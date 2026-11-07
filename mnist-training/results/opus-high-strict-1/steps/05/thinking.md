The penalty is too weak for 8, which pulls in almost everything since it expects ink nearly everywhere, and the same penalty bites harder on sparse templates. 0 and 1 got better, but 7 started turning into 9. I'm thinking about normalizing the penalty per class or adding per-class bias terms instead, since the only feedback I have is the confusion matrices.

I'm weighing per-class normalization of the penalty so that its expected value under random ink is the same for every digit, since 8's small empty set would otherwise be scaled up too heavily. Bias terms for each class are the other option, and I'm considering a smaller penalty weight alongside them.

I'm working out how to normalize the penalty so each class's expected value under random ink is equal, which keeps 8's small empty set from being scaled up too heavily. I'm setting the scale from the average template-to-mean overlap with a weight of 0.5. I'm also considering per-class bias terms for later, and noting that 7 drifting toward 9 may come from 7's sparse template taking the full penalty for any extra stroke.

I'm going to make the penalty per class so each digit's expected penalty under random ink is the same, which should stop 8 from getting scaled up too heavily. I'm setting that scale from the average template-to-mean overlap with a weight of 0.5, and I'll keep the other changes as they are.
