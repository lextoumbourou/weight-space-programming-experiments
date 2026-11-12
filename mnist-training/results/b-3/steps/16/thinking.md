The 8s are now overpredicted, at 2297, which is worse than before. I suspect the plateau change is responsible, since it may have shrunk the averaged 8 template's norm and eased the penalty. I'll revert the plateau to 2.5 to match step 14, keeping the crossed 7 and s=1.6, so step 16 is just step 14 again.

Next I'm checking that the crossed 7, the s=1.6 setting, and the bias update all carry over, since the 7 template is now an average of four variants.
