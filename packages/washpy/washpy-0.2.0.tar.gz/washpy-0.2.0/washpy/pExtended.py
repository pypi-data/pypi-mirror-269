from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class pExtendedPWM507(BaseModel):
    """
    This is my best effort attempt at capturing the pExtended field in a python struct,
    tailored to the PWM 507 machine.

    Some of these fields are completely missing from the official Miele documentation,
    some are spelled a little differently, some have a slightly different type.
    """

    DoorOpen: bool
    DeviceLocked: bool
    SpinningSpeed: Optional[int]
    TargetSpinningSpeed: int
    CurrentSpinningSpeed: int
    SISetTemperature: List[int]
    SIBlockTargetTemperature: int
    WaitingForPayment: bool
    pProgramphase: int
    Extras: Dict[str, bool]
    AutoDosing: Optional[Dict[str, Any]]
    ProgramID: Optional[int]
    ProgramName: Optional[str]
    StepID: Optional[int]
    StepName: Optional[str]
    CurrentLoadWeight: int
    SINominalLoad: int
    SISetLoad: int
    SICurrentLoad: int

    # undocumented
    SICurrentTemperature: List[int]
    # undocumented
    BlockID: int
    # undocumented
    BlockName: str

    # deprecated
    Temperature: List[int]
    # deprecated
    TargetTemperature: List[int]
    # deprecated
    CurrentTemperature: List[int]


def test_pExtendedPWM507_parsing():
    # real data, captured in the wild
    json_data = {
        "DoorOpen": False,
        "DeviceLocked": False,
        "Temperature": [-32768, -32768, -32768],
        "TargetTemperature": [4000, -32768, -32768],
        "CurrentTemperature": [1600, -32768, -32768],
        "WaitingForPayment": False,
        "pProgramphase": 12007,
        "SpinningSpeed": 1600,
        "TargetSpinningSpeed": 1600,
        "CurrentSpinningSpeed": 0,
        "CurrentLoadWeight": 0,
        "SINominalLoad": -2147483648,
        "SISetLoad": -2147483648,
        "SICurrentLoad": -2147483648,
        "SICurrentTemperature": [-32768, -32768, -32768],
        "SISetTemperature": [4000, -32768, -32768],
        "SIBlockTargetTemperature": -32768,
        "ProgramID": 0,
        "ProgramName": "",
        "BlockID": 0,
        "BlockName": "",
        "StepID": 0,
        "StepName": "",
        "Extras": {
            "Quick": False,
            "Single": False,
            "WaterPlus": False,
            "RinsingPlus": False,
            "PreWash": False,
            "Soak": False,
            "RinseHold": False,
            "ExtraQuiet": False,
            "SteamSmoothing": False,
            "PreRinse": False,
            "Microfibre": False,
            "Gentle": False,
            "AllergoWash": False,
            "Eco": False,
            "Intensive": False,
            "StarchHold": False,
            "ProgramLocked": False,
            "HygienePlus": False,
        },
        "AutoDosing": {
            "Container": 0,
            "NoLaundryDetergent": False,
            "NoFabricConditioner": False,
            "NoAdditive": False,
        },
    }

    expected = pExtendedPWM507(
        DoorOpen=False,
        DeviceLocked=False,
        Temperature=[-32768, -32768, -32768],
        TargetTemperature=[4000, -32768, -32768],
        CurrentTemperature=[1600, -32768, -32768],
        WaitingForPayment=False,
        pProgramphase=12007,
        SpinningSpeed=1600,
        TargetSpinningSpeed=1600,
        CurrentSpinningSpeed=0,
        CurrentLoadWeight=0,
        SINominalLoad=-2147483648,
        SISetLoad=-2147483648,
        SICurrentLoad=-2147483648,
        SICurrentTemperature=[-32768, -32768, -32768],
        SISetTemperature=[4000, -32768, -32768],
        SIBlockTargetTemperature=-32768,
        ProgramID=0,
        ProgramName="",
        BlockID=0,
        BlockName="",
        StepID=0,
        StepName="",
        Extras={
            "Quick": False,
            "Single": False,
            "WaterPlus": False,
            "RinsingPlus": False,
            "PreWash": False,
            "Soak": False,
            "RinseHold": False,
            "ExtraQuiet": False,
            "SteamSmoothing": False,
            "PreRinse": False,
            "Microfibre": False,
            "Gentle": False,
            "AllergoWash": False,
            "Eco": False,
            "Intensive": False,
            "StarchHold": False,
            "ProgramLocked": False,
            "HygienePlus": False,
        },
        AutoDosing={
            "Container": 0,
            "NoLaundryDetergent": False,
            "NoFabricConditioner": False,
            "NoAdditive": False,
        },
    )

    assert expected == pExtendedPWM507(**json_data)
