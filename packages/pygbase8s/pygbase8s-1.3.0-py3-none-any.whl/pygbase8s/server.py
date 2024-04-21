# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 12:06
import re
import os
from multiprocessing import Value
from pygbase8s.instance import Instance
from pygbase8s.env import ENV
from pygbase8s.dbspace import DBSpace
from pygbase8s.dblog import LogicalLog
from pygbase8s.onconfig import ServerOnconfig
from pygbase8s.sqlhosts import ServerSQLHosts

'''
实例
'''


class Server(Instance):
    """
    数据库实例类
    """

    def __init__(self, name, ids, onconfig=None, sqlhosts=None):
        """
        :param name: str, 实例名称
        :param ids: IDS，所属的IDS实例
        :param onconfig: ONCONFIG， onconfig实例
        :param sqlhosts: SQLHOSTS， sqlhosts实例
        """
        super().__init__()
        self._ids = ids
        self._name = name
        self._onconfig = onconfig if onconfig else self._get_onconfig()
        self._sqlhosts = sqlhosts if sqlhosts else self._get_sqlhosts()
        self._idle = Value('b', True)
        self._initial = Value('b', True)
        self._path = "{ids_path}/storage/{server_name}".format(
            ids_path=self.ids.path,
            server_name=self.name)
        self._env = ENV()
        self._env.set_variable('GBASEDBTDIR', self.ids.path)
        self._env.set_variable('ONCONFIG', f'onconfig.{self.onconfig.name}')
        self._env.set_variable('GBASEDBTSQLHOSTS', self.sqlhosts.path)
        self._env.set_variable('GBASEDBTSERVER', self.name)
        self._env.set_variable('PATH', f"{self.ids.path}/bin:{self.ids.path}/extend/krakatoa/jre/bin:$PATH")
        self._product = self.ids

    def reconnect(self):
        """
        重建ssh连接
        :return:
        """
        self.ids.machine.reconnect()

    @property
    def ids(self):
        """
        返回对应的IDS实例
        :return: IDS
        """
        return self._ids

    @property
    def onconfig(self):
        """
        :return: Server的onconfig实例
        """
        return self._onconfig

    def _get_onconfig(self):
        onconfig = ServerOnconfig(ids=self.ids, name=self.name)
        onconfig.initialize()
        onconfig.set_variable("SERVERNUM", self.ids.machine.get_available_server_num())
        return onconfig


    @property
    def sqlhosts(self):
        """
        :return: Server的sqlhosts实例
        """
        return self._sqlhosts

    def _get_sqlhosts(self):
        sqlhosts = ServerSQLHosts(ids=self.ids, name=self.name)
        sqlhosts.initialize()
        sqlhosts.add_server(servername=self.name, ip=self.ids.session.ip,
                            port=self.ids.machine.get_available_server_port())
        return sqlhosts

    @property
    def ip(self):  # 返回实例ip
        """
        返回实例的IP地址
        :return: str
        """
        return self.sqlhosts.get_ip(self.name)

    @property
    def port(self):
        """
        返回实例的监听端口
        :return: int
        """
        return self.sqlhosts.get_port(self.name)

    @property
    def path(self):
        """
        返回实例的路径（chunk所在的路径）
        :return: str
        """
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def idle(self):
        """
        返回实例是否空闲
        :return: bool
        """
        return self._idle

    @property
    def initial(self):
        """
        返回实例是否是初始化状态
        :return: bool
        """
        return self._initial

    def initialize(self):  # 初始化实例
        """
        初始化实例
        :return:
        """
        self._add_chunk_file('rootdbs')
        code, out = self.run_cmd("oninit -ivwy", cwd=self.path, username='gbasedbt')
        if code != 0:
            raise Exception(f"实例{self.name}初始化失败，错误码{code}, 错误信息{out}")

    def startup(self):  # 启动实例
        """
        启动实例
        :return:
        """
        code, out = self.run_cmd('oninit -vwy', cwd=self.path, username='gbasedbt')
        if code != 0:
            raise Exception(f"实例{self.name}启动失败，错误码{code}, 错误信息{out}")

    def shutdown(self):  # 关停实例
        """
        关停实例
        :return:
        """
        code, out = self.run_cmd('onmode -ky;onclean -ky', username='gbasedbt')
        if code != 0:
            raise Exception(f"关停实例{self.name}失败，错误码{code}, 错误信息{out}")

    def release(self):  # 设置实例状态为空闲状态
        """
        释放实例(将实例归还实例池)
        :return:
        """
        with self.idle.get_lock():
            self.idle.value = True

    def set_state_initial(self):
        """
        设置实例状态为初始化状态
        :return:
        """
        with self.initial.get_lock():
            self.initial.value = True

    def is_idle(self):  # 返回实例是否空闲
        """
        返回实例空闲与否
        :return: bool
        """
        return self.idle.value

    def is_initial(self):  # 返回实例是否是初始状态
        """
        返回实例是否为初始化状态
        :return: bool
        """
        return self.initial.value

    def occupy(self):  # 设置实例状态为使用状态
        """
        设置实例为使用状态
        :return:
        """
        with self.idle.get_lock():
            self.idle.value = False
            self.initial.value = False

    def _add_chunk_file(self, chunk_name, path='.') -> str:
        """
        实例中创建chunk文件
        :param chunk_name: str， 文件名称
        :param path: str, 指定chunk存储目录
        :return: str, chunk路径
        """
        chunk_path = self.path if path == '.' else path
        self.run_cmd(f"mkdir -p {chunk_path};chmod 755 {chunk_path}")
        code, out = self.run_cmd(f'touch {chunk_name};chmod 660 {chunk_name}; chown gbasedbt:gbasedbt {chunk_name}',
                                 cwd=chunk_path)
        if code != 0:
            raise Exception(f"添加chunk file {chunk_name}失败，错误码{code}, 错误信息{out}")
        chunk_full_path = os.path.join(chunk_path, chunk_name)
        if os.name == 'nt':
            chunk_full_path = chunk_full_path.replace('\\', '/')
        return chunk_full_path

    def add_dbspace(self, name, size, type='BA', offset=0, pagesize=2, chunk_name=None, path='.'):
        """
        添加数据空间
        :param name: str, 空间名称
        :param size: int, 大小，KB
        :param type: int，类型：BA、TBA、BBA、SBA、UBA
        :param offset: int, 偏移量
        :param pagesize: int, 页大小
        :param chunk_name: str, chunk名称
        :param path: str, 指定chunk的存储目录
        :return:
        """
        primary_chunk_name = f"{name}_1" if not chunk_name else chunk_name
        primary_chunk_path = self._add_chunk_file(primary_chunk_name, path)
        if type.upper() == 'BA':
            code, out = self.run_cmd(f"onspaces -c -d {name} -p {primary_chunk_path} -o {offset} -s {size} -k {pagesize}",
                                     cwd=self.path)
        elif type.upper() == 'TBA':
            code, out = self.run_cmd(f"onspaces -c -d {name} -p {primary_chunk_path} -o {offset} -s {size} -k {pagesize} -t",
                                     cwd=self.path)
        elif type.upper() == 'BBA':
            code, out = self.run_cmd(f"onspaces -c -b {name} -g {pagesize} -p {primary_chunk_path} -o {offset} -s {size}",
                                     cwd=self.path)
        elif type.upper() == 'SBA':
            code, out = self.run_cmd(f"onspaces -c -S {name} -p {primary_chunk_path} -o {offset} -s {size}",
                                     cwd=self.path)
        elif type.upper() == 'UBA':
            code, out = self.run_cmd(f"onspaces -c -S {name} -t -p {primary_chunk_path} -o {offset} -s {size}",
                                     cwd=self.path)
        else:
            raise Exception(f'不支持的数据库空间类型{name}, 请输入<BA | TBA | BBA | SBA | UBA>')
        if code != 0:
            raise Exception(f"添加数据据空间{name}失败，错误码{code}, 错误信息{out}")

    def delete_dbspace(self, name):
        """
        删除数据空间
        :param name: str, 空间名称
        :return:
        """
        code, out = self.run_cmd(f"onspaces -d {name} -y", cwd=self.path)
        if code != 0:
            raise Exception(f"删除数据据空间{name}失败，错误码{code}, 错误信息{out}")

    def get_dbspaces(self):
        """
        获取实例上的全部数据空间
        :return: [DBSpace]
        """
        dbspaces = []
        code, out = self.run_cmd("onstat -d")
        if code != 0:
            raise Exception(f"获取实例{self.name}数据空间信息失败，错误码{code}, 错误信息{out}")
        dbspaces_dict = self._get_dbspaces_info(out)
        chunks_dict = self._get_chunks_info(out)
        for name in dbspaces_dict.keys():
            dbs_dict = dbspaces_dict.get(name)
            _dbspace = DBSpace(dbs_dict)
            _dbspace.set_chunks(chunks_dict.get(dbs_dict.get('number')))
            _dbspace.server = self
            dbspaces.append(_dbspace)
        return dbspaces

    def get_dbspace(self, name):
        """
        获取指定名称的数据空间
        :param name: str, 数据空间名称
        :return: DBSpace
        """
        code, out = self.run_cmd("onstat -d")
        if code != 0:
            raise Exception(f"获取实例{self.name}数据空间信息失败，错误码{code}, 错误信息{out}")
        dbspaces_dict = self._get_dbspaces_info(out)
        chunks_dict = self._get_chunks_info(out)
        for _name in dbspaces_dict.keys():
            if _name == name:
                dbs_dict = dbspaces_dict.get(_name)
                dbspace = DBSpace(dbs_dict)
                dbspace.set_chunks(chunks_dict.get(dbs_dict.get('number')))
                dbspace.server = self
                return dbspace
        raise Exception(f'未找到数据空间{name}')

    def add_llog(self, dbspace, size=10240):
        """
        添加逻辑日志
        :param dbspace: DBSpace, 数据空间名称
        :param size: 逻辑日志大小
        :return:
        """
        code, out = self.run_cmd(f'onparams -a -d {dbspace.name} -s {size}')
        if code != 0:
            raise Exception(f"在空间{dbspace.name}中添加逻辑日志失败，错误码{code}, 错误信息{out}")

    def get_llogs(self):
        """
        获取全部逻辑日志
        :return: [LLogs]
        """
        llogs = []
        code, out = self.run_cmd(f'onstat -l')
        if code != 0:
            raise Exception(f"获取逻辑日志失败，错误码{code}, 错误信息{out}")
        llogs_dict = self._get_llogs_info(out)
        for number in llogs_dict.keys():
            llog_dict = llogs_dict.get(number)
            llog = LogicalLog(llog_dict)
            llogs.append(llog)
        return llogs

    def delete_llog(self, llog):
        """
        删除指定逻辑日志
        :param llog: LLog
        :return:
        """
        code, out = self.run_cmd(f'onparams -d -l {llog.number} -y')
        if code != 0:
            raise Exception(f"删除逻辑日志失败，错误码{code}, 错误信息{out}")

    def move_plog(self, dbspace, size=None):
        """
        迁移物理日志
        :param dbspace: DBSpace, 承载物理日志的数据空间
        :param size: int , KB
        :return:
        """
        if not size:
            size = dbspace.get_free_size()
        code, out = self.run_cmd(f'onparams -p -s {size} -d {dbspace.name} -y')
        if code != 0:
            raise Exception(f"迁移物理日志到{dbspace.name}失败，错误码{code}, 错误信息{out}")

    @staticmethod
    def _get_dbspaces_lines(msg, info):
        lines = []
        _block = False
        _title = False
        for line in msg.splitlines():
            line = line.strip()
            if line == "":
                continue
            if _title and re.match('\d+\s+active.*?', line):
                break
            if _title:
                lines.append(line)
            if not _block and line.strip() == info:
                _block = True
                continue
            if _block and not _title and line.startswith('address'):
                _title = True
        return lines

    @staticmethod
    def _get_logs_lines(msg):
        """
        返回指定段的文本行
        :param msg: onstat -l的结果
        :return: 文本行
        """
        lines = []
        _block = False
        for line in msg.splitlines():
            line = line.strip()
            if line == "":
                continue
            if re.match('\d+\s+active.*?', line):
                break
            if line.startswith('address'):
                _block = True
                continue
            if _block:
                lines.append(line)
        return lines

    @staticmethod
    def _get_dbspaces_info(msg):
        dbspaces_info = {}
        lines = Server._get_dbspaces_lines(msg, 'Dbspaces')
        for line in lines:
            info = line.split()
            address, number, fchunk, nchunks, pgsize = info[0], info[1], info[3], info[4], info[5]
            flags = (info[6], info[7])
            owner, name = info[8], info[9]
            dbspaces_info[name] = {
                'number': number,
                'address': address,
                'flags': flags,
                'fchunk': fchunk,
                'nchunks': nchunks,
                'pgsize': pgsize,
                'owner': owner,
                'name': name
            }
        return dbspaces_info

    @staticmethod
    def _get_chunks_info(msg):
        chunks_info = {}    # key是dbs number， value是chunk列表
        _current_chunk = {}
        lines = Server._get_dbspaces_lines(msg, 'Chunks')
        for line in lines:
            info = line.split()
            if info[0] == 'Metadata':
                metadata = {'size': info[1], 'free': info[2], 'bpages': info[3]}
                _current_chunk['metadata'] = metadata
            else:
                address, chunk, dbs, offset, size, free = info[0], info[1], info[2], info[3], info[4], info[5]
                flags, pathname = info[-2], info[-1]
                _current_chunk = {
                        'adddress': address,
                        'chunk': chunk,
                        'dbs': dbs,
                        'offset': offset,
                        'size': size,
                        'free': free[1:] if free.startswith('~') else free,
                        'flags': flags,
                        'pathname': pathname
                    }
                if dbs not in chunks_info:
                    chunks_info[dbs] = [_current_chunk]
                else:
                    chunks_info[dbs].append(_current_chunk)
        return chunks_info

    @staticmethod
    def _get_llogs_info(msg):
        llogs = {}  # key是number， value是列表
        lines = Server._get_logs_lines(msg)
        for line in lines:
            info = line.split()
            address, number, flags, uniqid, begin, size, used, percent_used = info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7]
            _llog = {
                'adddress': address,
                'number': number,
                'flags': flags,
                'uniqid': uniqid,
                'begin': begin,
                'size': size,
                'used': used,
                'percent_used': percent_used
            }
            llogs[number] = _llog
        return llogs

