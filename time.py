from datetime import datetime
import time

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

print(current_time)