# coding: utf-8
# @Time    : 2024/2/28 12:16
# @Author  : wangwei
import time
import warnings
from pygbase8s.env import ENV

'''
ssh 连接
'''


class SSHSession:
    """
    在指定Machine上执行shell命令的连接类
    """
    def __init__(self, ssh):
        """
        :param ssh: paramiko.SSHClient
        """
        self._ssh = ssh
        self._sftp = None
        self._channel = None
        self._env = ENV()
        self._char_set = 'utf8'
        self._ip = self.ssh.get_transport().sock.getpeername()[0]
        self._cmd_over_flag = "[GBaseTerminal]>"

    @property
    def sftp(self):
        if not self._sftp:
            try:
                self._sftp = self.ssh.open_sftp()
            except Exception as e:
                warnings.warn('SFTP启动失败，不支持文件上传/下载: %s' % e)
        return self._sftp

    @property
    def ssh(self):
        """
        返回当前对象使用的ssh
        :return: ssh
        """
        return self._ssh


    @property
    def ip(self):
        """
        返回当前session连接的服务器ip
        :return: str
        """
        return self._ip


    @property
    def char_set(self):
        """
        返回当前session的字符集
        :return: str
        """
        return self._char_set

    @char_set.setter
    def char_set(self, char_set: str):
        """
        设置当前session的字符集
        :return:
        """
        self._char_set = char_set

    @property
    def env(self):
        """
        返回当前session的env
        :return: env
        """
        return self._env

    @env.setter
    def env(self, env: ENV):
        """
        设置当前session的env
        :param env:
        :return:
        """
        self._env = env

    @property
    def channel(self):
        if not self._channel:
            self._channel = self.ssh.invoke_shell()
            self._channel.send(f"export PS1='{self._cmd_over_flag}'\n".encode(self.char_set))
            time.sleep(2)
            self._channel.recv(8192)
        return self._channel

    def _get_buffer_last_line(self, buffer) -> str:
        context: str = buffer.decode(self.char_set)
        lines = [line for line in context.splitlines() if line.strip() != '']
        last_line = '' if len(lines) == 0 else lines[-1]
        return last_line

    def run_cmd_in_channel(self, cmd, cwd: str = None, username: str = None, timeout: int = None):
        """
        在通道中执行shell命令
        :param cmd: 同 run_cmd
        :param cwd: 同 run_cmd
        :param username: 同 run_cmd
        :param timeout: 同 run_cmd
        :return: stream, 可迭代对象，exp: for text in stream: print(text,end='')
        """
        cmds_str = self._get_runtime_cmd(cmd, cwd, username, timeout)
        self.channel.send(f'{cmds_str}\n'.encode(self.char_set))
        while True:
            buffer = self.channel.recv(8192)
            yield buffer.decode(self.char_set)
            flag = self._get_buffer_last_line(buffer)
            if flag == self._cmd_over_flag:
                break

    def upload(self, local_file, remote_file):
        """
        上传本地文件到machine上
        :param local_file: 本地文件路径
        :param remote_file: machine上的文件路径
        :return:
        """
        self.sftp.put(local_file, remote_file)

    def download(self, remote_file, local_file):
        """
        下载machine上的文件到本地
        :param remote_file: machine上文件路径
        :param local_file: 本地文件路径
        :return:
        """
        self.sftp.get(remote_file, local_file)

    def run_cmd(self, cmd, cwd: str = None, username: str = None, timeout: int = None):
        """
        执行shell命令
        :param cmd: str， 命令字符串
        :param cwd: str, 工作路径
        :param username: str, 执行命令的用户
        :param timeout: int, 命令执行超时时间
        :return: code 命令状态码, out 标准输出+标准错误
        """
        cmds_str = self._get_runtime_cmd(cmd, cwd, username, timeout)
        stdin, stdout, stderr = self.ssh.exec_command(cmds_str, get_pty=True)
        return_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode(self.char_set) + stderr.read().decode(self.char_set)
        return return_code, output

    def _get_runtime_cmd(self, cmd, cwd: str = None, username: str = None, timeout: int = None):
        cmds = [f"export {k}={v}" if v else f'unset {k}' for k, v in self.env.get_variables().items()]
        exec_cmd = cmd if timeout is None else f"timeout -s SIGKILL {timeout}s {cmd}"
        cmds.append(exec_cmd)
        cmds_str = ";".join(cmds)
        if cwd:
            cmds_str = f'cd {cwd}; {cmds_str}'
        if username:
            cmds_str = cmds_str.replace('"', '\\"')
            cmds_str = f'su - {username} --session-command "{cmds_str}"'
        return cmds_str

    def set_char_set(self, char_set):
        """
        设置字符集
        :param char_set: str, utf8、 gbk...
        :return:
        """
        self.char_set = char_set

    def get_char_set(self):
        """
        获取字符集
        :return: str
        """
        return self.char_set

    def close(self):
        """
        关闭连接
        :return:
        """
        if self._sftp:
            self.sftp.close()
        self.ssh.close()
