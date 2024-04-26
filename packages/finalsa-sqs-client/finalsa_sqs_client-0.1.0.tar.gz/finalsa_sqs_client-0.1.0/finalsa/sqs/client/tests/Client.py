from finalsa.sqs.client.interfaces import SqsService
from finalsa.common.models import (SqsReponse, SqsMessage)
from typing import Dict, List, Callable, Union, Optional
from uuid import uuid4, UUID
from json import dumps
from datetime import datetime, timezone


class SqsServiceTest(SqsService):

    def __init__(
        self,
        get_correlation_id: Callable[[], Union[str, UUID]] = None
    ) -> None:
        self.messages = {}
        if get_correlation_id is not None:
            self.get_correlation_id = get_correlation_id
        else:
            self.get_correlation_id = self.__class__.default_correlation_id

    def receive_messages(
            self,
            queue_url: str,
            max_number_of_messages: int = 1,
            _: int = 1
    ) -> List[SqsReponse]:
        if queue_url not in self.messages:
            return []
        messages = self.messages[queue_url]
        if len(messages) == 0:
            return []
        message_responses = []
        while len(messages) > 0 and len(message_responses) < max_number_of_messages:
            message_responses.append(messages.pop(0))
        return message_responses

    def send_message(
            self,
            queue_url: str,
            data: Dict,
            id: str = None,
            topic: str = "default",
            correlation_id: str = None,
            timestamp: datetime = datetime.now(timezone.utc)
    ) -> None:
        if id is None:
            id = str(uuid4())
        if correlation_id is None:
            correlation_id = str(self.get_correlation_id())

        message = SqsMessage(
            id=UUID(id),
            topic=topic,
            payload=dumps(data),
            correlation_id=correlation_id,
            timestamp=timestamp
        )
        self.send_raw_message(queue_url, message.to_dict(), {
            'topic': message.topic,
            'correlation_id': message.correlation_id,
        })

    def send_raw_message(
            self,
            queue_url: str,
            data: Union[Dict, str],
            attributes: Optional[Dict] = {}
    ) -> None:
        if queue_url not in self.messages:
            self.messages[queue_url] = []

        if 'correlation_id' not in attributes:
            attributes['correlation_id'] = str(self.get_correlation_id())

        self.messages[queue_url].append(SqsReponse.from_boto_response({
            'MessageId': str(uuid4()),
            'ReceiptHandle': str(uuid4()),
            'MD5OfBody': str(uuid4()),
            'Body': dumps(data),
            'Attributes': attributes,
            'MessageAttributes': {
                'correlation_id': {'Type': 'String', 'Value': attributes['correlation_id']}
            }
        }))

    def delete_message(self, queue_url: str, receipt_handle: str) -> None:
        if queue_url not in self.messages:
            return
        messages = self.messages[queue_url]
        for i, message in enumerate(messages):
            if message.receipt_handle == receipt_handle:
                messages.pop(i)
                return

    def get_queue_arn(self, _: str) -> str:
        return 'arn:aws:sqs:us-east-1:123456789012:MyQueue'

    def get_queue_attributes(self, _: str, ) -> Dict:
        return {
            "QueueArn": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
            "ApproximateNumberOfMessages": "0",
            "ApproximateNumberOfMessagesNotVisible": "0",
            "ApproximateNumberOfMessagesNotVisible": "0",
            "ApproximateNumberOfMessagesDelayed": "0",
        }

    def get_queue_url(self, queue_name: str) -> str:
        return f"https://sqs.us-east-1.amazonaws.com/123456789012/{queue_name}"
