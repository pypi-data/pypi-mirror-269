# coding: utf-8
# @Time    : 2024/3/5 13:39
# @Author  : wangwei
from pygbase8s.instance import Instance
from pygbase8s.env import ENV
from pygbase8s.sqlhosts import CMSQLHosts
from pygbase8s.onconfig import CMOnconfig


class CM(Instance):
    """
    GBase 8s CM类
    """

    def __init__(self, csdk, cluster, name: str = None, port: int = None):
        """
        :param csdk: CSDK
        :param cluster: Cluster
        :param name: str, CM名称
        :param port: int, CM端口
        """
        super().__init__()
        self._csdk = csdk
        self._product = self.csdk
        self._cluster = cluster
        if not port:
            self._port = self.csdk.machine.get_available_server_port()
        else:
            self._port = port
        if not name:
            self._name = "single_cm"
        else:
            self._name = name
        self._sqlhosts = None
        self._onconfig = None
        self._path = self.csdk.path
        self._env = ENV()
        self._env.set_variable('GBASEDBTDIR', self.csdk.path)
        self._env.set_variable('GBASEDBTSQLHOSTS', self.sqlhosts.path)
        self._env.set_variable('GBASEDBTSERVER', None)
        self._env.set_variable('ONCONFIG', self.onconfig.path)
        self._env.set_variable('PATH', f"{self.csdk.path}/bin:$PATH")


    def reconnect(self):
        """
        重新连接machine
        :return:
        """
        self.csdk.machine.reconnect()

    @property
    def onconfig(self):
        """
        :return: CM的onconfig实例
        """
        if not self._onconfig:
            self._onconfig = CMOnconfig(self.csdk, self.name)
            self._onconfig.initialize()
            cluster_info = f'''
            GBASEDBTSERVER db_group
            SLA {self.name} DBSERVERS=ALL WORKERS=16
            FOC ORDER=ENABLED TIMEOUT=10 RETRY=1 PRIORITY=1'''
            self._onconfig.add_cluster_info(cluster_info)
        return self._onconfig

    @property
    def sqlhosts(self):
        """
        :return: CM的sqlhosts实例
        """
        if not self._sqlhosts:
            self._sqlhosts = CMSQLHosts(self.csdk, self.name)
            self._sqlhosts.initialize()
            self._sqlhosts.add_group(group_name='db_group', i=10, c=1)
            self._sqlhosts.add_server_to_group(self.cluster.primary_node, 'db_group')
            for slave_node in self.cluster.get_all_slaves():
                self._sqlhosts.add_server_to_group(slave_node, 'db_group')
            self._sqlhosts.add_group(group_name='cm', i=12, c=0)
            self._sqlhosts.add_server_to_group(self, 'cm')
        return self._sqlhosts

    @property
    def cluster(self):
        """
        :return: CM的集群实例
        """
        return self._cluster

    @property
    def csdk(self):
        """
        返回CM对应的CSDK实例
        :return: CSDK
        """
        return self._csdk

    @property
    def path(self):
        """
        返回CM的path
        :return: str
        """
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def ip(self):
        """
        返回CM的ip地址
        :return: str
        """
        return self.session.ip

    @property
    def port(self):
        """
        返回cm的监听端口
        :return: int
        """
        return self._port

    def startup(self):
        """
        启动CM
        :return:
        """
        code, out = self.run_cmd(f'oncmsm -c {self.onconfig.path}\n', username='gbasedbt')
        if code != 0:
            raise Exception(f"CM启动失败，错误码{code}, 错误信息{out}")

    def shutdown(self):  # 关停实例
        """
        关停CM
        :return:
        """
        code, out = self.run_cmd(f'oncmsm -k {self.name}', username='gbasedbt')
        if code != 0:
            raise Exception(f"关停CM失败，错误码{code}, 错误信息{out}")
