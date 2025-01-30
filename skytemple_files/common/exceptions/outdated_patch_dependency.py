from skytemple_files.common.i18n_util import _


class OutdatedPatchDependencyError(Exception):
    """
    Raised when trying to apply an ASM patch that depends on another patches that exist but are outdated
    """

    def __init__(self, patch_name: str, outdated_dependencies: list[str]):
        """
        Creates a new OutdatedPatchDependencyError
        :param patch_name: Name of the patch that failed to apply due to outdated dependencies
        :param outdated_dependencies: List containing the names of each outdated dependency
        """
        self.patch_name = patch_name
        self.outdated_dependencies = outdated_dependencies

    def __str__(self):
        msg = _(
            f"The patch {self.patch_name} cannot be applied because the following patches it depends on are outdated:"
        )
        for dependency in self.outdated_dependencies:
            msg += f"\n- {dependency}"
        msg += _("\nPlease reapply these patches first.")

        return msg
