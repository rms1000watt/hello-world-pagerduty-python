import os
import json
import time
import datetime
import requests

# https://v2.developer.pagerduty.com/docs/send-an-event-events-api-v2

def get_api_key():
  return os.environ["PD_API_KEY"]


def get_dedup_key(service_str):
  return "dedup-key-%s-%s" %(datetime.datetime.now().isocalendar()[1], service_str)


def resolve_event(api_key, service_name, dedup_key):
  print("Resolving Event: service_name=%s dedup_key=%s" %(service_name, dedup_key))

  payload = {
    "routing_key": api_key,
    "event_action": "resolve",
    "dedup_key": dedup_key
  }

  make_request(payload)


def create_event(api_key, service_name, dedup_key):
  print("Creating Event: service_name=%s dedup_key=%s" %(service_name, dedup_key))

  payload = {
    "routing_key": api_key,
    "event_action": "trigger",
    "dedup_key": dedup_key,
    "payload": {
      "summary": "Ryan smith test please disregard",
      "source": "ryan-smith-test-please-disregard",
      "severity": "warning",
      "component": service_name,
      "class":  "Deployment Notification"
    }
  }

  make_request(payload)


def make_request(payload):
  headers = {"Content-Type": "application/json"}
  try:
    response = requests.post('https://events.pagerduty.com/v2/enqueue',
      data=json.dumps(payload),
      headers=headers)

    if response.json()["status"] == "success":
      print("Success")
    else:
      print("Failed: status=%s response=%s" %(response.json()["status"], response.text))
  except Exception as e:
    print("Failed: %s" %(e))


def main():
  api_key = get_api_key()
  dedup_key = get_dedup_key("31")

  create_event(api_key, "test-service-31", dedup_key)

  print("Sleeping 60s")
  time.sleep(60)

  resolve_event(api_key, "test-service-31", dedup_key)


if __name__ == "__main__":
  main()
