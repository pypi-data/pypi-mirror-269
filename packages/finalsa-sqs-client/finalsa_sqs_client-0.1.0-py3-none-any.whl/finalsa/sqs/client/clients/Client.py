from finalsa.sqs.client.exceptions import SqsException
from finalsa.sqs.client.interfaces import SqsService
from finalsa.common.models import (SqsMessage, SqsReponse, to_message_attributes)
from json import dumps
from typing import Dict, List, Callable, Union, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
import boto3
import botocore
import botocore.exceptions


class SqsServiceImpl(SqsService):

    def __init__(
        self,
        get_correlation_id: Callable[[], Union[str, UUID]] = None
    ) -> None:
        self.sqs = boto3.client('sqs')
        if get_correlation_id is not None:
            self.get_correlation_id = get_correlation_id
        else:
            self.get_correlation_id = self.__class__.default_correlation_id

    def receive_messages(
            self,
            queue_url: str,
            max_number_of_messages: int = 1,
            wait_time_seconds: int = 1
    ) -> List[SqsReponse]:
        try:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['SentTimestamp'],
                MaxNumberOfMessages=max_number_of_messages,
                MessageAttributeNames=['All'],
                WaitTimeSeconds=wait_time_seconds
            )
            if 'Messages' not in response:
                return []
            messages = response['Messages']
            message_responses = []
            for message in messages:
                message_responses.append(
                    SqsReponse.from_boto_response(message))
            return message_responses
        except botocore.exceptions.ClientError as err:
            raise SqsException(err, err.response['Error']['Message'])
        except Exception as ex:
            raise SqsException(ex, "No se pudo recibir el mensaje de la cola")

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
        real_data = data
        if isinstance(data, dict):
            real_data = dumps(data)
        try:
            self.sqs.send_message(
                QueueUrl=queue_url,
                MessageAttributes=to_message_attributes(attributes),
                MessageBody=real_data
            )
        except botocore.exceptions.ClientError as err:
            raise SqsException(err, err.response['Error']['Message'])
        except Exception as ex:
            raise SqsException(ex, "No se pudo enviar el mensaje a la cola")

    def delete_message(self, queue_url: str, receipt_handle: str):
        try:
            self.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        except botocore.exceptions.ClientError as err:
            raise SqsException(err, err.response['Error']['Message'])
        except Exception as ex:
            raise SqsException(
                ex, f"The message could not be deleted from the queue {receipt_handle}")

    def get_queue_arn(self, queue_url: str):
        response = self.get_queue_attributes(queue_url)
        return response['Attributes']['QueueArn']

    def get_queue_attributes(self, queue_url: str, ):
        response = self.sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=[
                'All',
            ]
        )
        return response

    def get_queue_url(self, queue_name: str):
        response = self.sqs.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']
