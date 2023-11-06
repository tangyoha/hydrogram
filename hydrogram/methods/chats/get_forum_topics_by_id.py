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

import logging
from typing import Iterable, List, Union

import hydrogram
from hydrogram import raw, types

log = logging.getLogger(__name__)


class GetForumTopicsByID:
    async def get_forum_topics_by_id(
        self: "hydrogram.Client", chat_id: Union[int, str], topic_ids: Union[int, Iterable[int]]
    ) -> Union["types.ForumTopic", List["types.ForumTopic"]]:
        """Get one or more topic from a chat by using topic identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            topic_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single topic identifier or an iterable of topic ids (as integers) to get the information of the
                topic themselves.

        Returns:
            :obj:`~hydrogram.types.ForumTopic` | List of :obj:`~hydrogram.types.ForumTopic`: In case *topic_ids* was not
            a list, a single topic is returned, otherwise a list of topics is returned.

        Example:
            .. code-block:: python

                # Get one topic
                await app.get_forum_topics_by_id(chat_id, 12345)

                # Get more than one topic (list of topics)
                await app.get_forum_topics_by_id(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """
        ids, ids_type = (topic_ids, int) if topic_ids else (None, None)

        if ids is None:
            raise ValueError("No argument supplied. Either pass topic_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = list(ids)

        rpc = raw.functions.channels.GetForumTopicsByID(channel=peer, topics=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            topic_list = [types.ForumTopic._parse(topic) for topic in r.topics]
            topics = types.List(topic_list)
        else:
            topics = types.ForumTopic._parse(r.topics[0])

        return topics
