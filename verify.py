from datetime import datetime
import os.path
import time
from main import run

_file_ = 'export99.dxf'

# time before conversion
print("Converted time: ", datetime.now().strftime("%c"))
run(_file_, None, False)

# check the date/time the file was last modified.
print("Last modified: " + time.ctime(os.path.getmtime(_file_)))
