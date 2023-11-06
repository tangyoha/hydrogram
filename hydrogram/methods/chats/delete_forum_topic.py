#  Hydrogram - Telegram MTProto API Client Library for Python
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

from typing import Union

import hydrogram
from hydrogram import raw


class DeleteForumTopic:
    async def delete_forum_topic(
        self: "hydrogram.Client", chat_id: Union[int, str], topic_id: int
    ) -> bool:
        """Delete a forum topic.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            topic_id (``int``):
                Unique identifier (int) of the target forum topic.

        Returns:
            `bool`: On success, a Boolean is returned.

        Example:
            .. code-block:: python

                await app.delete_forum_topic(chat_id, topic_id)
        """
        try:
            await self.invoke(
                raw.functions.channels.DeleteTopicHistory(
                    channel=await self.resolve_peer(chat_id), top_msg_id=topic_id
                )
            )
        except Exception as e:
            print(e)
            return False
        return True
