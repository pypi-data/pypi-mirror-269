from loguru import logger
from time import time
import tempfile
import os

Logger = logger

# Logger.configure(
#  handlers=[
#   # dict(sink=sys.stderr, format="[{time}] {message}"),
#   dict(sink=os.path.join(tempfile.gettempdir(), f"{int(time())}.log"), format="[{time}] {message}", enqueue=True, colorize=False),
#  ]
# )
Logger.add(os.path.join(tempfile.gettempdir(), f"{int(time())}.log"), colorize=False, enqueue=True)