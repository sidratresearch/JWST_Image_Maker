import sys
from importing2 import get_files

filenames = sys.argv[1:]
for i in range(len(filenames)):
    filenames[i] = "/" + filenames[i]

print(filenames)

data = get_files(filenames)
print(data.shape)