if __name__ == '__main__':
    msg = '''
Your evaluation license will expire on 2025-03-04 00:00:00
On-Line -- Up 00:43:43 -- 156268 Kbytes

Physical Logging
Buffer bufused  bufsize  numpages   numwrits   pages/io
  P-2  23       64       32         6          5.33
      phybegin         physize    phypos     phyused    %used
      1:263            25000      1242       23         0.09

Logical Logging
Buffer bufused  bufsize  numrecs    numpages   numwrits   recs/pages pages/io
  L-3  0        32       883        83         50         10.6       1.7
        Subsystem    numrecs    Log Space used
        OLDRSAM      879        106976
        HA           4          176

address          number   flags    uniqid   begin                size     used    %used
450f0f88         1        U-B----  1        1:25263              5000     5000   100.00
44ed6f30         2        U-B----  2        1:30263              5000     5000   100.00
44ed6f98         3        U-B----  3        1:35263              5000     5000   100.00
44fa5f30         4        U---C-L  4        1:40263              5000      227     4.54
44fa5f98         5        A------  0        1:45263              5000        0     0.00
450d5050         6        A------  0        1:50263              5000        0     0.00
 6 active, 6 total

   '''
    from pprint import pprint

    llogs = Server._get_llogs_info(msg)
    pprint(llogs)
