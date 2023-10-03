# mypy: ignore-errors

from typing import TYPE_CHECKING, Container, Iterable, Tuple, Union

from pylint.checkers import BaseChecker
from pylint.checkers.deprecated import DeprecatedMixin

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DeprecationChecker(DeprecatedMixin, BaseChecker):
    """
    Class implementing deprecation checker.
    """
    name = "deprecated-function-call-st"
    options = ()
    enabled = True
    msgs = {
        **DeprecatedMixin.DEPRECATED_METHOD_MESSAGE,
        **DeprecatedMixin.DEPRECATED_ARGUMENT_MESSAGE,
    }

    def deprecated_decorators(self) -> Iterable:
        """Callback returning the deprecated decorators.

        Returns:
            collections.abc.Container of deprecated decorator names.
        """
        # pylint: disable=no-self-use
        return ()

    def deprecated_methods(self) -> Container[str]:
        """Callback returning the deprecated methods/functions.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """
        # pylint: disable=no-self-use
        return {
            "skytemple_files.common.util.read_uintle",
            "skytemple_files.common.util.read_uintbe",
            "skytemple_files.common.util.read_sintle",
            "skytemple_files.common.util.read_sintbe",
            "skytemple_files.common.util.write_uintle",
            "skytemple_files.common.util.write_uintbe",
            "skytemple_files.common.util.write_sintle",
            "skytemple_files.common.util.write_sintbe",
        }

    def deprecated_arguments(
        self, method: str
    ) -> Iterable[Tuple[Union[int, None], str]]:
        """Callback returning the deprecated arguments of method/function.

        Args:
            method (str): name of function/method checked for deprecated arguments

        Returns:
            collections.abc.Iterable in form:
                ((POSITION1, PARAM1), (POSITION2: PARAM2) ...)
            where
                * POSITIONX - position of deprecated argument PARAMX in function definition.
                  If argument is keyword-only, POSITIONX should be None.
                * PARAMX - name of the deprecated argument.
            E.g. suppose function:

            .. code-block:: python
                def bar(arg1, arg2, arg3, arg4, arg5='spam')

            with deprecated arguments `arg2` and `arg4`. `deprecated_arguments` should return:

            .. code-block:: python
                ((1, 'arg2'), (3, 'arg4'))
        """
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        return ()

    def deprecated_modules(self) -> Iterable:
        """Callback returning the deprecated modules.

        Returns:
            collections.abc.Container of deprecated module names.
        """
        # pylint: disable=no-self-use
        return ()

    def deprecated_classes(self, module: str) -> Iterable:
        """Callback returning the deprecated classes of module.

        Args:
            module (str): name of module checked for deprecated classes

        Returns:
            collections.abc.Container of deprecated class names.
        """
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        return ()


def register(linter: 'PyLinter') -> None:
    linter.register_checker(DeprecationChecker(linter))
