from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import aiofiles
from nonebot import require

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_cache_file

if TYPE_CHECKING:
    from os import PathLike
    from typing import Union, AsyncIterable, Iterator

    from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent


async def upload_file(bot: Bot, event: Event, filename: str,
                      data: Union[None, bytes, str,
                      AsyncIterable[Union[str, bytes]],
                      Iterator[Union[str, bytes]]] = None,
                      path: Union[None, str, PathLike[str]] = None):
    if path is None:
        cache_file = get_cache_file(plugin_name="ssttkkl_nonebot_utils",
                                    filename=str(uuid.uuid4()))
        async with aiofiles.open(cache_file, "wb+") as buf:
            await buf.write(data)

        path = cache_file

    if isinstance(event, PrivateMessageEvent):
        bot.upload_private_file(user_id=event.user_id, file=path, name=filename)
    elif isinstance(event, GroupMessageEvent):
        bot.upload_group_file(group_id=event.group_id, file=path, name=filename)


__all__ = ("upload_file",)
