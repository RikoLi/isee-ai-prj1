import time
from n_puzzle_state_main import *

# Multi-times Performance test
times = 30
s = 0
for i in range(times):
    start = time.clock()
    main()
    end = time.clock()
    s = s + end - start

print('Average duration:', s/times)