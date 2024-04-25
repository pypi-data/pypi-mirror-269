import io
import socket
import time
from typing import Optional

import paramiko
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException

from ..model import Protocol, Query, Response
from .base import BaseProtocol
from ..exceptions import ConnectionFailed, ExecutionError, CredentialsError


class SSHProtocol(BaseProtocol):
    name = 'ssh'
    """
    A class used to represent a ssh connection to remote host

    :param host: hostname or ip address of remote server
    :param login: user login for remote connection
    :param password: user password for remote connection
    :param port: ssh port. default 22 If not specified
    :param SSH_CONNECT_TIMEOUT: an optional timeout (in seconds)
        for the TCP connect
    :param EXEC_COMMAND_TIMEOUT: an optional timeout (in seconds)
        for execute command
    """

    SSH_CONNECT_TIMEOUT: int = 60
    EXEC_COMMAND_TIMEOUT: int = 60

    def __init__(self, protocol: Optional[Protocol] = None):
        if not self._connection and protocol:
            self.connect(protocol)

    def connect(self, protocol: Protocol):
        """Open SSH connection to remote host.

        :raises: CreateSSHConnectionError: if failed authentication
            or connection or establishing an SSH session
        """
        host = protocol.host
        login = protocol.username
        password = protocol.password
        port = protocol.port
        ssh_key = protocol.pem_file
        try:
            if password:
                self._connection = paramiko.SSHClient()
                self._connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._connection.connect(
                    hostname=host, username=login,
                    password=password, port=port,
                    look_for_keys=False, allow_agent=False,
                    timeout=SSHProtocol.SSH_CONNECT_TIMEOUT
                )
            elif ssh_key:
                keyfile = io.StringIO(ssh_key)
                self._connection = paramiko.SSHClient()
                self._connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._connection.connect(
                    host, port, login,
                    pkey=RSAKey.from_private_key(keyfile),
                    timeout=SSHProtocol.SSH_CONNECT_TIMEOUT,
                    look_for_keys=False,
                    allow_agent=False
                )
        except AuthenticationException as error:
            raise CredentialsError(str(error))
        except (SSHException, socket.timeout) as exc:
            raise ConnectionFailed(str(exc))
        except Exception as error:
            raise ConnectionFailed(f'SSH connection failed: {error}')

    def close(self):
        """Close SSH connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type: Exception, *args):
        self.close()
        if exc_type is not None:
            return False
        return True

    def execute(self, query: Query) -> Response:
        command = query.command
        sudo = query.sudo
        timeout = query.timeout
        if self._connection is None:
            self.connect()
        stdin, stdout, err = self._connection.exec_command(
            command=command,
            timeout=timeout)
        if sudo:
            stdin.write(sudo + "\n")
            stdin.flush()
            time.sleep(1)
        error = err.read().decode('utf-8')
        if not stdout and error:
            raise ExecutionError(error + stdout.read().decode('utf-8') + f'\nCommand: {command}')
        else:
            return Response(result=stdout.read().decode('utf-8'), status=True, text='Command executed successfully')
