import datetime
from typing import Any, Dict, Optional
import isodate
from pydantic import BaseModel
from washpy.status import Status


class StateModel(BaseModel):
    """
    captures the output format of the /State endpoint.

    For pExtended: the contents of the field are device specific.
    For the PWM 507 machine, look at the `pExtendedPWM507` class.

    """

    Status: Status
    ProgramID: int
    ProgramPhase: int
    SyncState: int
    pRemainingTime: str
    pElapsedTime: str
    pSystemTime: str
    pStartTime: str
    pEndTime: str
    pLastNotificationTime: str
    ProcessUID: str
    pExtended: Dict[str, Any]


class State:
    """
    Wrapper around `StateModel`.

    This class provides some control logic around
    accessing the properties of `StateModel`.

    Some properties are not always valid,
    largely depending on the value of State.Status
    """

    _model: StateModel

    def __init__(self, **data) -> None:
        self._model = StateModel(**data)

    def __repr__(self) -> str:
        return f"State({self._model.__repr__()})"

    def __str__(self) -> str:
        return self._model.__str__()

    @property
    def Status(self) -> Status:
        """
        This property should always be valid.
        """
        return self._model.Status

    @property
    def ProgramID(self) -> int:
        """
        This property should always be valid.
        """
        return self._model.ProgramID

    @property
    def ProgramPhase(self) -> Optional[int]:
        """
        - None, if the machine is not in the RUNNING state.
        - int: ProgramPhase, a device specific 16 bit integer denoting the program phase
        """
        if self._model.Status != Status.RUNNING:
            return None
        return self._model.ProgramPhase

    @property
    def SyncState(self) -> int:
        return self._model.SyncState

    @property
    def pRemainingTime(self) -> Optional[isodate.Duration | datetime.timedelta]:
        """
        - None, if the machine is not in the RUNNING state, or if the returned date from the machine is not valid.
        - Duration: pRemainingTime, the remaining time of the currently active program.
        """
        if self._model.Status != Status.RUNNING:
            return None

        try:
            return isodate.parse_duration(self._model.pRemainingTime)
        except:
            return None

    @property
    def pElapsedTime(self) -> Optional[isodate.Duration | datetime.timedelta]:
        """
        - None, if the machine is not in the
          RUNNING, PAUSE, END_PROGRAMMED, FAILURE, or PROGRAMME_INTERRUPTED state,
          or if the returned date from the machine is not valid.
        - pElapsedTime, the elapsed time of the currently active program.
        """
        if self._model.Status not in {
            Status.RUNNING,
            Status.PAUSE,
            Status.END_PROGRAMMED,
            Status.FAILURE,
            Status.PROGRAMME_INTERRUPTED,
        }:
            return None

        try:
            return isodate.parse_duration(self._model.pElapsedTime)
        except:
            return None

    @property
    def pSystemTime(self) -> datetime.datetime:
        """
        This property should always be valid.
        """
        return isodate.parse_datetime(self._model.pSystemTime)

    @property
    def pStartTime(self) -> Optional[datetime.datetime]:
        """
        - None, if the machine is not in one of these states:
            - PROGRAMMED_WAITING_TO_START
            - RUNNING
            - PAUSE
            - END_PROGRAMMED
            - FAILURE
            - PROGRAMME_INTERRUPTED
            - RINSE_HOLD
          or if the returned date from the machine is not valid.
        - pStartTime, the start time of the currently active program.
        """

        if self._model.Status not in {
            Status.PROGRAMMED_WAITING_TO_START,
            Status.RUNNING,
            Status.PAUSE,
            Status.END_PROGRAMMED,
            Status.FAILURE,
            Status.PROGRAMME_INTERRUPTED,
            Status.RINSE_HOLD,
        }:
            return None

        try:
            return isodate.parse_datetime(self._model.pStartTime)
        except:
            return None

    @property
    def pEndTime(self) -> Optional[datetime.datetime]:
        """
        - None, if the machine is not in one of these states:
            - RUNNING
            - PAUSE
            - END_PROGRAMMED
            - FAILURE
            - PROGRAMME_INTERRUPTED
          or if the returned date from the machine is not valid.
        - pEndTime, the estimated end time of the currently active program.
        """
        if self._model.Status not in {
            Status.RUNNING,
            Status.PAUSE,
            Status.END_PROGRAMMED,
            Status.FAILURE,
            Status.PROGRAMME_INTERRUPTED,
        }:
            return None

        try:
            return isodate.parse_datetime(self._model.pEndTime)
        except:
            return None

    @property
    def pLastNotificationTime(self) -> Optional[datetime.datetime]:
        """
        - None, if there is no time stamp.
        - pLastNotificationTime, the timestamp of the last received notification.
        """
        stamp = self._model.pLastNotificationTime

        if stamp == "":
            return None

        try:
            return isodate.parse_datetime(stamp)
        except:
            return None

    @property
    def ProcessUID(self) -> str:
        """
        According to the Miele documentation,
        this property should always be valid for devices newer than 01.01.2022.

        The behaviour of older devices is not specified in more detail.
        washpy assumes, that older devices will always return this property,
        albeit with an empty string as the value.
        """
        return self._model.ProcessUID

    @property
    def pExtended(self) -> Dict[str, Any]:
        """
        The contents of this property are device specific.

        Fow PWM 507 machines take a look at the class `pExtendedPWM507`
        """
        return self._model.pExtended


