# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from ..protobufs import main_pb2
from .io_port_type import IoPortType


class IoPortLabel:
    """
    The label of an IO port.
    """

    @property
    def port_type(self) -> IoPortType:
        """
        The type of the port.
        """

        return self._port_type

    @port_type.setter
    def port_type(self, value: IoPortType) -> None:
        self._port_type = value

    @property
    def channel_number(self) -> int:
        """
        The number of the port.
        """

        return self._channel_number

    @channel_number.setter
    def channel_number(self, value: int) -> None:
        self._channel_number = value

    @property
    def label(self) -> str:
        """
        The label of the port.
        """

        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.IoPortLabel
    ) -> 'IoPortLabel':
        instance = IoPortLabel.__new__(
            IoPortLabel
        )  # type: IoPortLabel
        instance.port_type = IoPortType(pb_data.port_type)
        instance.channel_number = pb_data.channel_number
        instance.label = pb_data.label
        return instance
