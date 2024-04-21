# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 15:49
import paramiko
from pygbase8s.ssh_session import SSHSession
from pygbase8s.env import ENV
from multiprocessing import current_process

'''
服务器
'''


class User:
    """
    操作系统用户类
    """

    def __init__(self, username, password):
        """
        :param username: 用户名称
        :param password: 用户密码
        """
        self.username = username
        self.password = password

    def __str__(self):
        """
        返回用户名
        :return: str
        """
        return self.username


class RemoteMachine:
    """
    机器类，一个IP对应一个实体服务器
    """
    _instance = {}
    _init_flag = None

    def __new__(cls, ip, password, **kwargs):
        if ip not in cls._instance:
            cls._instance[ip] = super().__new__(cls)
            cls._init_flag = True
        else:
            cls._init_flag = False
        return cls._instance[ip]

    def __init__(self, ip, password, port=22, server_num_min=200, port_min=50000):
        """
        :param ip: 服务器ip
        :param password: root用户的密码
        :param port: ssh端口
        :param server_num_min: SERVERNUM的最小范围
        :param port_min: 端口的最小范围
        """
        if self._init_flag:
            self._ip = ip
            self._ssh_port = port
            self.users = {
                'root': User('root', password),
                'gbasedbt': None,
                'general': []
            }
            self._server_num_min = server_num_min
            self._port_min = port_min
            self._general_user = None
            self._session = None
            self._env = ENV()
            self._pid = current_process().pid
            self._master_session = None

    @property
    def session(self):
        """
        返回当前machine的session连接
        :return: SSHSession
        """
        _pid = current_process().pid
        if _pid != self._pid:  # 如果跨进程
            self._master_session = self._session
            self.reconnect()  # 重置self._session
            self._pid = _pid
        elif not self._session:  # 如果session是空
            self.reconnect()
        self._session.env = self.env
        return self._session

    @property
    def env(self):
        """
        返回当前machine的env
        :return:
        """
        return self._env

    def reconnect(self, user_name='root'):
        """
        重建ssh连接
        :param user_name: str, 用户名
        :return:
        """
        self._session = self._create_session(self.users.get(user_name))

    def _create_session(self, user: User):
        transport = paramiko.Transport((self.ip, self.ssh_port))
        transport.connect(username=user.username, password=user.password)
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        return SSHSession(ssh=ssh)

    def run_cmd(self, cmd, **kwargs):
        """
        执行shell命令
        :param cmd: str， 命令字符串
        :param kwargs: cwd： 工作没目录 username: 执行命令的而用户 timeout：超时时间
        :return: code 状态码， out 标准输出+标准错误
        """
        return self.session.run_cmd(cmd, **kwargs)

    def run_cmd_in_channel(self, cmd, **kwargs):
        """
        shell命令
        :param cmd: str, 命令字符串
        :param kwargs: cwd: 工作目录 username: 执行命令的用户 timeout: 超时时间
        :return: stream, exp: for text in stream: print(text, end='')
        """
        return self.session.run_cmd_in_channel(cmd, **kwargs)

    @property
    def ip(self):
        """
        返回ip地址
        :return: str
        """
        return self._ip

    @property
    def ssh_port(self):
        """
        返回ssh服务端口号
        :return: int
        """
        return self._ssh_port

    def add_user(self, user: User):
        """
        添加操作系统用户
        :param user: User类的实例
        :return:
        """
        code, out = self.run_cmd(f"id -u {user.username}")
        if code != 0:
            code, out = self.run_cmd(f"useradd {user.username}")
            if code != 0:
                raise Exception(f"添加用户{user.username}失败")
        code, out = self.run_cmd(f"echo '{user.password}'|passwd --stdin {user.username}")
        if code != 0:
            raise Exception(f"修改用户{user.username}密码失败")
        else:
            if user.username in ('root', 'gbasedbt'):
                self.users[user.username] = user
            else:
                self.users['general'].append(user)

    def _gen_general_user(self):
        for user in self.users.get('general'):
            yield user

    def get_user(self, type):
        """
        获取用户，当用户类型为general时，返回未被使用的用户
        :param type: str， 用户类型：root、gbasedbt、general
        :return: User
        """
        if type in ('root', 'gbasedbt'):
            return self.users.get(type)
        else:
            if self._general_user is None:
                self._general_user = self._gen_general_user()
            return next(self._general_user)

    def get_available_server_num(self):
        """
        获取machine上可用的SERVERNUM
        :return: int
        """
        for check_num in range(self._server_num_min, 256):
            address = str(hex(0x5256 + check_num))
            code, out = self.session.run_cmd(f"ipcs -m|grep {address}")
            if out == "":
                self._server_num_min = check_num + 1
                return check_num
        raise Exception("无可用的SERVERNUM")

    def get_available_server_port(self):
        """
        获取machine上可用的端口
        :return: int
        """
        for check_port in range(self._port_min, 65535):
            code, out = self.session.run_cmd(f"netstat -an|grep {check_port}")
            if out == "":
                self._port_min = check_port + 1
                return check_port
        raise Exception("无可用的端口")

    def upload(self, local_file, remote_file):
        """
        上传本地文件到machine上
        :param local_file: 本地文件路径
        :param remote_file: machine上的文件路径
        :return:
        """
        self.session.upload(local_file, remote_file)

    def download(self, remote_file, local_file):
        """
        下载machine上的文件到本地
        :param remote_file: machine上文件路径
        :param local_file: 本地文件路径
        :return:
        """
        self.session.download(remote_file, local_file)

    def trust(self, *machines):
        """
        配置互信
        :param machine: 与当前machine互信的machine实例
        :return:
        """
        cmd = "echo '+ +'> /etc/hosts.equiv"
        self.run_cmd(cmd)
        for _machine in machines:
            _machine.run_cmd(cmd)


if __name__ == '__main__':
    machine = RemoteMachine('172.16.3.78', 'Big4ifmx')
    machine.download('/tmp/tape_L0', 'tape_L0')
