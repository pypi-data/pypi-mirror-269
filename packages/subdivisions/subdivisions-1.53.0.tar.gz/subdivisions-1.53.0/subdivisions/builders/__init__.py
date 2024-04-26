import os
from dataclasses import dataclass

from loguru import logger

from subdivisions.base import AWSClientMixin
from subdivisions.config import sub_config
from subdivisions.exceptions import PubSubException


@dataclass
class SubDivisionsBuilder(AWSClientMixin):
    topic: str

    def get_kms_key(self):
        kms = self.get_client("kms")
        response = kms.list_aliases()

        if os.getenv("LOCALSTACK_HOSTNAME_LOCAL") and not response.get("Aliases", []):
            logger.info(f"KMS create key local: {sub_config.pub_key}")
            key = kms.create_key()
            kms.create_alias(
                AliasName=sub_config.pub_key, TargetKeyId=key["KeyMetadata"]["KeyId"]
            )
            response = kms.list_aliases()

        logger.debug(f"KMS Response: {response}")
        pubsub_keys = [
            alias["TargetKeyId"]
            for alias in response["Aliases"]
            if alias["AliasName"] == sub_config.pub_key
        ]
        if pubsub_keys:
            logger.debug(f"Default KMS KeyId found: {pubsub_keys[0]}")
            return pubsub_keys[0]
        raise PubSubException("Encryption Key not available.")