def test_StateModel_parsing():
    # real data, pExtended is a bit truncated
    json_data = {
        "Status": 5,
        "ProgramID": 1,
        "ProgramPhase": 260,
        "SyncState": 2,
        "pRemainingTime": "PT0H26M0S",
        "pElapsedTime": "PT0H34M0S",
        "pSystemTime": "2024-04-24T17:47:01",
        "pStartTime": "2024-04-24T17:13:09",
        "pEndTime": "2024-04-24T18:13:01",
        "pLastNotificationTime": "",
        "ProcessUID": "DC0DF9D0E11308F6182F6B0B9B5C4473A5212271461EB823CF0546A71A5A12F8",
        "pExtended": {
            "DoorOpen": False,
            "DeviceLocked": False,
            "StepName": "",
            "Extras": {
                "Quick": False,
            },
            "AutoDosing": {
                "Container": 0,
                "NoLaundryDetergent": False,
            },
        },
    }

    expected = StateModel(
        Status=Status(5),
        ProgramID=1,
        ProgramPhase=260,
        SyncState=2,
        pRemainingTime="PT0H26M0S",
        pElapsedTime="PT0H34M0S",
        pSystemTime="2024-04-24T17:47:01",
        pStartTime="2024-04-24T17:13:09",
        pEndTime="2024-04-24T18:13:01",
        pLastNotificationTime="",
        ProcessUID="DC0DF9D0E11308F6182F6B0B9B5C4473A5212271461EB823CF0546A71A5A12F8",
        pExtended={
            "DoorOpen": False,
            "DeviceLocked": False,
            "StepName": "",
            "Extras": {
                "Quick": False,
            },
            "AutoDosing": {
                "Container": 0,
                "NoLaundryDetergent": False,
            },
        },
    )

    assert expected == StateModel(**json_data)


def test_State_parsing():
    # real data, pExtended is a bit truncated
    json_data = {
        "Status": 5,
        "ProgramID": 1,
        "ProgramPhase": 260,
        "SyncState": 2,
        "pRemainingTime": "PT0H26M0S",
        "pElapsedTime": "PT0H34M0S",
        "pSystemTime": "2024-04-24T17:47:01",
        "pStartTime": "2024-04-24T17:13:09",
        "pEndTime": "2024-04-24T18:13:01",
        "pLastNotificationTime": "",
        "ProcessUID": "DC0DF9D0E11308F6182F6B0B9B5C4473A5212271461EB823CF0546A71A5A12F8",
        "pExtended": {
            "DoorOpen": False,
            "DeviceLocked": False,
            "StepName": "",
            "Extras": {
                "Quick": False,
            },
            "AutoDosing": {
                "Container": 0,
                "NoLaundryDetergent": False,
            },
        },
    }

    expected = State(
        Status=Status(5),
        ProgramID=1,
        ProgramPhase=260,
        SyncState=2,
        pRemainingTime="PT0H26M0S",
        pElapsedTime="PT0H34M0S",
        pSystemTime="2024-04-24T17:47:01",
        pStartTime="2024-04-24T17:13:09",
        pEndTime="2024-04-24T18:13:01",
        pLastNotificationTime="",
        ProcessUID="DC0DF9D0E11308F6182F6B0B9B5C4473A5212271461EB823CF0546A71A5A12F8",
        pExtended={
            "DoorOpen": False,
            "DeviceLocked": False,
            "StepName": "",
            "Extras": {
                "Quick": False,
            },
            "AutoDosing": {
                "Container": 0,
                "NoLaundryDetergent": False,
            },
        },
    )

    assert expected._model == State(**json_data)._model
