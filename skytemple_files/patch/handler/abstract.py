#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Union

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.errors import PatchNotConfiguredError


class AbstractPatchHandler(ABC):
    """A handler for applying a ROM patch to PMD EoS."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name for this patch. It must be the same as in the ppmdu configuration file."""

    @property
    @abstractmethod
    def description(self) -> str:
        """A description text for your patch."""

    @property
    @abstractmethod
    def author(self) -> str:
        """The author of the patch."""

    @property
    @abstractmethod
    def version(self) -> str:
        """
        The version for this patch as a string. Only used for displaying it to the user,
        but may be used by the handler to update the patch.
        Must follow Python package version conventions.
        """

    @property
    def category(self) -> PatchCategory:
        """
        The category describing the purpose of this patch.
        """
        return PatchCategory.OTHER

    @abstractmethod
    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        """
        Returns True, if the patch is applied, False otherwise.
        Raises NotImplementedError if ROM not supported.
        """

    @abstractmethod
    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        """
        Apply the patch. The apply parameter is a callable which applies the actual patch files using ARMIPS,
        as specified in the configuration file.
        The ``apply`` callable might raise a RuntimeError, if the patch was not applied successfully.
        It raises a ArmipsNotInstalledError when armips is not installed.
        The configuration (``config``) may be invalid (no longer up to date) after calling ``apply``.

        :param apply: Applies the ROM patch
        :param rom: Nintendo DS ROM that is being patched.
        :param config: ppmdu configuration for the ROM to be patched.

        :raises RuntimeError: On error applying the patch. If this is raised, the ROM will not be modified.
        :raises ValueError: On error applying the patch. If this is raised, the ROM will not be modified.
        """

    @abstractmethod
    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        """
        TODO: Not supported yet. For future implementation.
        See apply method for info on how it will work.
        May raise NotImplementedError, if not supported.
        """

    def get_parameter(self, name: str) -> Union[int, str]:
        """
        Returns the given configuration parameter. Make sure it is defined.
        :param name: name of the parameter
        """
        try:
            if name in self.__parameters:
                return self.__parameters[name]
            raise PatchNotConfiguredError("No configuration provided.", name, "No configuration provided.")
        except AttributeError:
            raise PatchNotConfiguredError("No configuration provided.", "*", "No configuration provided.")

    def get_parameters(self) -> Dict[str, Union[int, str]]:
        """
        Returns all given configuration parameters or an empty dict of nothing was given.
        """
        try:
            return self.__parameters
        except AttributeError:
            return dict()

    # noinspection PyAttributeOutsideInit
    def supply_parameters(self, parameters: Dict[str, Union[int, str]]):
        """Only to be called by the patch handler: Sets the configuration parameters."""
        self.__parameters = parameters


class DependantPatch(ABC):
    """Extra interface to be implemented by patches that require other patches to be applied first."""

    @abstractmethod
    def depends_on(self) -> List[str]:
        """
        A list of patches (names) that need to be applied before this patch can be applied.
        """
