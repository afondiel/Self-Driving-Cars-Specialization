""".
Sure! Here's the modified code that changes the `pattern` variable to match a 
full stop or period in the file and then adds a new line at the beginning of the 
following word/sentence:



- This code will add a new line after every period in the input file. Is there anything else you would like to know?

"""

import os
import sys
import re

new_file_line = ""
# Add full path of the file that contains the pattern to extract  
file_path_read=".\w6\doc-papers\l2-script.md"
# Add path of new file to write the final result
new_file_write="l2-script"+"-formated"+".md"

# where "." is the pattern to match
pattern = "\. "

# super main
if __name__ == '__main__':

    with open(file_path_read, 'r') as file_appl:
        for line in file_appl.readlines():
            new_file_line = line
            # print(line)
            res = re.sub(pattern,".\n- ", new_file_line)
            with open(new_file_write, 'a') as new_file_appl:
                # res += '\n'
                new_file_appl.write(res)
                # print(line, end='')


