import sys
import os

# set the src folder to be on the sys path, that way 
# we can import from src and actually do tests!

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'src')
sys.path.insert(0, src)
