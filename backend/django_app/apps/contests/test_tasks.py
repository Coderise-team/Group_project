from unittest.mock import MagicMock, patch

import pytest
from apps.contests.tasks import _broadcast_contest_ended


@pytest.mark.django_db
def test_broadcast_contest_ended_no_channel_layer():
    """When no channel layer is configured, the function returns silently."""
    with patch("channels.layers.get_channel_layer", return_value=None):
        # Should not raise
        _broadcast_contest_ended([1, 2, 3])


@pytest.mark.django_db
def test_broadcast_contest_ended_sends_to_each_contest():
    """Each contest_id gets a 'contest_ended' message sent to its group."""
    sent = []

    fake_layer = MagicMock()

    def fake_async_to_sync(coro_fn):
        """Replace async_to_sync with a sync recorder."""

        def sync_sender(group, message):
            sent.append((group, message))

        return sync_sender

    with (
        patch("channels.layers.get_channel_layer", return_value=fake_layer),
        patch("asgiref.sync.async_to_sync", side_effect=fake_async_to_sync),
    ):
        _broadcast_contest_ended([10, 20])

    assert ("contest_10", {"type": "contest_ended"}) in sent
    assert ("contest_20", {"type": "contest_ended"}) in sent
