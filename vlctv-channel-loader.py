#
# vlctv-channel-loader.py
#
# Takes an m3uplus file produced by m3u4u.com and creates a pickledb file for VLCTV and vlctv-gui.py
# Output file should be reviewed and may need to be tweaked before use
#
# 26 March 2021

import re
from pathlib import Path

# Regex for grabbing channel names from m3u list
channelname = '(tvg-name=")([A-Z,a-z,0-9,\(\),\:,\/,\@,\&,\á,\-,\|,\=,\!, ]+)(")'

# Regex for grabbing channel URLs from m3u list. Change the first part of the URL
# to match your m3u URL. Leave the [0-9]+.ts as is (assuming these are normally numeric values)
channelurl = 'http://your.iptvprovider.com:8089/[0-9]+.ts'

# Get the path to the m3u4u file
m3upath = input('Enter full path for the m3u file to be extracted: ')
try:
    m3u = open(m3upath, 'r')
except:
    print(f'Unable to open {m3upath}. Exiting...')
    exit()

# Enter the name of the channel file to be created (usually named tv.db)
channelfile = input('Enter full path for the new channel file: ')
try:    
    channel = open(channelfile, 'w')
except:
    print(f'Unable to create {channelfile}. Exiting...')
    exit()

# Write the opening curly brace for pickledb {
channel.write('{')

chcounter = 0
urlcounter = 0
foundname = False

# Parse the file for channels and URLs
for line in m3u:
    namematch = re.search(channelname, line)
    if namematch:
        channel.write('"' + namematch.group(2) + '": ')
        chcounter += 1
        foundname = True
    urlmatch = re.search(channelurl, line)
    # Only write a URL if a channel was written, to prevent orphan URLs because the regex may not get every line due to possible odd chars.
    if urlmatch:
        if foundname:
            channel.write('"' + urlmatch.group(0) + '",\n ')
            urlcounter += 1
            foundname = False

# Write the pickledb footer to terminate the list
channel.write('" ": " "}')

# Clean up and close everything
m3u.close()
channel.close()
print(f"Finished load, wrote {chcounter} channels and {urlcounter} URLs.")
