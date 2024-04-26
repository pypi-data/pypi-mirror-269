from finalsa.sns.client import (
    SnsClient,
    SnsClientImpl,
    SnsClientTest,
    __version__
)
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def test_version():
    assert __version__ is not None


def test_client():
    assert SnsClient is not None


def test_client_impl():
    client = SnsClientImpl()
    assert client is not None


def test_client_test():
    client = SnsClientTest()
    assert client is not None


def test_client_publish():
    client = SnsClientTest()
    response = client.publish("test", "test")
    assert response is not None


def test_client_create_topic():
    client = SnsClientTest()
    response = client.create_topic("test")
    assert response is not None


def test_client_get_topic():
    client = SnsClientTest()
    response = client.get_topic("test")
    assert response is None


def test_client_get_or_create_topic():
    client = SnsClientTest()
    response = client.get_or_create_topic("test")
    assert response is not None
    assert response['name'] == "test"


def test_client_get_all_topics():
    client = SnsClientTest()
    response = client.get_all_topics()
    assert len(response) == 0
    client.create_topic("test")
    response = client.get_all_topics()
    assert len(response) == 1
    client.get_or_create_topic("test")
    response = client.get_all_topics()
    assert len(response) == 1


def test_client_subscription_exists():
    client = SnsClientTest()
    response = client.subscription_exists("test", "test")
    assert response == False
    client.get_or_create_topic("test")
    response = client.subscription_exists("test", "test")
    assert response == False
    client.subscribe("test", "test", "test")
    response = client.subscription_exists("test", "test")
    assert response == True


def test_client_list_subscriptions():
    client = SnsClientTest()
    response = client.list_subscriptions("test")
    assert len(response) == 0

    client.get_or_create_topic("test")
    response = client.list_subscriptions("test")
    assert len(response) == 0
    client.subscribe("test", "test", "test")
    response = client.list_subscriptions("test")
    assert len(response) == 1


def test_publish_message():
    client = SnsClientTest()
    response = client.publish_message("test", "test")
    assert response is not None
    assert len(client.topics["test"]["messages"]) == 1

    respo = client.publish_message("test", {})
    assert respo is not None
    assert len(client.topics["test"]["messages"]) == 2


def test_publish():
    client = SnsClientTest()
    response = client.publish("test", "test")
    assert response is not None
    assert len(client.topics["test"]["messages"]) == 1
    assert client.topics["test"]["messages"][0]["Message"] == "test"


def test_get_topic():
    client = SnsClientTest()
    response = client.get_topic("test")
    assert response is None
    client.get_or_create_topic("test")
    response = client.get_topic("test")
    assert response is not None
    assert response["name"] == "test"


def test_get_or_create_topic():
    client = SnsClientTest()
    response = client.get_or_create_topic("test")
    assert response is not None
    assert response["name"] == "test"
    response = client.get_or_create_topic("test")
    assert response is not None
    assert response["name"] == "test"


def test_create_topic():

    client = SnsClientTest()
    response = client.create_topic("test")
    assert response is not None
    assert response["name"] == "test"
    response = client.create_topic("test")
    assert response is not None
    assert response["name"] == "test"


def test_get_all_topics():
    client = SnsClientTest()
    response = client.get_all_topics()
    assert len(response) == 0
    client.create_topic("test")
    response = client.get_all_topics()
    assert len(response) == 1
    client.get_or_create_topic("test")
    response = client.get_all_topics()
    assert len(response) == 1


def test_subscription_exists():
    client = SnsClientTest()
    response = client.subscription_exists("test", "test")
    assert response == False
    client.get_or_create_topic("test")
    response = client.subscription_exists("test", "test")
    assert response == False
    client.subscribe("test", "test", "test")
    response = client.subscription_exists("test", "test")
    assert response == True


def test_list_subscriptions():
    client = SnsClientTest()
    response = client.list_subscriptions("test")
    assert len(response) == 0

    client.get_or_create_topic("test")
    response = client.list_subscriptions("test")
    assert len(response) == 0
    client.subscribe("test", "test", "test")
    response = client.list_subscriptions("test")
    assert len(response) == 1
