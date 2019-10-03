#!/usr/bin/python
#
# Script to extract a block of data from an IT-PIE collection file and
# output it in JSON format.
#

import glob
import re
import json
import os

# block_command is a regexp to match beginning and end of block data

block_command = 'cmdShowIpInterfaceB'

# in_block is a flag to indicate if we're processing a block of data

in_block = False

output = []

for fn in glob.glob("sample_collection_engine_data/*"):
    fh = open(fn)

    # Parse filename, expected to be in IT-PIE format

    fn_fields = os.path.basename(fn).split('_')
    ipaddr = fn_fields[1]
    timestamp = fn_fields[2]
    [date, time] = timestamp.split('-')
    
    for line in fh:
        if re.search(block_command, line):
            in_block = not in_block
        if in_block and re.search('YES', line):
            output.append([ipaddr, date, time, line.rstrip()])

print json.dumps(output, indent=4)
