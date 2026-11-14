The loss is down to 0.2713 with accuracy at 91.69%, and six steps remain. Next I'll tune the long-stroke vote (sH) and the presence weight (s), since the earlier finding that the end features were over-weighted hints that presence may be more reliable than I assumed. I'll test raising s from 0.25 to 0.30 while keeping T fixed.

Since ends looked over-weighted, lowering them helped, which makes me think presence may deserve relatively more weight than I assumed. I'll test raising s to 0.30 first, since the heavy-vote change earlier came out neutral, then check sH afterward.
