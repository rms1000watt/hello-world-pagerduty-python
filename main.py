import os
import json
import datetime
import requests


def main():
  api_key = get_api_key()
  dedup_key = get_dedup_key("31")
  print(dedup_key)

  # create_event(api_key, "test-service-31", dedup_key)


def get_api_key():
  return os.environ["PD_API_KEY"]


def get_dedup_key(service_str):
  return "dedup-key-%s-%s" %(datetime.datetime.now().isocalendar()[1], service_str)


def create_event(api_key, service_name, dedup_key):
  header = {"Content-Type": "application/json"}

  # https://v2.developer.pagerduty.com/docs/send-an-event-events-api-v2
  payload = {
    "routing_key": api_key,
    "event_action": "trigger",
    "dedup_key": dedup_key,
    "payload": {
      "summary": "Ryan smith test please disregard",
      "source": "ryan-smith-test-please-disregard",
      "severity": "info",
      "component": service_name,
      "class":  "Deployment Notification"
    }
  }

  response = requests.post('https://events.pagerduty.com/v2/enqueue',
    data=json.dumps(payload),
    headers=header)

  if response.json()["status"] == "success":
    print('Incident created with with dedup key (also known as incident / alert key) of ' + '"' + response.json()['dedup_key'] + '"')
  else:
    print(response.text) # print error message if not successful

if __name__ == "__main__":
  main()
