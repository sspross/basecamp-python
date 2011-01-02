from xml.etree import ElementTree as ET
from basecamp import Basecamp

# Prepare the interaction with Basecamp.
bc = Basecamp('https://yourcompany.projectpath.com', 'username', 'password')

# Get time entries from a company
time_entries = bc.time_entries_report(1734824, 20100101, 20101231)

# Calculate sum of hours
total_hours = 0
for hours in ET.fromstring(time_entries).findall('time-entry/hours'):
    total_hours += float(str(hours.text))

print "Total hours: %f" % total_hours
