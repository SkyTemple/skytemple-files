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
import gettext
from abc import ABC, abstractmethod
from inspect import currentframe


class AbstractLocaleManager(ABC):
    @abstractmethod
    def translate(self, message, locale_code):
        pass

    @abstractmethod
    def gettext(self, message):
        pass


class LocaleManager(AbstractLocaleManager):
    def __init__(self, domain, localedir, main_languages):
        self.domain = domain
        self.localedir = localedir
        self.main_languages = main_languages

        self.main_translations = gettext.translation(domain, localedir=localedir, languages=main_languages)

    def translate(self, message, locale_code):
        try:
            return gettext.translation(self.domain, localedir=self.localedir, languages=[locale_code]).gettext(message)
        except Exception:
            return message

    def gettext(self, message):
        return self.main_translations.gettext(message)


class NullLocaleManager(AbstractLocaleManager):
    def translate(self, message, locale_code):
        return message

    def gettext(self, message):
        return message


_locales: AbstractLocaleManager = NullLocaleManager()


def _(s):
    """
    This proxy function calls the translation function (if available).
    We use a proxy, so when imported before the localization is ready, we can ensure
    the reload()'ed function is actually called.
    """
    return _locales.gettext(s)


def get_locales():
    return _locales


def reload_locale(domain, localedir, main_languages):
    global _locales
    _locales = LocaleManager(domain, localedir, main_languages)
    _locales.main_translations.install()
    global __
    import builtins
    try:
        from explorerscript import util
        util._ = builtins._
    except ImportError:
        pass
    try:
        from desmume import i18n_util
        i18n_util._ = builtins._
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
