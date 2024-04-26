from finalsa.common.models import (SqsReponse)
from typing import Dict, List, Union, Optional
from uuid import uuid4
from datetime import datetime, timezone
from abc import ABC, abstractmethod


class SqsService(ABC):

    @staticmethod
    def default_correlation_id():
        return str(uuid4())

    @abstractmethod
    def receive_messages(
            self,
            queue_url: str,
            max_number_of_messages: int = 1,
            wait_time_seconds: int = 1
    ) -> List[SqsReponse]:
        pass

    @abstractmethod
    def send_message(
            self,
            queue_url: str,
            data: Dict,
            id: str = None,
            topic: str = "default",
            correlation_id: str = None,
            timestamp: datetime = datetime.now(timezone.utc)
    ) -> None:
        pass

    @abstractmethod
    def send_raw_message(
            self,
            queue_url: str,
            data: Union[Dict, str],
            attributes: Optional[Dict] = {}
    ) -> None:
        pass

    @abstractmethod
    def delete_message(self, queue_url: str, receipt_handle: str) -> None:
        pass

    @abstractmethod
    def get_queue_arn(self, queue_url: str) -> str:
        pass

    @abstractmethod
    def get_queue_attributes(self, queue_url: str, ) -> Dict:
        pass

    @abstractmethod
    def get_queue_url(self, queue_name: str) -> str:
        pass
