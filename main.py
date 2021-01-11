import urllib3
import requests
import threading
from google.cloud import pubsub_v1

# Disable unverified SSL certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO use this: https://cloud.google.com/community/tutorials/delivering-cloud-monitoring-notifications-to-third-party-services
# TODO read from config

project_id = "craftnote-live"
subscription_name = "projects/craftnote-live/subscriptions/cloud-function-errors"
bridgeIp = "192.168.1.113"
username = "lx-2rUum1alLQS9ncdvxbAoROxKdgv7bsTRsKSl5"
lampIds = ["18","19"]  # 5: living room, 6: kitchen, 18 studio links

count = 0

def set_lights(value):
    min_value = 0
    max_value = 5
    scaling_factor = 4000
    hue = max(min_value, max_value - value) * scaling_factor

    for lampId in lampIds:
        set_lamp_color(lampId, hue)

def set_lamp_color(lampId, hue):
    url = f"https://{bridgeIp}/api/{username}/lights/{lampId}/state"
    body = {"on": True, "sat": 254, "bri": 254, "hue": hue}
    r = requests.put(url, json=body, verify=False)
    print(r.text)

def subscribe():
    subscriber = pubsub_v1.SubscriberClient()

    def callback(message):
        print(message.data)
        global count
        count = count + 1
        message.ack()

    future = subscriber.subscribe(subscription_name, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()


def run():
    global count
    print(f"The count was {count}")
    set_lights(count)
    count = 0
    threading.Timer(10.0, run).start()


def main():
    run()
    subscribe()



if __name__ == "__main__":
    main()
