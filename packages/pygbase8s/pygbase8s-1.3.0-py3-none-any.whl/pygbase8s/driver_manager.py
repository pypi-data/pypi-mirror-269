# coding: utf-8
# @Time    : 2024/4/3 13:32
# @Author  : wangwei
import jaydebeapi
from abc import ABCMeta, abstractmethod

'''
按照DB-API接口规范进行封装
'''


class DriverManager(metaclass=ABCMeta):

    def __init__(self, driver_path):
        self._path = driver_path

    @property
    def path(self):
        return self._path

    @abstractmethod
    def connect(self, *args):
        pass


class JDBCDriver(DriverManager):

    def __init__(self, driver_path):
        super().__init__(driver_path)
        self._path = driver_path

    def connect(self, server, user, dbname=None, params=None):
        if params is None:
            params = {}
        variables_str = ';'.join([f'{key}={value}' for key, value in params.items()])
        if variables_str != '':
            variables_str = f':{variables_str}'
        if dbname:
            url = 'jdbc:gbasedbt-sqli://{ip}:{port}' + f'/{dbname}' + f'{variables_str}'
        else:
            url = 'jdbc:gbasedbt-sqli://{ip}:{port}' + f'{variables_str}'
        conn = jaydebeapi.connect(jclassname='com.gbasedbt.jdbc.Driver',
                                  url=url.format(ip=server.ip, port=server.port),
                                  driver_args=(user.username, user.password),
                                  jars=self._path)
        return conn


