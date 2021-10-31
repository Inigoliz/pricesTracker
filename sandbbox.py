from datetime import datetime
import os

today = datetime.now()
print(today)

path = str(os.path.dirname(os.path.abspath(__file__)))

print(path)

