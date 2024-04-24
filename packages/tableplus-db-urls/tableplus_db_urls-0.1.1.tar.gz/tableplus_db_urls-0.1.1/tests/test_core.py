import tempfile

import pytest
from tableplus.core import build_db_url
from tableplus.core import get_local_db_conn_str
from tableplus.core import get_prod_db_conn_str


@pytest.fixture()
def temp_env():
    """Create a temporary .env file."""
    temp = tempfile.NamedTemporaryFile(suffix=".env", delete=False)
    temp.write(b"POSTGRES_USER=user\nPOSTGRES_PASSWORD=pass\nPOSTGRES_DB=path")
    temp.close()
    return temp


def test_build_db_url():
    params = {"foo": "bar"}
    url = build_db_url("user", "pass", "path", params=params)
    assert url == "postgresql://user:pass@127.0.0.1:5432/path?foo=bar"


def test_build_db_url_with_ssh():
    params = {"foo": "bar"}
    url = build_db_url(
        "user", "pass", "path", ssh_user="testuser", ssh_host="127.0.0.1", params=params
    )

    assert (
        url == "postgresql://testuser@127.0.0.1/user:pass@127.0.0.1:5432/path?foo=bar"
    )


def test_get_local_db_conn_str(temp_env):
    conn_str = get_local_db_conn_str(temp_env.name)
    assert conn_str.startswith("postgresql://user:pass@127.0.0.1:5432/path")


def test_get_prod_db_conn_str(temp_env):
    conn_str = get_prod_db_conn_str(
        temp_env.name, ssh_user="testuser", ssh_host="127.0.0.1"
    )
    assert conn_str.startswith(
        "postgresql+ssh://testuser@127.0.0.1/user:pass@127.0.0.1:5432/path"
    )
