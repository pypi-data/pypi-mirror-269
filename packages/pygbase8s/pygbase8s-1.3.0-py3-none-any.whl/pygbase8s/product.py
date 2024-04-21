# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 15:56
import time
from abc import ABCMeta, abstractmethod

'''
IDS
'''


class Product(metaclass=ABCMeta):
    """
    GBase 8s 产品抽象类
    """

    def __init__(self):
        self._machine = None
        self._path = None

    @property
    def machine(self):
        """
        返回ids所属的machine实例
        :return: Machine
        """
        return self._machine

    @machine.setter
    def machine(self, machine):
        self._machine = machine

    @property
    def path(self):
        """
        返回ids的path
        :return: str
        """
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def session(self):
        """
        操作当前产品的SSHsession
        :return: SSHsession
        """
        return self.machine.session

    @abstractmethod
    def install(self, pkg_path):  # 执行产品安装
        """
        产品安装
        :param pkg_path: str, 安装包位置
        :return:
        """
        pass


class IDS(Product):
    """
    IDS产品类
    """

    def __init__(self, path, machine):
        """
        :param path: ids的路径
        :param machine: 所属的machine
        """
        super().__init__()
        self._machine = machine
        self._path = path

    def install(self, pkg_path):  # 执行ids安装
        """
        安装ids
        :param pkg_path: 安装包路径
        :return:
        """
        target_path = "/tmp/ids_{}".format(time.time())  # 安装包解压目录
        code, out = self.session.run_cmd(f"rm -rf {self.path}; mkdir -p {target_path} {self.path}")
        if code != 0:
            raise Exception(f"创建ids安装包解压目录 {target_path} 或 安装目录 {self.path}失败, 错误码{code}， 错误信息{out}")
        else:
            code, out = self.machine.run_cmd(
                f"tar -xf {pkg_path} -C {target_path};cd {target_path};./ids_install -i silent -DLICENSE_ACCEPTED=TRUE -DUSER_INSTALL_DIR={self.path}")
            if code != 0:
                raise Exception(f"执行ids安装失败, 错误码{code}， 错误信息{out}")


class CSDK(Product):
    """
    CSDK产品类
    """

    def __init__(self, path, machine):
        """
        :param path: str, csdk路径
        :param machine: 所属machine
        """
        super().__init__()
        self._machine = machine
        self._path = path

    def install(self, pkg_path):  # 执行ids安装
        """
        安装csdk
        :param pkg_path: str， 安装包路径
        :return:
        """
        target_path = "/tmp/csdk_{}".format(time.time())  # 安装包解压目录
        code, out = self.session.run_cmd(f"mkdir -p {target_path} {self.path}")
        if code != 0:
            raise Exception(f"创建csdk安装包解压目录 {target_path} 或 安装目录 {self.path}失败, 错误码{code}， 错误信息{out}")
        else:
            code, out = self.machine.run_cmd(
                f"tar -xf {pkg_path} -C {target_path};cd {target_path};./installclientsdk -i silent -DLICENSE_ACCEPTED=TRUE -DUSER_INSTALL_DIR={self.path}")
            if code != 0:
                raise Exception(f"执行csdk安装失败, 错误码{code}， 错误信息{out}")
