import logging
from google.cloud import pubsub_v1

logger = logging.getLogger(__name__)


class PubSubClient:
    def __init__(
        self,
        project_id: str,
        topic: str,
    ):
        logger.info(f"Creating publisher client..")
        self._publisher_client = pubsub_v1.PublisherClient()

        self._topic_path = self._publisher_client.topic_path(
            project_id,
            topic,
        )
        logger.debug(f"{self._topic_path=}")

    def publish(self, msg: str | bytes) -> None:
        # Convert the message to bytes.
        if isinstance(msg, str):
            msg_bytes: bytes = msg.encode("utf-8")
        else:
            msg_bytes = msg

        # Publish the message to topic.
        future = self._publisher_client.publish(self._topic_path, data=msg_bytes)

        # block until the message has been published successfully
        message_id = future.result()

        logger.info(f"Message '{msg}' published. Message ID {message_id}")
