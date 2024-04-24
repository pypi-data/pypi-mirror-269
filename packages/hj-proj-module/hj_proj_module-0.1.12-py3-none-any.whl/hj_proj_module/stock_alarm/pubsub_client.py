import logging
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from google.auth import default

logger = logging.getLogger(__name__)


class PubSubClient:
    def __init__(
        self,
        project_id: str,
        topic: str,
        keyfile_path: None | str = None,
    ):
        logger.info(f"Creating publisher client..")

        if keyfile_path:
            logger.info("Creating credentials with SA keyfile..")
            self._credentials = service_account.Credentials.from_service_account_file(
                keyfile_path
            )
        else:
            # https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
            logger.info(
                "Creating credentials with Application Default Credentials (ADC).."
            )
            self._credentials, _ = default()

        self._publisher_client = pubsub_v1.PublisherClient(
            credentials=self._credentials
        )

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
