import sys, os

# set the src folder to be on the sys path, that way 
# we can import from src and actually do tests!

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.join(root, 'Src')
sys.path.insert(0, root)