from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Message, Event, Bot, MessageSegment

from .render import render
from .bot_info_util import get_bot_info

light_status = on_command("状态", aliases={"运行状态", "status", "st"})


@light_status.handle()
async def status(
        bot: Bot,
        event: Event):
    bot_info = await get_bot_info(bot)
    render_jpg_path = render(bot_info)
    await light_status.send(Message(MessageSegment.image(f"file://{render_jpg_path}")))