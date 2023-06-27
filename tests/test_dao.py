from src.dao import (
    add_subscription,
    delete_subscription,
    get_all_subscriptions,
    get_subscription,
)


def test_add_subscription():
    add_subscription("TEST", 1)

    subscription = get_subscription("TEST", 1)
    assert len(subscription) == 1

    delete_subscription("TEST", 1)


def test_delete_subscription():
    add_subscription("TEST", 1)

    subscription = get_subscription("TEST", 1)
    assert len(subscription) == 1

    delete_subscription("TEST", 1)

    subscription = get_subscription("TEST", 1)
    assert len(subscription) == 0
