from finalsa.sns.client.interface import SnsClient
from finalsa.common.models import SqsMessage
from typing import Union, Dict, Optional
from json import dumps
from uuid import uuid4
from datetime import datetime, timezone


class SnsClientTest(SnsClient):

    def __init__(self) -> None:
        self.topics = {}
        self.get_correlation_id = self.__class__.default_correlation_id

    def create_topic(self, name: str):
        self.topics[name] = {
            "arn": f"arn:aws:sns:us-east-1:123456789012:{name}",
            "name": name,
            "id": "123456789012",
            "subscriptions": [],
            "messages": []
        }
        return self.topics[name]

    def subscription_exists(self, topic_name: str, arn: str) -> bool:
        if topic_name in self.topics:
            topic = self.topics[topic_name]
            for sub in topic['subscriptions']:
                if sub['Endpoint'] == arn:
                    return True
        return False

    def get_all_topics(self):
        return list(self.topics.keys())

    def get_or_create_topic(self, name: str):
        if name in self.topics:
            return self.topics[name]
        return self.create_topic(name)

    def get_topic(self, topic_name: str):
        return self.topics.get(topic_name, None)

    def list_subscriptions(self, topic: str):
        if topic in self.topics:
            return self.topics[topic]['subscriptions']
        return []

    def subscribe(self, topic_name: str, protocol: str, endpoint: str) -> Dict:
        if topic_name in self.topics:
            topic = self.topics[topic_name]
            if not self.subscription_exists(topic_name, endpoint):
                topic['subscriptions'].append({
                    "Endpoint": endpoint,
                    "Protocol": protocol
                })
                return {}
        return {}

    def publish_message(self, topic_name: str, payload: Union[Dict, SqsMessage]) -> Dict:
        correlation_id = str(self.get_correlation_id())
        message_attrs = {
            'correlation_id':  correlation_id,
            'topic': topic_name
        }
        if isinstance(payload, SqsMessage):
            payload = payload.model_dump_json()
            return self.publish(topic_name, payload, message_attrs)

        message = SqsMessage(
            id=str(uuid4()),
            topic=topic_name,
            payload=dumps(payload),
            correlation_id=correlation_id,
            timestamp=datetime.now(timezone.utc)
        )
        return self.publish(topic_name, message.model_dump_json(), message_attrs)

    def publish(self, topic_name: str, payload: Union[Dict, str], att_dict: Optional[Dict] = {}) -> Dict:
        self.get_or_create_topic(topic_name)
        self.topics[topic_name]['messages'].append({
            "Message": payload,
            "Attributes": att_dict
        })
        return {}

    def clear(self):
        self.topics = {}
    