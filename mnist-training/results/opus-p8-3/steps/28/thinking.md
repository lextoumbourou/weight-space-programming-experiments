Removing the template term or shrinking it might help, since it could be pulling 7s toward 9. I'll try β=0 as a quick test, and I want to tune λ as well. I'm also going to check how the linear sum proxy behaves for the Naive Bayes weights on raw scores.

I'm checking whether the linear sum proxy amplifies strong stroke values beyond their binary effect, which would push low-probability features strongly negative. I'll test β = 1.5 to see whether halving the template term helps, since templates were weaker and the Naive Bayes features seem stronger.
