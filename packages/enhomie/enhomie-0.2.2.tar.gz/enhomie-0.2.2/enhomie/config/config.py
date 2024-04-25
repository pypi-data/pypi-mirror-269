"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from typing import Optional

from encommon.config import Config as _Config
from encommon.types import merge_dicts
from encommon.utils.common import PATHABLE

from .params import Params



class Config(_Config):
    """
    Contain the configurations from the arguments and files.

    :param files: Complete or relative path to config files.
    """


    def __init__(
        self,
        files: Optional[PATHABLE] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(
            files=files,
            model=Params)


    @property
    def params(
        self,
    ) -> Params:
        """
        Return the Pydantic model containing the configuration.

        .. warning::
           This method completely overrides the parent but is
           based on that code, would be unfortunate if upstream
           changes meant this breaks or breaks something else.

        :returns: Pydantic model containing the configuration.
        """

        params = self.__params

        if isinstance(params, Params):
            return params


        merged = self.files.merged

        merge_dicts(
            dict1=merged,
            dict2=self.cargs,
            force=True)


        update_params = False

        with suppress(AttributeError):

            _merged = self.paths.merged

            for _merge in _merged.values():

                merge_dicts(
                    dict1=merged,
                    dict2=_merge,
                    force=False)

            update_params = True


        params = self.model(**merged)


        if update_params is True:
            self.__params = params

        assert isinstance(params, Params)

        return params
