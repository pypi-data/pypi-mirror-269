from finalsa.sqs.client import (
    __version__, SqsServiceImpl, SqsService, SqsException, SqsServiceTest
)
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def test_version():
    assert __version__ is not None


def test_sqs_service_impl():
    assert SqsServiceImpl is not None


def test_sqs_service():
    assert SqsService is not None


def test_sqs_exception():
    assert SqsException is not None


def test_sqs_service_test():
    assert SqsServiceTest is not None


def test_sqs_service_receive_messages():
    service = SqsServiceTest()
    messages = service.receive_messages("test")
    assert messages is not None
    assert len(messages) == 0


def test_sqs_service_send_message():
    service = SqsServiceTest()
    service.send_message("test", {"test": "test"})
    messages = service.receive_messages("test")
    assert messages is not None
    assert len(messages) == 1


def test_sqs_service_send_raw_message():
    service = SqsServiceTest()
    service.send_raw_message("test", {"test": "test"}, {"test": "test"})
    messages = service.receive_messages("test")
    assert messages is not None
    assert len(messages) == 1


def test_sqs_service_delete_message():
    service = SqsServiceTest()
    service.send_message("test", {"test": "test"})
    messages = service.receive_messages("test")
    assert messages is not None
    assert len(messages) == 1
    service.delete_message("test", messages[0].receipt_handle)
    messages = service.receive_messages("test")
    assert messages is not None
    assert len(messages) == 0


def test_sqs_service_get_queue_arn():
    service = SqsServiceTest()
    arn = service.get_queue_arn("test")
    assert arn is not None


def test_consume_message():
    service = SqsServiceTest()
    service.send_message("test", {"test": "test"})
    messages = service.receive_messages("test")
    assert messages is not None


def test_get_queue_attributes():
    service = SqsServiceTest()
    attributes = service.get_queue_attributes("test")
    assert attributes is not None


def test_get_queue_url():
    service = SqsServiceTest()
    url = service.get_queue_url("test")
    assert url is not None
    assert url == "https://sqs.us-east-1.amazonaws.com/123456789012/test"
