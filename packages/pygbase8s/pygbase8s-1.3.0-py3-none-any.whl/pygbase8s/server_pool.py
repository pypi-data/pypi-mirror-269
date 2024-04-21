# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 11:56
import time
from threading import Thread
from pygbase8s.cluster import *
from pygbase8s.onconfig import ServerOnconfig
from pygbase8s.sqlhosts import ServerSQLHosts
from multiprocessing import Lock
from paramiko.ssh_exception import SSHException

'''
实例池
'''


class ServerPool:
    """
    GBase 8s实例类资源池
    """
    def __init__(self, ids, count):
        """
        :param ids: IDS， ids实例
        :param count: int, 资源池实例的数量
        """
        self.ids = ids
        self.count = count
        self.base_name = 'gbase'
        self.servers = []
        self.lock = Lock()
        self.ports = []

    @property
    def session(self):
        """
        返回操作当前实例池的SSHSession
        :return: SSHSession
        """
        return self.ids.session

    def initialize(self):  # 初始化实例池中的实例
        """
        初始化资源池，会根据配置的实例数量初始化出指定数量的配置文件
        :return:
        """
        server_nums = self._get_free_server_num(self.count)
        self.ports = self._get_free_server_port(self.count)
        sqlhosts = ServerSQLHosts(ids=self.ids, name=self.base_name)
        sqlhosts.initialize()
        for i in range(self.count):
            server_name = self.base_name + str(i)
            onconfig = ServerOnconfig(ids=self.ids, name=server_name)
            onconfig.initialize()
            onconfig.set_variable("SERVERNUM", server_nums[i])
            sqlhosts.add_server(servername=server_name, ip=self.ids.session.ip, port=self.ports[i])
            server = Server(ids=self.ids, name=server_name, onconfig=onconfig, sqlhosts=sqlhosts)
            self.servers.append(server)
        # 实例池管理线程，用于将空闲但非初始状态的实例恢复到初始状态
        t_manage = Thread(target=self._manage)
        t_manage.daemon = True
        t_manage.start()

    def get_server(self, timeout=None):  # 从实例池中返回一个实例
        """
        返回一个空闲的实例
        :return: Server
        """
        with self.lock:
            start = time.time()
            while True:
                for server in self.servers:
                    if server.is_idle() and server.is_initial():  # 返回一个空闲的实例，并设置为使用状态
                        server.occupy()
                        server.onconfig.backup()
                        return server
                if timeout:
                    if time.time() - start > timeout:
                        raise Exception('获取空闲实例超时')

    def get_cluster(self, type: str):  # 从实例池中返回一个集群
        """
        返回一个指定类型的集群(SDS、HDR、RSS)实例（单机部署）
        :param type: str, 集群类型SDS、HDR或RSS
        :return: Cluster
        """
        primary_node = self.get_server()
        bak_node = self.get_server()
        if type.upper() == 'SDS':
            return SDSCluster(primary_node, bak_node)
        elif type.upper() == 'HDR':
            return HDRCluster(primary_node, bak_node)
        elif type.upper() == 'RSS':
            return RSSCluster(primary_node, bak_node)

    def set_base_name(self, base_name):
        """
        设置实例池中实例的基本名称，如gbase， 则实例的实际名称会是gbase0，gbase1...
        :param base_name: str, 实例的基本名称
        :return:
        """
        self.base_name = base_name

    def _get_free_server_num(self, count):
        server_nums = []
        for i in range(count):
            server_nums.append(self.ids.machine.get_available_server_num())
        return server_nums

    def _get_free_server_port(self, count):
        ports = []
        for i in range(count):
            ports.append(self.ids.machine.get_available_server_port())
        return ports

    def _manage(self):
        while True:
            for server in self.servers:
                if server.is_idle() and not server.is_initial():    # 空闲，但不是初始状态
                    try:
                        server.run_cmd('onclean -ky')
                        server.onconfig.recovery()
                    except SSHException:
                        break
                    server.set_state_initial()  # 修改实例状态为初始化状态
            time.sleep(1)


