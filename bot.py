import requests
from functions import *
import time

i = 1
while True:
    send_message(i)
    i += 1
    time.sleep(1)
