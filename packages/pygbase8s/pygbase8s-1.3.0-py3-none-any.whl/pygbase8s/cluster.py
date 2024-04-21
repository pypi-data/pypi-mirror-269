# coding: utf-8
# @Time    : 2024/3/5 10:01
# @Author  : wangwei
from pygbase8s.server import Server


class Cluster:
    """
    具备搭建HDR\RSS\SDS 以及两地三中心的能力
    """

    def __init__(self, primary_node: Server):
        self._primary_node = primary_node
        self._hdr_node = None
        self._sds_nodes = list()
        self._rss_nodes = list()
        self._remote_level0_path = '/tmp/tape_L0'
        self._local_level0_path = 'tape_L0'
        self._new_level0 = True
        self._is_start = False

    @property
    def new_level0(self) -> bool:
        return self._new_level0

    @new_level0.setter
    def new_level0(self, value: bool):
        self._new_level0 = value

    @property
    def remote_level0_path(self):
        return self._remote_level0_path

    @remote_level0_path.setter
    def remote_level0_path(self, path):
        self._remote_level0_path = path

    @property
    def local_level0_path(self):
        return self._local_level0_path

    @local_level0_path.setter
    def local_level0_path(self, path):
        self._local_level0_path = path

    @property
    def primary_node(self):
        return self._primary_node

    @property
    def hdr_node(self):
        return self._hdr_node

    @hdr_node.setter
    def hdr_node(self, hdr: Server):
        self.primary_node.ids.machine.trust(hdr.ids.machine)
        self._hdr_node = hdr
        if self._is_start:
            self.hdr_init()

    @property
    def sds_nodes(self):
        return self._sds_nodes

    @property
    def rss_nodes(self):
        return self._rss_nodes

    def add_sds(self, sds: Server):
        self.primary_node.ids.machine.trust(sds.ids.machine)
        self._sds_nodes.append(sds)
        if self._is_start:
            self.default_sqlhosts_init()
            self._params_common(sds)
            self.sds_init(sds, is_primary=False)

    def add_rss(self, rss: Server):
        self.primary_node.ids.machine.trust(rss.ids.machine)
        self._rss_nodes.append(rss)
        if self._is_start:
            self.default_sqlhosts_init()
            self._params_common(rss)
            if len(self.rss_nodes) == 1:
                self.primary_node.run_cmd("onmode -wf LOG_INDEX_BUILDS=1")
            self.rss_init(rss)

    def remove_rss(self, rss: Server):
        self.primary_node.run_cmd(f"onmode -d delete RSS {rss.name}")

    def get_all_slaves(self):
        slaves = []
        slaves.extend(self.sds_nodes)
        slaves.extend(self.rss_nodes)
        if self.hdr_node:
            slaves.append(self.hdr_node)
        return slaves

    @staticmethod
    def _params_common(node: Server):
        node.onconfig.set_variable('DRINTERVAL', '30')
        node.onconfig.set_variable('DRTIMEOUT', '30')
        node.onconfig.set_variable('UPDATABLE_SECONDARY', '0')
        node.onconfig.set_variable('DRLOSTFOUND', '$GBASEDBTDIR/etc/dr.lostfound')

    def sds_init(self, node: Server, is_primary: False):
        tmp_path = f'{node.path}_tmp'
        if not is_primary:
            node.onconfig.set_variable('SDS_ENABLED', '1')
        node.onconfig.set_variable('SDS_PAGING', f'{tmp_path}/sdstmp1,{tmp_path}/sdstmp2')
        node.onconfig.set_variable('SDS_TEMPDBS', f'sdstmpdbs1, {tmp_path}_tmp/sdstmpdbs1,2,0,16000')
        self._sds_add_tmp(node, tmp_path)
        if not is_primary:
            if node.ip == self.primary_node.ip:
                node.path = self.primary_node.path
            node.startup()
        else:
            node.initialize()
            code, out = node.run_cmd(f'onmode -d set SDS primary {node.name}')
            if code != 0:
                raise Exception(f"主节点{node.name} set SDS primary {node.name}失败，错误码{code}, 错误信息{out}")

    @staticmethod
    def _sds_add_tmp(node: Server, tmp_path: str):
        code, out = node.run_cmd(f"mkdir -p {node.path} {tmp_path};chmod 755 {node.path} {tmp_path}")
        if code != 0:
            raise Exception(f"节点{node.name}创建存储目录失败，错误码{code}, 错误信息{out}")
        code, out = node.run_cmd(
            'touch sdstmp1 sdstmp2;chown gbasedbt:gbasedbt sdstmp1 sdstmp2;chmod 660 sdstmp1 sdstmp2',
            cwd=f'{tmp_path}')
        if code != 0:
            raise Exception(f"节点{node.name}创建sdstmp失败，错误码{code}, 错误信息{out}")
        code, out = node.run_cmd('touch sdstmpdbs1;chown gbasedbt:gbasedbt sdstmpdbs1; chmod 660 sdstmpdbs1',
                                 cwd=f'{tmp_path}')
        if code != 0:
            raise Exception(f"节点{node.name}创建sdstmpdbs失败，错误码{code}, 错误信息{out}")

    def default_onconfig_init(self):
        nodes = self.get_all_slaves()
        nodes.insert(1, self.primary_node)
        for node in nodes:
            self._params_common(node)

    def default_sqlhosts_init(self):
        slaves = self.get_all_slaves()
        slaves.insert(0, self.primary_node)
        for node in slaves:
            other_nodes = [_node for _node in slaves if _node != node]
            for _node in other_nodes:
                node.sqlhosts.add_server(_node.name, _node.ip, _node.port)

    def backup_restore(self, node_backup: Server, node_restore: Server, strage='FILE'):
        if strage == 'FILE':
            self._backup_restore_with_file(node_backup, node_restore)
        else:
            raise Exception(f"not support the strage <{strage}>")

    def _backup_restore_with_file(self, node_backup: Server, node_restore: Server):
        self._get_backup_file(node_backup)
        node_restore.ids.machine.upload(self.local_level0_path, self.remote_level0_path)
        self._restore_with_file(node_restore, self.remote_level0_path)

    def _get_backup_file(self, node: Server):
        if self.new_level0:
            code, out = node.run_cmd(f"ontape -s -L 0 -t STDIO > {self.remote_level0_path}")
            if code != 0:
                raise Exception(f"节点{node.name}执行0级备份失败，错误码{code}, 错误信息{out}")
            node.ids.machine.download(self.remote_level0_path, self.local_level0_path)
            self.new_level0 = False

    def _restore_with_file(self, node, file):
        code, out = node.run_cmd(f'cat {file}|ontape -p -t STDIO', cwd=node.path)
        if code != 0:
            raise Exception(f"节点{node.name}执行备份恢复失败，错误码{code}, 错误信息{out}")

    def hdr_init(self):
        code, out = self.primary_node.run_cmd(f'onmode -d primary {self.hdr_node.name}')
        if code != 0:
            raise Exception(
                f"节点{self.primary_node.name}执行onmode -d primary {self.hdr_node.name}失败，错误码{code}, 错误信息{out}")
        self.hdr_node._add_chunk_file('rootdbs')
        self.backup_restore(self.primary_node, self.hdr_node)
        code, out = self.hdr_node.run_cmd(f'onmode -d secondary {self.primary_node.name}')
        if code != 0:
            raise Exception(
                f"节点{self.hdr_node.name}执行onmode -d secondary失败，错误码{code}, 错误信息{out}")

    def rss_init(self, rss: Server):
        code, out = self.primary_node.run_cmd(f'onmode -d add RSS {rss.name}')
        if code != 0:
            raise Exception(
                f"节点{self.primary_node.name}执行onmode -d add RSS {rss.name}失败，错误码{code}, 错误信息{out}")
        rss._add_chunk_file('rootdbs')
        self.backup_restore(self.primary_node, rss)
        code, out = rss.run_cmd(f'onmode -d RSS {self.primary_node.name}')
        if code != 0:
            raise Exception(f"节点{rss.name}执行onmode -d RSS {self.primary_node.name}失败，错误码{code}, 错误信息{out}")

    def startup(self):
        self._is_start = True
        if len(self.sds_nodes) > 0:
            self.sds_init(self.primary_node, is_primary=True)
            for node in self.sds_nodes:
                self.sds_init(node, is_primary=False)
        else:
            self.primary_node.initialize()
        if len(self.rss_nodes) > 0:
            self.primary_node.run_cmd('onmode -wf LOG_INDEX_BUILDS=1')
            for node in self.rss_nodes:
                self.rss_init(node)
        if self.hdr_node:
            self.hdr_init()

    def shutdown(self):
        for slave in self.get_all_slaves():
            slave.shutdown()
        self.primary_node.shutdown()
