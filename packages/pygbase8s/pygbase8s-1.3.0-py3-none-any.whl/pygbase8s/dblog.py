# coding: utf-8
# @Time    : 2024/3/13 10:36
# @Author  : wangwei

class LogicalLog:

    def __init__(self, lloginfo: dict):
        self._address = lloginfo.get('address')
        self._begin = lloginfo.get('begin')
        self._flags = lloginfo.get('flags')
        self._number = lloginfo.get('number')
        self._percent_used = lloginfo.get('percent_used')
        self._size = lloginfo.get('size')
        self._uniqid = lloginfo.get('uniqid')
        self._used = lloginfo.get('used')

    @property
    def address(self):
        return self._address

    @property
    def begin(self):
        return self._begin

    @property
    def flags(self):
        return self._flags

    @property
    def number(self):
        return self._number

    @property
    def percent_used(self):
        return self._percent_used

    @property
    def size(self):
        return self._size

    @property
    def uniqid(self):
        return self._uniqid

    @property
    def used(self):
        return self._used