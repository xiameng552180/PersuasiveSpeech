
import re
import os
test_str = 'this is Xingbo. I am from Wuhan! Nice to meet you; Do you like me?'
idxs = [m.start() for m in re.finditer(r'[\.\?\!]+', test_str)]
ini_idx = 0

for idx in idxs:
    print(test_str[ini_idx:idx+1].strip())
    ini_idx = idx+1
