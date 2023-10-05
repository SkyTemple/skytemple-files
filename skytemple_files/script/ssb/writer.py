"""Converts Ssb models back into the binary format used by the game"""
#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

import logging
import math

from range_typed_integers import u16_checked, u16

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_JP,
    GAME_REGION_US,
    Pmd2Data,
)
from skytemple_files.common.util import (
    write_u16,
)
from skytemple_files.script.ssb.header import (
    SSB_HEADER_EU_LENGTH,
    SSB_HEADER_JP_LENGTH,
    SSB_HEADER_US_LENGTH,
    AbstractSsbHeader,
    SsbHeaderEu,
    SsbHeaderJp,
    SsbHeaderUs,
)
from skytemple_files.script.ssb.model import SSB_PADDING_BEFORE_ROUTINE_INFO, Ssb

logger = logging.getLogger(__name__)


class SsbWriter:
    """
    Writes a SSB model to a binary stream for saving in ROM.
    Also updates the original_binary_data field of the model.
    """

    def __init__(self, model: Ssb, static_data: Pmd2Data):
        self.model = model
        self.bytes_written = 0
        self.static_data = static_data
        self._string_codec = static_data.string_encoding

    def write(self) -> bytes:
        """
        model.routine_info = built_routine_info_with_offset
        model.routine_ops = built_routine_ops
        model.constants = built_constants
        model.strings = built_strings
        """

        logger.debug("Serializing SSB model...")

        header_cls: type[AbstractSsbHeader]
        if self.static_data.game_region == GAME_REGION_US:
            header_cls = SsbHeaderUs
            header_len = SSB_HEADER_US_LENGTH
        elif self.static_data.game_region == GAME_REGION_EU:
            header_cls = SsbHeaderEu
            header_len = SSB_HEADER_EU_LENGTH
        elif self.static_data.game_region == GAME_REGION_JP:
            header_cls = SsbHeaderJp
            header_len = SSB_HEADER_JP_LENGTH
        else:
            raise ValueError(f"Unsupported game region {self.static_data.game_region}")

        # STRUCTURE:
        # 0x-- Header
        # 0x00 Routine Info
        #      Routines
        #      Const String Table
        #      Const Strings
        #      <Padding if not even>
        #      {for each lang:}
        #      - Language String Table
        #      - Language Strings
        #      - <Padding if not even>

        # Length header + (6 for each routine) + 2KB buffer - TODO: Calculate properly.
        data = bytearray(header_len + 6 * len(self.model.routine_info) + 2048)
        self.bytes_written += header_len  # We write the header at the very end!

        # 4 bytes of padding, written at the end
        self.bytes_written += SSB_PADDING_BEFORE_ROUTINE_INFO

        if len(self.model.strings) == 0:
            # Init empty string list
            self.model.strings = {
                lang_name: [] for lang_name in header_cls.supported_langs()
            }
        number_of_strings = 0
        if len(self.model.strings.keys()) > 0:
            number_of_strings = len(
                self.model.strings[next(iter(self.model.strings.keys()))]
            )

        # Routine Info - The offsets used for the routine starts MUST already be correctly calculated!
        for offset, routine_info in self.model.routine_info:
            write_u16(data, u16(offset // 2), self.bytes_written)
            write_u16(data, routine_info.type.value, self.bytes_written + 2)
            write_u16(data, routine_info.linked_to, self.bytes_written + 4)
            self.bytes_written += 6

        # Routines - The offsets used for the routine starts MUST already be correctly calculated!
        op_codes = self.static_data.script_data.op_codes__by_id
        for i, ops in enumerate(self.model.routine_ops):
            for op in ops:
                self.write_u16(data, op.op_code.id, self.bytes_written)
                self.bytes_written += 2
                if (
                    self.static_data.script_data.op_codes__by_id[op.op_code.id].params
                    == -1
                ):
                    # Dynamic argument handling: Write number of arguments next
                    self.write_u16(
                        data, u16_checked(len(op.params)), self.bytes_written
                    )
                    self.bytes_written += 2
                for argidx, param in enumerate(op.params):
                    # If negative, store as 14-bit or 16-bit signed integer.
                    if param < 0:
                        # TODO: Support for repeating args
                        args = op_codes[op.op_code.id].arguments__by_id
                        if argidx in args and args[argidx].type == "sint16":
                            param = 0x10000 + param
                        else:
                            param = 0x8000 + param
                    self.write_u16(data, u16_checked(param), self.bytes_written)
                    self.bytes_written += 2

        # Const String Table and Constants
        start_of_const_table = self.bytes_written
        len_of_const_table = 2 * len(self.model.constants)
        const_table_bytes_written = 0
        const_string_bytes_written = 0
        for constant in self.model.constants:
            abs_pos_of_string = (
                start_of_const_table + len_of_const_table + const_string_bytes_written
            )
            written_pos_of_string = (
                const_string_bytes_written + len_of_const_table + number_of_strings * 2
            )

            self.write_u16(
                data,
                u16_checked(written_pos_of_string),
                start_of_const_table + const_table_bytes_written,
            )
            const_table_bytes_written += 2

            string_len = self._write_string(data, constant, abs_pos_of_string)
            const_string_bytes_written += string_len

        self.bytes_written += const_string_bytes_written + const_table_bytes_written
        if self.bytes_written % 2 != 0:
            self.bytes_written += 1

        # Language String Tables and Language Strings
        len_of_string_tables = 2 * number_of_strings
        previous_languages_block_sizes = 0
        string_lengths: dict[str, int] = {}
        if (
            number_of_strings != 0
            and len({len(i) for i in self.model.strings.values()}) != 1
        ):
            raise ValueError(
                _(
                    "Could not compile script: All languages must have the same amount of strings."
                )
            )
        for lang in header_cls.supported_langs():
            start_of_string_table = self.bytes_written
            string_table_bytes_written = 0
            string_bytes_written = 0
            for string in self.model.strings[lang]:
                abs_pos_of_string = (
                    start_of_string_table + len_of_string_tables + string_bytes_written
                )
                written_pos_of_string = (
                    abs_pos_of_string
                    - start_of_const_table
                    - previous_languages_block_sizes
                )

                self.write_u16(
                    data,
                    u16_checked(written_pos_of_string),
                    start_of_string_table + string_table_bytes_written,
                )
                string_table_bytes_written += 2

                string_len = self._write_string(data, string, abs_pos_of_string)
                string_bytes_written += string_len

            self.bytes_written += string_bytes_written + string_table_bytes_written

            if self.bytes_written % 2 != 0:
                self.bytes_written += 1

            string_lengths[lang] = self.bytes_written - start_of_string_table
            previous_languages_block_sizes += string_lengths[lang]

        # Header
        if header_cls == SsbHeaderUs:
            # Number of constants
            write_u16(data, u16_checked(len(self.model.constants)), 0x00)
            # Number of Strings
            write_u16(data, u16_checked(number_of_strings), 0x02)
            # Constant Strings Start
            write_u16(
                data,
                u16_checked(
                    (start_of_const_table - header_len + len_of_const_table) // 2
                ),
                0x04,
            )
            # Const length
            write_u16(
                data, u16_checked(math.ceil(const_string_bytes_written / 2)), 0x06
            )
            # String length
            assert len(string_lengths) == 1
            for length in string_lengths.values():
                write_u16(data, u16(length // 2), 0x08)
            # Unknown - TODO: what is the value here actually?
            write_u16(data, u16(0), 0x0A)
        elif header_cls == SsbHeaderEu:
            # Number of constants
            write_u16(data, u16_checked(len(self.model.constants)), 0x00)
            # Number of Strings
            write_u16(data, u16_checked(number_of_strings), 0x02)
            # Constant Strings Start
            write_u16(
                data,
                u16_checked(
                    (start_of_const_table - header_len + len_of_const_table) // 2
                ),
                0x04,
            )
            # Const length
            write_u16(
                data, u16_checked(math.ceil(const_string_bytes_written / 2)), 0x06
            )
            assert len(string_lengths) == 5
            for i, length in enumerate(string_lengths.values()):
                write_u16(data, u16_checked(length // 2), 0x08 + (2 * i))
        elif header_cls == SsbHeaderJp:
            # Number of constants
            write_u16(data, u16_checked(len(self.model.constants)), 0x00)
            # Unknown. TODO: Might want to check this.
            write_u16(data, u16(0), 0x02)
            # Constant Strings Start
            write_u16(
                data,
                u16((start_of_const_table - header_len + len_of_const_table) // 2),
                0x04,
            )
            # Const length
            write_u16(
                data, u16_checked(math.ceil(const_string_bytes_written / 2)), 0x06
            )
            # Unknown. TODO: Might want to check this.
            write_u16(data, u16(0), 0x08)
            # Unknown. TODO: Might want to check this.
            write_u16(data, u16(0), 0x0A)

        # Important metadata
        write_u16(
            data, u16_checked((start_of_const_table - header_len) // 2), header_len
        )
        write_u16(data, u16_checked(len(self.model.routine_info)), header_len + 2)

        assert self.bytes_written % 2 == 0
        if len(data) < self.bytes_written:
            bytes_needed = self.bytes_written - len(data)
            data += bytes(bytes_needed)
        return data[: self.bytes_written]

    def write_u16(self, data: bytearray, to_write: u16, start=0):
        """
        Special version of write_uintle that enlarges the buffer before writing, if needed.
        TODO: Calculate the entire size of the buffer before.
        """
        if len(data) < start + 2:
            bytes_needed = start + 2 - len(data)
            data += bytes(bytes_needed)
        write_u16(data, to_write, start)

    def _write_string(self, data: bytearray, to_write: str, start=0):
        b = bytes(to_write, self._string_codec) + bytes([0])
        length = len(b)
        if len(data) < start + length:
            bytes_needed = start + length - len(data)
            data += bytes(bytes_needed)
        data[start : start + length] = b
        return length
