#! /usr/bin/python

###
# Text unwrapper - removes all line breaks
###

import sys, re

### MAIN ###
# Read text
text = sys.stdin.read()

# Replace stuff #######################
# Format:
# Remove line breaks
text = text.replace("""
""",""" """)
# Remove HTML breaks
text = text.replace("""<br>""","""""")
# Remove all tabs
text = text.replace("""\t""",""" """)
# squish spaces
text = re.sub(" +"," ",text,count=0)

# Print it out again
print text

### END ###
