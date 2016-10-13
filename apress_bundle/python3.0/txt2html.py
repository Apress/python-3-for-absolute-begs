#! /usr/bin/python3.0

"""
Convert text file to HTML page
"""
import re

input_filename = eval(input('Enter a filename:-> '))

output_filename = input_filename.replace('.txt', '.html')
title = input_filename.split('/')
title = title[-1].rstrip('.txt').title()
header = """<html>
<head>
<title>{0!s}</title>
</head>
<body>
<h1>{0!s}</h1>
<p>
""".format(title)
footer = """
</p>
</body>
</html>
"""

# Open file
input_file = open(input_filename)
text = input_file.read()
input_file.close()

# Manipulate text
# Change anything like 'Ashpetal' or 'Ashey Petl' to 'Cinderella'.
text = re.sub('[Aa]sh.*?[Pp](elt|etal)', '<b>Cinderella</b>', text)
# Add <p> tags to newlines after periods etc.
text = re.sub('([\]\".:?!-])\n', '\\1</p>\n<p>', text)
# Add <br> tags to newlines after letters and commas.
text = re.sub('([a-z,;])\n', '\\1<br />\n', text)
# Italicise everything between quotes.
text = re.sub('(".+?")', '<i>\\1</i>', text)
# Make everything bold between asterisks.
text = re.sub('(\W)\*([a-z A-Z]+?)\*(\W)', '\\1<b>\\2</b>\\3', text)
# Underline words between underscores.
text = re.sub('(_\w+?_)', '<u>\\1</u>', text)
# Join up Header, text and footer
text = ''.join([header, text, footer])

# Write out web page
output_file = open(output_filename, 'w')
output_file.write(text)
output_file.close()
print((output_filename, "written out."))
