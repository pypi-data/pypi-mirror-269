# coding: utf-8
# @Time    : 2024/3/6 9:38
# @Author  : wangwei
'''
环境变量
'''


class ENV:
    """
    环境类， 描述shell运行的环境
    """

    def __init__(self):
        self._variables = {}

    def set_variable(self, key, value):
        """
        设置指定环境变量的值
        :param key: str, 变量名称
        :param value: str, 变量的值
        :return:
        """
        self._variables[key] = value

    def unset_variable(self, key):
        """
        取消设置指定环境变量的值
        :param key: str, 变量名称
        :return:
        """
        self._variables[key] = None

    def get_variable(self, key):
        """
        获取指定环境变量的值
        :param key: str, 变量名称
        :return: 变量的值
        """
        return self._variables.get(key, '')

    def get_variables(self):
        """
        获取所有环境变量
        :return: dict
        """
        return self._variables

    def update(self, env):
        """
        使用一个环境实例更新当前实例
        :param env: ENV
        :return:
        """
        self._variables.update(env.get_variables())

    def __str__(self):
        """
        返回设置当前环境中环境变量的shell命令
        :return: str
        """
        return '\n'.join([f"export {k}={v}" if v else f'unset {k}'for k, v in self.get_variables().items()])


if __name__ == '__main__':

    env = ENV()
    env.set_variable('DB_LOCALE', 'zh_CN.utf8')
    env.set_variable('CLIENT_LOCALE', 'zh_CN.utf8')
    env.set_variable('GBASEDBTDIR', '/data/wangwei/gbase8s')
    print(env)
