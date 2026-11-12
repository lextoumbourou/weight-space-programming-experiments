Accuracy and loss both ticked up a little, and the biases look off now that the new features are in. Digit 4 is strong at 931, with 7 at 905 and 1 at 927. Digits 9 and 3 dropped, and the 5→8 and 3→5 confusions are still showing up. I'm now checking the column sums to see how the biases need rebalancing.

I'm applying the bias adjustments now: nudging 9 and 3 up, and 4, 7, 1, 8 and 2 down. On the 5→8 confusions, the 8 template has no endpoints so it gets zero endpoint weight, while the 5 template does. I'll leave the endpoint strength as it is for now and test the bias change first.
