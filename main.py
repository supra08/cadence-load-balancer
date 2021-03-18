from socket import error as socket_error

from fabric import Connection
from paramiko.ssh_exception import AuthenticationException


class Host(object):
    def __init__(self,
                 host_ip,
                 username,
                 password):
        self.host_ip = host_ip
        self.username = username
        self.password = password

    def _get_connection(self):
        connect_kwargs = {'password': self.password}
        return Connection(host=self.host_ip, user=self.username, port=22,
                          connect_kwargs=connect_kwargs)

    def run_command(self, command):
        try:
            with self._get_connection() as connection:
                print('Running `{0}` on {1}'.format(command, self.host_ip))
                result = connection.run(command, warn=True, hide='stderr')
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

        if result.failed:
            print (
                'The command `{0}` on host {1} failed with the error: '
                '{2}'.format(command, self.host_ip, str(result.stderr)))

    def put_file(self, local_path, remote_path):
        try:
            with self._get_connection() as connection:
                print('Copying {0} to {1} on host {2}'.format(
                    local_path, remote_path, self.host_ip))
                connection.put(local_path, remote_path)
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

    def _raise_authentication_err(self, exc):
        print (
            "SSH: could not connect to {host} "
            "(username: {user}, key: {key}): {exc}".format(
                host=self.host_ip, user=self.username,
                key=self.key_file_path, exc=exc))


if __name__ == '__main__':
    remote_host = Host(host_ip='<host-ip>',
                       username='<username, e.g. centos>',
                       password='')
    remote_host.put("./monitor.py")
    remote_host.run_command('echo "Hello World"')
    remote_host.run_command('python3 monitor.py')