import sys
from unittest.mock import MagicMock

sys.modules["board"] = MagicMock()
sys.modules["busio"] = MagicMock()
sys.modules["adafruit_platformdetect"] = MagicMock()
