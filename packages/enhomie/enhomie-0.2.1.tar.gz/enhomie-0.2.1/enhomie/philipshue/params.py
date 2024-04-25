"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Literal
from typing import Optional

from pydantic import BaseModel



_SENSORS = Literal[
    'button1',
    'button2',
    'button3',
    'button4',
    'motion1']



class PhueDeviceParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param bridge: Name of bridge where the device belongs.
    :param phid: Unique identifier for device within bridge.
    :param label: Name of the device to find within bridge.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    bridge: str
    phid: Optional[str] = None

    label: Optional[str] = None


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)

        phid = self.phid
        label = self.label

        assert phid or label



class WhenPhueChangeParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param devices: List of devices in scope for conditional.
    :param sensors: List of sensors in scope for conditional.
    :param since: Minimum required time post change occurred.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    devices: list[str]
    sensors: list[Literal[
        'button1',
        'button2',
        'button3',
        'button4',
        'motion1']]

    since: int = 0
