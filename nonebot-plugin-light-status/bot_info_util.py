from nonebot.adapters.onebot.v11 import Bot
from nonebot import logger


async def get_bot_info(bot: Bot):
    adapter_type = str(bot.type)
    bot_id = str(bot.self_id)
    nickname = str((await bot.get_login_info())['nickname'])
    avatar_url = f"http://q1.qlogo.cn/g?b=qq&nk={bot.self_id}&s=640"
    bot_status = (await bot.get_status())['stat']
    message_received, message_sent = bot_status['message_received'], bot_status['message_sent']
    return adapter_type, bot_id, nickname, avatar_url, message_received, message_sent
