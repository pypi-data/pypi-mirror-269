# coding: utf-8
# @Time    : 2024/3/5 9:35
# @Author  : wangwei
import os

class DBSpace:
    """
    GBase 8s数据库数据空间类
    """
    def __init__(self, dbsinfo: dict):
        """
        :param dbsinfo: dict, 数据空间信息
        """
        self._number = dbsinfo.get('number')
        self._name = dbsinfo.get('name')
        self._owner = dbsinfo.get('owner')
        self._pgsize = dbsinfo.get('pgsize')
        self._fchunk = dbsinfo.get('fchunk')
        self._nchunks = dbsinfo.get('nchunks')
        self._flags = dbsinfo.get('flags')
        self._address = dbsinfo.get('address')
        self._chunks = None
        self._server = None

    @property
    def server(self):
        """
        返回数据空间所属的SERVER
        :return: SERVER
        """
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    @property
    def number(self):
        """
        返回number字段的值
        :return: str
        """
        return self._number

    @property
    def address(self):
        """
        返回address字段的值
        :return: str
        """
        return self._address

    @property
    def name(self):
        """
        返回name字段的值
        :return: str
        """
        return self._name

    @property
    def owner(self):
        """
        返回owner字段的值
        :return: str
        """
        return self._owner

    @property
    def pgsize(self):
        """
        返回pgsize字段的值
        :return: str
        """
        return self._pgsize

    @property
    def fchunk(self):
        """
        返回fchunk字段的值
        :return: fchunk
        """
        return self._fchunk

    @property
    def nchunks(self):
        """
        返回nchunks字段的值
        :return: nchunks
        """
        return self._nchunks

    @property
    def flags(self):
        """
        返回flags字段的值
        :return: flags
        """
        return self._flags

    def set_chunks(self, chunk_info_list):
        """
        绑定dbspace和chunks
        :param chunk_info_list: [Chunk]
        :return:
        """
        self._chunks = []
        for chunk_info in chunk_info_list:
            self._chunks.append(Chunk(chunk_info))

    def add_chunk(self, size, offset=0, chunk_name=None, path='.'):
        """
        添加chunk
        :param size: int, 大小， KB
        :param offset: int, 偏移量
        :param chunk_name: str, chunk名称
        :param path: str, chunk路径
        :return:
        """
        index = len(self.get_chunks()) + 1
        _chunk_name = f"{self.name}_{index}" if not chunk_name else chunk_name
        chunk_path = self.server._add_chunk_file(_chunk_name, path)
        code, out = self.server.run_cmd(f"onspaces -a {self.name} -p {chunk_path} -o {offset} -s {size}",
                                     cwd=self.server.path)
        if code != 0:
            raise Exception(f"dbspace {self.name}添加chunk失败，错误码{code}, 错误信息{out}")
        self._update_chunks_info()

    def delete_chunk(self, pathname, offset=0):
        """
        删除chunk
        :param pathname: str, chunk路径
        :param offset: int, 偏移量
        :return:
        """
        code, out = self.server.run_cmd(f"onspaces -d {self.name} -p {pathname} -o {offset} -y")
        if code != 0:
            raise Exception(f"dbspace {self.name}删除chunk失败，错误码{code}, 错误信息{out}")
        self._update_chunks_info()

    def get_chunks(self):
        """
        获取该dbspace的全部chunk
        :return: [Chunk]
        """
        return self._chunks

    def get_size(self):
        """
        返回数据空间大小
        :return: int, KB
        """
        size = 0
        pgsize = int(self.pgsize) / 1024
        for chunk in self.get_chunks():
            size += int(chunk.size)
        size = size * pgsize
        return size

    def get_free_size(self):
        """
        返回数据空间剩余大小
        :return: int
        """
        size = 0
        pgsize = int(self.pgsize) / 1024
        for chunk in self.get_chunks():
            size += int(chunk.free)
        size = size * pgsize
        return size

    def _update_chunks_info(self):
        dbspace = self.server.get_dbspace(self.name)
        self._number = dbspace.number
        self._name = dbspace.name
        self._owner = dbspace.owner
        self._pgsize = dbspace.pgsize
        self._fchunk = dbspace.fchunk
        self._nchunks = dbspace.nchunks
        self._flags = dbspace.flags
        self._address = dbspace.address
        self._chunks = dbspace.get_chunks()


class Chunk:
    """
    Chunk类，对应SERVER中chunk
    """
    def __init__(self, chunk_info: dict):
        """
        :param chunk_info: dict, chunk信息
        """
        self._pathname = chunk_info.get('pathname')
        self._size = chunk_info.get('size')
        self._free = chunk_info.get('free')
        self._dbs = chunk_info.get('dbs')
        self._address = chunk_info.get('address')
        self._offset = chunk_info.get('pathname')
        self._chunk = chunk_info.get('chunk')
        self._metadata = chunk_info.get('metadata', None)

    @property
    def pathname(self):
        """
        返回chunk信息中pathname字段的值
        :return: str
        """
        return self._pathname

    @property
    def size(self):
        """
        返回size字段的值
        :return: str
        """
        return self._size

    @property
    def free(self):
        """
        返回free字段的值
        :return: str
        """
        return self._free

    @property
    def dbs(self):
        """
        返回dbs字段的值
        :return: str
        """
        return self._dbs

    @property
    def address(self):
        """
        返回address字段的值
        :return: str
        """
        return self._address

    @property
    def offset(self):
        """
        返回offset字段的值
        :return: str
        """
        return self._offset

    @property
    def chunk(self):
        """
        返回chunk字段的值
        :return: str
        """
        return self._chunk

    @property
    def metadata(self):
        """
        返回chunk元数据信息
        :return: dict
        """
        return self._metadata
