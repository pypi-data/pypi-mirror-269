# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List, Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2
from .servo_tuning_param import ServoTuningParam


class SimpleTuning:
    """
    The masses and parameters last used by simple tuning.
    """

    @property
    def is_used(self) -> bool:
        """
        Whether the tuning returned is currently in use by this paramset,
        or if it has been overwritten by a later change.
        """

        return self._is_used

    @is_used.setter
    def is_used(self, value: bool) -> None:
        self._is_used = value

    @property
    def carriage_mass(self) -> Optional[float]:
        """
        The mass of the carriage in kg.
        """

        return self._carriage_mass

    @carriage_mass.setter
    def carriage_mass(self, value: Optional[float]) -> None:
        self._carriage_mass = value

    @property
    def load_mass(self) -> float:
        """
        The mass of the load in kg, excluding the mass of the carriage.
        """

        return self._load_mass

    @load_mass.setter
    def load_mass(self, value: float) -> None:
        self._load_mass = value

    @property
    def tuning_params(self) -> List[ServoTuningParam]:
        """
        The parameters used by simple tuning.
        """

        return self._tuning_params

    @tuning_params.setter
    def tuning_params(self, value: List[ServoTuningParam]) -> None:
        self._tuning_params = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.SimpleTuning
    ) -> 'SimpleTuning':
        instance = SimpleTuning.__new__(
            SimpleTuning
        )  # type: SimpleTuning
        instance.is_used = pb_data.is_used
        instance.carriage_mass = pb_data.carriage_mass if pb_data.has_carriage_mass else None
        instance.load_mass = pb_data.load_mass
        instance.tuning_params = [ServoTuningParam.from_protobuf(item) for item in pb_data.tuning_params]
        return instance
