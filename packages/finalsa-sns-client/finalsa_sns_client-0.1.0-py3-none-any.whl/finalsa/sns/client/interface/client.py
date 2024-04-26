from finalsa.common.models import SqsMessage
from typing import Union, Dict, List, Optional
from uuid import uuid4
from abc import ABC, abstractmethod


class SnsClient(ABC):

    @staticmethod
    def default_correlation_id() -> str:
        return str(uuid4())

    @abstractmethod
    def create_topic(self, name: str):
        pass

    @abstractmethod
    def subscription_exists(self, topic_name: str, arn: str) -> bool:
        pass

    @abstractmethod
    def get_all_topics(self) -> List:
        pass

    @abstractmethod
    def get_or_create_topic(self, name: str):
        pass

    @abstractmethod
    def get_topic(self, topic_name: str):
        pass

    @abstractmethod
    def list_subscriptions(self, topic: str) -> List:
        pass

    @abstractmethod
    def subscribe(self, topic_name: str, protocol: str, endpoint: str) -> Dict:
        pass

    @abstractmethod
    def publish_message(self, topic_name: str, payload: Union[Dict, SqsMessage]) -> Dict:
        pass

    @abstractmethod
    def publish(self, topic_name: str, payload: Union[Dict, str], att_dict: Optional[Dict] = {}) -> Dict:
        pass
