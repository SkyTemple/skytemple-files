#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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

from inspect import currentframe
try:
    import builtins
    _ = builtins._
except Exception:
    _ = lambda a: a


def reload_locale():
    global _
    import builtins
    _ = builtins._
    try:
        from explorerscript import util
        util._ = _
    except ImportError:
        pass
    try:
        from desmume import i18n_util
        i18n_util._ = _
    except ImportError:
        pass


def f(s, additional_locals=None):
    """f-strings as a function, for use with translatable strings: f'{techticks}' == f('{techticks}')"""
    if additional_locals is None:
        additional_locals = {}
    frame = currentframe().f_back
    s1 = s.replace("'", "\\'").replace('\n', '\\n')
    additional_locals.update(frame.f_locals)
    try:
        return eval(f"f'{s1}'", additional_locals, frame.f_globals)
    except SyntaxError as e:
        if "f-string expression part cannot include a backslash" in str(e):
            s1 = s.replace('"', '\\"').replace('\n', '\\n')
            return eval(f'f"{s1}"', additional_locals, frame.f_globals)
