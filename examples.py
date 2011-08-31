from xml.etree import ElementTree as ET
from basecamp import Basecamp

# Prepare the interaction with Basecamp.
bc = Basecamp('https://yourcompany.projectpath.com', 'username', 'password')

# Get time entries from a company
time_entries = bc.time_entries(5371948)

# Calculate sum of hours
entries = ET.fromstring(time_entries).findall('time-entry/hours')
total_hours = sum([float(str(hours.text)) for hours in entries])

print "Total hours: %f" % total_hours
