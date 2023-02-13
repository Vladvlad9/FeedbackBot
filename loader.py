from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import SimpleEventIsolation, MemoryStorage

from config import CONFIG

# bot = Bot(
#         token=CONFIG.BOT.TOKEN[0],
#         parse_mode=ParseMode.HTML
#     )
#
# storage = MemoryStorage()
#
# dp = Dispatcher(
#     bot=bot,
#     storage=storage
# )
dp = Dispatcher(events_isolation=SimpleEventIsolation())


# storage = MemoryStorage()
#
# curDP = Dispatcher(events_isolation=SimpleEventIsolation())

# async def tesbot():
#     bots = [Bot(token) for token in CONFIG.BOT.TOKEN[0]]
#     for bot in bots:
#         await bot.get_updates(offset=-1)
#     return bots
