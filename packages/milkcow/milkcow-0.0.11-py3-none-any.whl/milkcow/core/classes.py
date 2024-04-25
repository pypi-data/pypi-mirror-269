from milkcow.core.connections import BaseSqliteDb, Db0, Db1, MilkDb
from milkcow.core.basebufferedsocket import BaseBuffedSocket
from milkcow.common.transcode import ReceiverStore
from milkcow.core.milkcat import milkcat


class SocketTransmitter(BaseBuffedSocket):
    def __init__(self):
        self._self_delete_on_send = True
        super().__init__()

    def send(self):
        super().send()
        if self._self_delete_on_send is True:
            self.wipe()

    def extend(self, key: str, values) -> None:
        '''Extend values in buffer'''
        self._buffer.extend(key, values)

    def items(self):
        '''Return items in buffer'''
        return self._buffer.items()

    def wipe(self):
        '''Clear buffer'''
        self._buffer.wipe()

    def __str__(self):
        return f'SocketTransmitter(...) -> {self._buffer}'

    def __repr__(self):
        return self.__str__()


class MilkCow(MilkDb):
    def __str__(self):
        return f'MilkCow(...) -> {self._store}'

    def __repr__(self):
        return self.__str__()


class JqCow(BaseSqliteDb):
    def __init__(self, key_on: str) -> None:
        super().__init__()
        self.key_on = key_on

    def __str__(self):
        return 'KeyCow(...)'

    def __repr__(self):
        return self.__str__()

    def _prep_values_for_store(self, values: list) -> None:
        del values

    def push_raw(self, raw_json: str):
        pylist = milkcat.load(raw_json)
        self.push_unkeyed(pylist)

    def push_unkeyed(self, pylist: list):
        key_map = milkcat.map_by_key(self.key_on, pylist)
        for k, v in key_map.items():
            self.push(k, v)


class SendCow(Db0):
    def get_sender(self):
        '''Return SocketTransmitter with new data in its buffer'''
        sender = SocketTransmitter()
        sender._self_delete_on_send = True
        for k in self.keys():
            values = self.new(k)
            sender.extend(k, values)
        return sender

    def __str__(self):
        return f'MilkCow(...) -> {self._store}'

    def __repr__(self):
        return self.__str__()


class ObjectCow(Db1):
    def __str__(self):
        return f'ObjectCow(...) -> {self._store}'

    def __repr__(self):
        return self.__str__()


class StringCow(Db1):
    def __str__(self):
        return f'ObjectCow(...) -> {self._store}'

    def __repr__(self):
        return self.__str__()


class Receiver(ReceiverStore):
    def recv(self):
        '''recv classmodel objects into self'''
        buffer = SocketTransmitter()
        buffer.recv()
        for k, v in buffer.items():
            self.extend(k, v)

    def __str__(self):
        return f'Receiver(...) -> {super().__str__()}'

    def __repr__(self):
        return self.__str__()
