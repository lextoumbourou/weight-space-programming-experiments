The endpoint penalty looks far too strong, since it wiped out 8 and 0. Endpoint maps seem to be active nearly everywhere, even on 0s and 8s, because endpoint detectors fire on curves and stroke edges too. That suggests β has to be very small, or removed entirely. Meanwhile the change that brought 3 up to 781 might have come from the cusp tip, and I want to check that.

Trying β at zero while keeping the cusp change, to see whether the cusp tip is what lifted 3 and 2. The endpoint detectors might be better made sparser with a higher bias, but I'll test one change at a time first.
