import pytest


@pytest.fixture(scope="session")
def config_ssh():
    hostname = '192.168.0.102'
    username = 'root'
    password = 'linuxvmimages.com'
    port_ssh = 2022
    port_nginx = 12345
    yield hostname, username, password, port_ssh, port_nginx
