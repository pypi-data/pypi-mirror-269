# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 21:22
import re
from abc import ABCMeta, abstractmethod

'''
sqlhost实例
'''


class SQLHosts(metaclass=ABCMeta):
    """
    sqlhosts文件抽象类
    """
    def __init__(self):
        self._name = None
        self._product = None

    @property
    def name(self):
        """
        返回sqlhosts实例的名称
        :return: str
        """
        return self._name

    @property
    def session(self):
        """
        返回操作当前实例的SSHSession
        :return: SSHSession
        """
        return self._product.session

    @property
    @abstractmethod
    def path(self):
        """
        返回文件路径
        :return: str
        """
        pass

    def initialize(self):
        """
        文件初始化
        :return:
        """
        code, out = self.session.run_cmd(f"rm -rf {self.path};touch {self.path}")
        if code != 0:
            raise Exception(f"创建sqlhosts文件失败，错误码{code}, 错误信息{out}")


class CMSQLHosts(SQLHosts):  # 一个实例对应一个集群
    """
    CM的sqlhosts文件类
    """

    def __init__(self, csdk, name):
        """
        :param csdk: CSDK, csdk实例
        :param name: str，文件名称
        """
        super().__init__()
        self._csdk = csdk
        self._name = name
        self._product = self.csdk

    @property
    def csdk(self):
        """
        返回对应的csdk实例
        :return: CSDK
        """
        return self._csdk

    @property
    def path(self):
        """
        返回当前文件的路径
        :return: str
        """
        return f"{self.csdk.path}/etc/sqlhosts.{self.name}"

    def add_group(self, group_name, i, c):
        """
        添加组
        :param group_name: 组名
        :param i: any, 组信息中i的值
        :param c: any, 组信息中c的值
        :return:
        """
        code, out = self.session.run_cmd(f"echo '{group_name}\tgroup\t-\t-\ti={i},c={c}' >> {self.path}")
        if code != 0:
            raise Exception(f"写入group信息到sqlhosts文件失败，错误码{code}, 错误信息{out}")

    def add_server_to_group(self, server, group_name):
        """
        在指定组中添加server
        :param server: SERVER
        :param group_name: str, 组名称
        :return:
        """
        code, out = self.session.run_cmd(
            f"echo '{server.name}\tonsoctcp\t{server.ip}\t{server.port}\tg={group_name}' >> {self.path}")
        if code != 0:
            raise Exception(f"server信息写入CM sqlhosts文件失败，错误码{code}, 错误信息{out}")


class ServerSQLHosts(SQLHosts):
    """
    SERVER的sqlhosts文件类
    """

    def __init__(self, ids, name):
        """
        :param ids: IDS
        :param name: 文件名称
        """
        super().__init__()
        self._ids = ids
        self._name = name
        self._servers = {}
        self._product = self.ids

    @property
    def servers(self):
        if len(self._servers) == 0:
            code, out = self.session.run_cmd(f'cat {self.path}')
            if code != 0:
                self._servers = {}
            else:
                self._servers = self._gen_servers_map(out)
        return self._servers

    @staticmethod
    def _gen_servers_map(out: str):
        _servers = {}
        lines = out.splitlines()
        for line in lines:
            match = re.match('(\w+)\s+onsoctcp\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+)', line)
            if match:
                _servers[match.group(1)] = (match.group(2), match.group(3))
        return _servers

    @property
    def ids(self):
        """
        返回对应的IDS实例
        :return: IDS
        """
        return self._ids

    @property
    def path(self):
        """
        返回文件路径
        :return: str
        """
        return f"{self.ids.path}/etc/sqlhosts.{self.name}"

    def add_server(self, servername, ip, port):
        """
        添加server到sqlhosts
        :param servername: str, server名称
        :param ip: str, ip
        :param port: int, port
        :return:
        """
        if servername in self._servers:
            if (ip, port) == self.servers.get(servername):
                return
            else:
                code, out = self.session.run_cmd(f"sed -ri 's#{servername}\s+.*#{servername} onsoctcp {ip} {port}#g' {self.path}")
                if code != 0:
                    raise Exception(f"修改sqlhosts文件中实例{servername}的信息失败，错误码{code}， 错误信息{out}")
        self._servers[servername] = (ip, port)
        code, out = self.session.run_cmd(f"echo {servername} onsoctcp {ip} {port} >> {self.path}")
        if code != 0:
            raise Exception(f"添加server到sqlhosts失败，错误码{code}, 错误信息{out}")

    def get_port(self, server_name):
        """
        获取指定实例的端口号
        :param server_name: str, server name
        :return: int
        """
        if server_name not in self.servers:
            raise Exception(f"实例 {server_name} 不存在")
        return self.servers.get(server_name)[1]

    def get_ip(self, server_name):
        """
        获取指定server的ip
        :param server_name: str, server name
        :return: str
        """
        if server_name not in self.servers:
            raise Exception(f"实例 {server_name} 不存在")
        return self.servers.get(server_name)[0]
