import requests
from config import *


def get_updates():
    return requests.get(url + "getUpdates").json()["result"]


def send_message(text):
    return requests.get(url + "sendMessage?chat_id={0}&text={1}".format(chat_id, text)).json()
