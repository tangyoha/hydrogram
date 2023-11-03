#  Hydrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2023 Dan <https://github.com/delivrance>
#  Copyright (C) 2023-present Amano LLC <https://amanoteam.com>
#
#  This file is part of Hydrogram.
#
#  Hydrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Hydrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Hydrogram.  If not, see <http://www.gnu.org/licenses/>.

import base64
import logging
import sqlite3
import struct
from typing import Optional

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class MemoryStorage(SQLiteStorage):
    def __init__(self, name: str, session_string: Optional[str] = None):
        super().__init__(name)

        self.session_string = session_string

    async def open(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create()

        if self.session_string:
            # Old format
            if len(self.session_string) in {
                self.SESSION_STRING_SIZE,
                self.SESSION_STRING_SIZE_64,
            }:
                dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                    (
                        self.OLD_SESSION_STRING_FORMAT
                        if len(self.session_string) == self.SESSION_STRING_SIZE
                        else self.OLD_SESSION_STRING_FORMAT_64
                    ),
                    base64.urlsafe_b64decode(
                        self.session_string + "=" * (-len(self.session_string) % 4)
                    ),
                )

                await self.dc_id(dc_id)
                await self.test_mode(test_mode)
                await self.auth_key(auth_key)
                await self.user_id(user_id)
                await self.is_bot(is_bot)
                await self.date(0)

                log.warning(
                    "You are using an old session string format. Use export_session_string to update"
                )
                return

            dc_id, api_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                self.SESSION_STRING_FORMAT,
                base64.urlsafe_b64decode(
                    self.session_string + "=" * (-len(self.session_string) % 4)
                ),
            )

            await self.dc_id(dc_id)
            await self.api_id(api_id)
            await self.test_mode(test_mode)
            await self.auth_key(auth_key)
            await self.user_id(user_id)
            await self.is_bot(is_bot)
            await self.date(0)

    async def delete(self):
        pass
