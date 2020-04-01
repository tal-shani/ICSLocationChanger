# -*- coding: utf-8 -*
"""ICS (iCalendar) Location Changer
Bulk change locations of meetings in iCalendar files according to their summary

Requirements:
    * ICS (iCalendar) file to edit
    * Mapping between event names (==summary) and their new location

Usage:
    * Fill in mapping as a Python dictionary inside the user configuration block
    * Complete input/output file paths
    * Run the script
"""

import re

# === User configuration block ===

'''
MEETINGS = {
    'Meeting #1 summary': 'Alternate location',
    'Meeting #2 summary': 'Another alternate location'
}
'''
MEETINGS = {

}

# Path for your ICS input file
INPUT_FILE_PATH = r'path/to/ics/file.ics'

# Output path of new ICS file
OUTPUT_FILE_PATH = r'New_ICS_Schedule.ics'

# === End of user configuration block ===


REG_MEETING_NAME = re.compile('SUMMARY:(.+)\r\n')
REG_LOCATION = re.compile('LOCATION:(.+)\r\n')

with open(INPUT_FILE_PATH,'rb') as f:
    data = f.read()

# Remove padding (if exists) and pack as a clean UTF-8 (BOM-less)
data = data.decode('utf-8-sig').strip('\x00')
data = data.encode('utf-8')

ics_objects = []
object_blocks = data.split('BEGIN:')

for block in object_blocks:
    if block.startswith('VEVENT'):
        
        try:
            # Search for meeting name and proceed only if alternate location exists
            meeting_name = REG_MEETING_NAME.findall(block)[0]
            assert meeting_name in MEETINGS
        except (IndexError, AssertionError):
            ics_objects.append(block)
            continue
        
        edited_block = REG_LOCATION.sub('LOCATION:{0}\r\n'.format(MEETINGS[meeting_name]), block)
        ics_objects.append(edited_block)
    else:
        ics_objects.append(block)

export = 'BEGIN:'.join(ics_objects)

# Return to original encoding
export = export.decode('utf-8').encode('utf-8-sig')

with open(OUTPUT_FILE_PATH, 'wb') as f:
    f.write(export)