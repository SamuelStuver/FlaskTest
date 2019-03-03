import os
import tempfile
import pytest

from flaskmonitor import monitor


@pytest.fixture
def client():
    db_fd, monitor.app.config['DATABASE'] = tempfile.mkstemp()
    monitor.app.config['TESTING'] = True
    client = monitor.app.test_client()

    with monitor.app.app_context():
        monitor.init_db()

    yield client

    os.close(db_fd)
    os.unlink(monitor.app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
