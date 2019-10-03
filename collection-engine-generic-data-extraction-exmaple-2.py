#!/usr/bin/python
#
# Script to extract a block of data from an IT-PIE collection file and
# output it in JSON format.
#
# by Brent Baccala; 20 Sep 2018

import glob
import re
import json
import os

# block_commands are regexps to match block data

block_commands = [
    {'name' : 'cmdShowIpInterfaceB', 'each_line' : 'YES'},
    {'name' : 'cmdShowArp', 'each_line' : 'Internet'},
    {'name' : 'cmdShowIpRouteVrfAllSummary', 'each_line' : ':'},
    {'name' : 'cmdShowIpArpVrfAll', 'each_line' : 'mgmt'}
]

# in_block is a flag to indicate if we're processing a block of data

in_block = {block['name'] : False for block in block_commands}

output = []

for fn in glob.glob("sample_collection_engine_data/*"):
    fh = open(fn)

    # Parse filename, expected to be in IT-PIE format

    fn_fields = os.path.basename(fn).split('_')
    ipaddr = fn_fields[1]
    timestamp = fn_fields[2]
    [date, time] = timestamp.split('-')
    
    for line in fh:
        for block in block_commands:
            block_name = block['name']
            if re.search(block_name, line):
                in_block[block_name] = not in_block[block_name]
            if in_block[block_name] and re.search(block['each_line'], line):
                output.append([ipaddr, line.rstrip()])

print json.dumps(output, indent=4)
