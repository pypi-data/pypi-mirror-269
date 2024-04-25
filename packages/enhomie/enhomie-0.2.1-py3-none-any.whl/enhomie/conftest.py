"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from pathlib import Path
from typing import Any

from encommon.times import Duration
from encommon.times import Times
from encommon.utils import read_text
from encommon.utils import save_text

from pytest import fixture

from requests_mock import Mocker

from .config import Config
from .homie import Homie
from .homie.test import (
    SAMPLES as CORE_SAMPLES)
from .philipshue.test import (
    SAMPLES as PHUE_SAMPLES)
from .ubiquiti.test import (
    SAMPLES as UBIQ_SAMPLES)



_ANCHOR = Times('-0s@s')

REPLACES = {


    '__STAMP_SMP__': (
        _ANCHOR.shift('-1h').simple),

    '__STAMP_SUB__': (
        _ANCHOR.shift('-1h').subsec),

    '__DURATION__': (
        str(Duration(
            Times(0).since,
            groups=2))),


    '__FSEEN_CUR__': (
        str(int(_ANCHOR.shift('-9d')))),

    '__LSEEN_CUR__': (
        str(int(_ANCHOR.shift('-1d')))),

    '__FSEEN_OLD__': (
        str(int(_ANCHOR.shift('-9d')))),

    '__LSEEN_OLD__': (
        str(int(_ANCHOR.shift('-1d')))),


    '__ASSOC_TIME__': (
        str(int(_ANCHOR.shift('-2d')))),


    '__DISCO_CUR__': (
        str(int(_ANCHOR.shift('-3h')))),

    '__DISCO_OLD__': (
        str(int(_ANCHOR.shift('-1d')))),


    '__START_DAY__': (
        _ANCHOR.shift('-0d@d').simple),

    '__STOP_DAY__': (
        _ANCHOR.shift('+1d@d').simple)}



def config_factory(
    tmp_path: Path,
) -> Config:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    save_text(
        f'{tmp_path}/config.yml',
        content=(
            "cache: ':memory:'\n"
            'enconfig:\n'
            '  paths:\n'
            f'    - {tmp_path}\n'
            f'    - {CORE_SAMPLES}\n'
            f'    - {PHUE_SAMPLES}\n'
            f'    - {UBIQ_SAMPLES}\n'
            'enlogger:\n'
            '  stdo_level: info\n'))

    return Config(
        f'{tmp_path}/config.yml')



@fixture
def config(
    tmp_path: Path,
) -> Config:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    return config_factory(tmp_path)



def homie_factory(  # noqa: CFQ001
    config: 'Config',
) -> Homie:
    """
    Construct the instance for use in the downstream tests.

    .. note::
       Function has slowly evolved and grown over time, but
       should be refactored and simplified in the future.

    :param config: Primary class instance for configuration.
    :returns: Newly constructed instance of related class.
    """

    homie = Homie(config)

    bridges = homie.phue_bridges
    routers = homie.ubiq_routers


    phue_paths = [
        ('https://192.168.1.10'
         '/clip/v2/resource'),
        ('https://192.168.2.10'
         '/clip/v2/resource')]

    phue_files = [
        f'{PHUE_SAMPLES}/jupiter.json',
        f'{PHUE_SAMPLES}/neptune.json']


    ubiq_paths = [

        ('https://192.168.1.1'
         '/api/auth/login'),
        ('https://192.168.1.1'
         '/proxy/network'
         '/api/s/default/rest/user'),
        ('https://192.168.1.1'
         '/proxy/network'
         '/api/s/default/stat/sta'),

        ('https://192.168.2.1'
         '/api/auth/login'),
        ('https://192.168.2.1'
         '/proxy/network'
         '/api/s/default/rest/user'),
        ('https://192.168.2.1'
         '/proxy/network'
         '/api/s/default/stat/sta')]

    ubiq_files = [

        (f'{UBIQ_SAMPLES}/jupiter'
         '/historic.json'),
        (f'{UBIQ_SAMPLES}/jupiter'
         '/realtime.json'),

        (f'{UBIQ_SAMPLES}/neptune'
         '/historic.json'),
        (f'{UBIQ_SAMPLES}/neptune'
         '/realtime.json')]


    def _replaces(
        path: str,
    ) -> dict[str, Any]:

        content = read_text(path)

        items = REPLACES.items()

        for key, new in items:

            content = (
                content
                .replace(key, new))

        loaded = loads(content)

        assert isinstance(loaded, dict)

        return loaded


    with Mocker() as mocker:


        dumped = _replaces(phue_files[0])

        mocker.get(
            url=phue_paths[0],
            json=dumped)


        dumped = _replaces(phue_files[1])

        mocker.get(
            url=phue_paths[1],
            json=dumped)


        for bridge in bridges.values():
            assert bridge.fetched


        mocker.post(ubiq_paths[0])


        dumped = _replaces(ubiq_files[0])

        mocker.register_uri(
            method='get',
            url=ubiq_paths[1],
            response_list=[
                {'json': dumped,
                 'status_code': 401},
                {'json': dumped}])


        dumped = _replaces(ubiq_files[1])

        mocker.get(
            url=ubiq_paths[2],
            json=dumped)


        mocker.post(ubiq_paths[3])


        dumped = _replaces(ubiq_files[2])

        mocker.register_uri(
            method='get',
            url=ubiq_paths[4],
            response_list=[
                {'json': dumped,
                 'status_code': 401},
                {'json': dumped}])


        dumped = _replaces(ubiq_files[3])

        mocker.get(
            url=ubiq_paths[5],
            json=dumped)


        for router in routers.values():
            assert router.fetched


    return homie



@fixture
def homie(
    config: 'Config',
) -> Homie:
    """
    Construct the instance for use in the downstream tests.

    :param config: Primary class instance for configuration.
    :returns: Newly constructed instance of related class.
    """

    return homie_factory(config)
