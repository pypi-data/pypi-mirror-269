"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..homie import HomieWhen



def when_phue_change(
    when: 'HomieWhen',
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param when: Primary class instance for the conditonal.
    :returns: Boolean indicating whether condition matched.
    """

    params = (
        when.params.phue_change)

    assert params is not None

    device_names = params.devices
    sensor_names = params.sensors
    since = params.since

    devices = (
        when.homie.phue_devices)


    def _append_outcome() -> None:

        assert changed is not False

        items = changed.items()

        for key, value in items:

            if key not in sensor_names:
                continue

            if value is None:
                continue

            _since = value.since

            if _since > since:
                continue

            outcomes.append(True)


    outcomes: list[bool] = []

    for name in device_names:

        device = devices[name]
        device.refresh_source()

        present = device.present
        connect = device.connect
        changed = device.changed

        if not present:
            outcomes.append(False)
            continue

        if not connect:
            outcomes.append(False)
            continue

        if not changed:
            outcomes.append(False)
            continue

        _append_outcome()


    return any(outcomes)



def chck_phue_change(
    when: 'HomieWhen',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param when: Primary class instance for the conditonal.
    """

    params = (
        when.params.phue_change)

    assert params is not None

    devices = (
        when.homie.phue_devices)


    device_names = params.devices

    for name in device_names:
        assert name in devices
