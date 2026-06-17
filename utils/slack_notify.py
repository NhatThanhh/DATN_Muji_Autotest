import requests
import json
import os

def send_message(text):
    url = os.getenv("SLACK_WEBHOOK")
    payload = {"text": text}
    requests.post(url, data=json.dumps(payload))

if __name__ == "__main__":
    send_message("Playwright Test Execution Completed. Reports Uploaded!")