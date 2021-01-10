from google.cloud import pubsub_v1

project_id = "craftnote-live"
subscription_name = "projects/craftnote-live/subscriptions/cloud-function-errors"


def main():
    subscriber = pubsub_v1.SubscriberClient()
    def callback(message):
        print(message.data)
        message.ack()

    future = subscriber.subscribe(subscription_name, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()

if __name__ == "__main__":
    main()