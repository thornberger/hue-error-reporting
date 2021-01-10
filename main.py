import urllib3
import requests
import threading
from google.cloud import pubsub_v1

# Disable unverified SSL certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

project_id = "craftnote-live"
subscription_name = "projects/craftnote-live/subscriptions/cloud-function-errors"
bridgeIp = "192.168.1.113"
username = "lx-2rUum1alLQS9ncdvxbAoROxKdgv7bsTRsKSl5"
lampId = "6"  # 5: living room, 6: kitchen

# https://192.168.1.113/api/lx-2rUum1alLQS9ncdvxbAoROxKdgv7bsTRsKSl5/lights/6/state

count = 0

def set_light(value):
    hue = max(0, 10 - value) * 10000;

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
    set_light(count)
    count = 0
    threading.Timer(10.0, run).start()


def main():
    run()
    subscribe()



if __name__ == "__main__":
    main()
