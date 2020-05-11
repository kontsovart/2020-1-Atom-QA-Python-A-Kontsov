import pytest
from ssh_client.remote_commands import SSH
import requests


def test_root(config_ssh):
    hostname, username, password, port_ssh, _ = config_ssh
    with SSH(hostname=hostname, username=username, password=password, port=port_ssh) as ssh:
        commands = [
            'sudo su',
            'cat /var/log/messages | tail',
        ]
        for command in commands:
            if command == 'sudo su':
                ssh.exec_cmd(command, "linuxvmimages.com")
            else:
                data = ssh.exec_cmd(command)
        assert "su: (to root)" in data


def test_nginx_ssh(config_ssh):
    hostname, username, password, port_ssh, port_nginx = config_ssh
    with SSH(hostname=hostname, username=username, password=password, port=port_ssh) as ssh:
        commands = [
            f'ss -tulpn | grep nginx | grep {str(port_nginx)}',
        ]
        for command in commands:
            data = ssh.exec_cmd(command)
        assert str(port_nginx) in data


def test_nginx_http(config_ssh):
    hostname, _, _, _, port_nginx = config_ssh
    data = requests.get(f"http://{hostname}:{port_nginx}")
    assert "CentOS" in data.text


def test_nginx_access_log(config_ssh):
    hostname, username, password, port_ssh, port_nginx = config_ssh
    data = requests.get(f"http://{hostname}:{port_nginx}")
    with SSH(hostname=hostname, username=username, password=password, port=port_ssh) as ssh:
        commands = [
            'cat /var/log/nginx/access.log | tail',
        ]
        for command in commands:
            data = ssh.exec_cmd(command)
        assert "python-request" in data


def test_nginx_remove_port(config_ssh):
    hostname, username, password, port_ssh, port_nginx = config_ssh
    with SSH(hostname=hostname, username=username, password=password, port=port_ssh) as ssh:
        commands = [
            f'firewall-cmd --remove-port={port_nginx}/tcp',
            'systemctl status nginx'
        ]
        for command in commands:
            data = ssh.exec_cmd(command)
        assert "active" in data

        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get(f"http://{hostname}:{port_nginx}", timeout=1)

        commands = [
            f'firewall-cmd --add-port={port_nginx}/tcp',
        ]
        for command in commands:
            ssh.exec_cmd(command)
