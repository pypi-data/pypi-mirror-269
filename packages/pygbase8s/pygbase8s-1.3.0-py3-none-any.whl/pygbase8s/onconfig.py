# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 20:59

"""
onconfig实例,对应实例或CM
"""

from abc import ABCMeta, abstractmethod
from multiprocessing import Array, Lock


class Onconfig(metaclass=ABCMeta):
    """
    onconfig文件抽象类
    """
    def __init__(self):
        self._name = None
        self._product = None

    @property
    def name(self):
        """
        返回配置名称
        :return: str
        """
        return self._name

    @property
    def session(self):
        """
        返回操作文件的SSHSession
        :return: SSHSession
        """
        return self._product.session

    @property
    @abstractmethod
    def path(self):
        """
        返回文件的路径
        :return: str
        """
        pass

    @abstractmethod
    def initialize(self):
        """
        初始化配置文件
        :return:
        """
        pass

    def get_variable(self, key):
        """
        获取指定该参数的值
        :param key: str，参数名称
        :return: str
        """
        code, out = self.session.run_cmd(f"grep -E '^{key}(\s*|\s+.*)$' {self.path}")
        if code != 0:
            raise Exception(f"获取onconfig变量失败，错误码{code}, 错误信息{out}")
        return out.split(maxsplit=1)[1]

    def set_variable(self, key, value):
        """
        设置指定参数的值
        :param key: str, 参数名称
        :param value: str, 值
        :return:
        """
        if key in ['VPCLASS', 'BUFFERPOOL']:
            regx = '^' + key + '\s+' + value.split(',')[0] + '.*'
        else:
            regx = '^' + key + '(\s*|\s+.*)$'
        grepcmd = f"grep -E '{regx}' {self.path}"
        code, out = self.session.run_cmd(grepcmd)
        if out == "":  # 要修改的参数不存在
            code, out = self.session.run_cmd(f"echo '{key} {value}' >> {self.path}")
        else:
            code, out = self.session.run_cmd(f"sed -ri 's#{regx}#{key} {value}#g' {self.path}")
        if code != 0:
            raise Exception(f"修改onconfig参数失败，错误码{code}, 错误信息{out}")


class CMOnconfig(Onconfig):
    """
    CM配置文件类
    """
    def __init__(self, csdk, name):
        """
        :param csdk: CSDK， csdk实例
        :param name: str，配置文件名称
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
        返回文件路径
        :return: str
        """
        return f"{self.csdk.path}/etc/oncmsm.{self.name}"

    def initialize(self):
        """
        初始化配置文件
        :return:
        """
        code, out = self.session.run_cmd(f"rm -rf {self.path}; "
                                         f"touch {self.path}; chown gbasedbt:gbasedbt {self.path}")
        if code != 0:
            raise Exception(f"创建onconfig.{self.name}失败，错误码{code}, 错误信息{out}")
        self.set_variable('NAME', self.name)
        self.set_variable('LOGFILE', '${GBASEDBTDIR}/tmp/%s.log' % self.name)
        self.set_variable('CM_TIMEOUT', '30')
        self.set_variable('SECONDARY_EVENT_TIMEOUT', '15')
        self.set_variable('SQLHOSTS', 'LOCAL')
        self.set_variable('LOCAL_IP', self.session.ip)
        self.set_variable('EVENT_TIMEOUT', '30')
        self.set_variable('LOG', '1')
        self.set_variable('DEBUG', '0')
        self.set_variable('CLUSTER', 'cluster1')

    def add_cluster_info(self, cluster_info):
        """
        添加cluster信息
        :param cluster_info: str，集群信息
        :return:
        """
        code, out = self.session.run_cmd("echo '{\n%s\n}' >> %s" % (cluster_info, self.path))
        if code != 0:
            raise Exception(f"添加cluster信息到cmonconfig文件失败，错误码{code}, 错误信息{out}")


class ServerOnconfig(Onconfig):
    """
    SERVER配置文件类
    """
    def __init__(self, ids, name):
        """
        :param ids: IDS，ids实例
        :param name: str，配置名称
        """
        super().__init__()
        self._ids = ids
        self._name = name
        # self._backup_file = None
        self._backup_file = Array('c', ''.encode())
        self._lock = Lock()
        self._product = self.ids

    @property
    def ids(self):
        """
        返回配置对应的IDS实例
        :return: IDS
        """
        return self._ids

    @property
    def path(self):
        """
        返回文件路径
        :return: str
        """
        return f"{self.ids.path}/etc/onconfig.{self.name}"

    def initialize(self):
        """
        配置文件初始化
        :return:
        """
        code, out = self.session.run_cmd(f"cp -rfp onconfig.std onconfig.{self.name}", cwd=f"{self.ids.path}/etc")
        if code != 0:
            raise Exception(f"复制onconfig.std失败，错误码{code}, 错误信息{out}")
        self.set_variable("ROOTPATH", "./rootdbs")
        self.set_variable("ROOTSIZE", "204800")
        self.set_variable("DBSERVERNAME", self.name)
        self.set_variable("MSGPATH", "$GBASEDBTDIR/tmp/online_{}.log".format(self.name))
        self.set_variable("FULL_DISK_INIT", "-1")
        self.set_variable("TAPEDEV", "/dev/null")
        self.set_variable("LTAPEDEV", "/dev/null")

    def backup(self):
        """
        配置文件备份
        :return:
        """
        with self._lock:
            if self._backup_file.value == b'':
                self._backup_file = Array('c', f"{self.path}.bak".encode())
                code, out = self.session.run_cmd(f"rm -rf {self.path}.bak;cp -rfp {self.path} {self.path}.bak")
                if code != 0:
                    raise Exception(f"备份{self.name}的onconfig文件失败，错误码{code}, 错误信息{out}")

    def recovery(self):
        """
        配置文件恢复
        :return:
        """
        with self._lock:
            if self._backup_file.value == b'':
                raise Exception(f"onconfig.{self.name}未定义备份文件，无法恢复")
            code, out = self.session.run_cmd(f"rm -rf {self.path};cp -rfp {self._backup_file.value.decode()} {self.path}")
            if code != 0:
                raise Exception(f"恢复{self.name}的onconfig备份文件失败，错误码{code}, 错误信息{out}")
