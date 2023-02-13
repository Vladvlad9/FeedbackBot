from aiogram import Router
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud import CRUDBots
import requests
router = Router()


class MyCallback(CallbackData, prefix="main"):
    main: str
    id: int
    editId: str

    @staticmethod
    async def back_main_menu_ikb(target: str, bot_id: int = 0) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="◀️ Назад",
                                         callback_data=MyCallback(main=target,
                                                                  id=bot_id,
                                                                  editId=""
                                                                  ).pack()
                                         )
                ]
            ]
        )

    @staticmethod
    async def main_menu_ikb(user_id: int) -> InlineKeyboardMarkup:
        data_main_menu = {
            "👨‍💻 Добавить бот": {"main": "AddBot", "id": user_id},
            "📈 Статистика": {"main": "Statistics", "id": user_id},
            "🤖 Мои боты": {"main": "MyBots", "id": user_id},
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=str(name_menu),
                                         callback_data=MyCallback(main=target_menu['main'],
                                                                  id=target_menu['id'],
                                                                  editId=""
                                                                  ).pack()
                                         )
                ] for name_menu, target_menu in data_main_menu.items()
            ]
        )

    @staticmethod
    async def my_bots_ikb(user_id: int) -> InlineKeyboardMarkup:
        my_bots = await CRUDBots.get_all(user_id=user_id)
        get_bot = []
        name_bot = {}
        for bot in my_bots:
            if bot.bot_token != "None":
                get_bot.append(bot)

          # https://t.me/+r-qGqZ7b1DBmN2Yy
        for bots in get_bot:
            data_bot = requests.get(f"https://api.telegram.org/bot{str(bots.bot_token)}/getMe")
            get_data_bot = data_bot.json()
            name_bot[get_data_bot['result']['username']] = {"bot_id": f"{bots.id}"}

        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=name_menu,
                                                         callback_data=MyCallback(main="ShowBot",
                                                                                  id=bot_items['bot_id'],
                                                                                  editId=str(name_menu)).pack())
                                ] for name_menu, bot_items in name_bot.items()
                            ] +
                            [
                                [
                                    InlineKeyboardButton(text="◀️ Назад", callback_data=MyCallback(main="BackMainMenu",
                                                                                                   id=user_id,
                                                                                                   editId="").pack())
                                ]
                            ]
        )

    @staticmethod
    async def settings_current_bot(bot_id: int) -> InlineKeyboardMarkup:
        # data_main_menu = {
        #     "Заблокировать пользователя": {"main": "AddBot", "id": bot_id, "editId": ""},
        #     "📅 Рассылка": {"main": "Statistics", "id": bot_id, "editId": ""},
        #     "📈 Статистика": {"main": "MyBots", "id": bot_id, "editId": ""},
        # }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="☠️ Заблокировать пользователя",
                                         callback_data=MyCallback(main="BlockedUser",
                                                                  id=bot_id,
                                                                  editId="").pack())
                ],
                [
                    InlineKeyboardButton(text="📅 Рассылка",
                                         callback_data=MyCallback(main="NewslettersBot",
                                                                  id=bot_id,
                                                                  editId="").pack()),
                    InlineKeyboardButton(text="📈 Статистика",
                                         callback_data=MyCallback(main="StatisticsBot",
                                                                  id=bot_id,
                                                                  editId="").pack())
                ],
                [
                    InlineKeyboardButton(text="💬 Добавить Чат",
                                         callback_data=MyCallback(main="AddChat",
                                                                  id=bot_id,
                                                                  editId="").pack())
                ],
                [
                    InlineKeyboardButton(text="◀️ Назад",
                                         callback_data=MyCallback(main="MyBots",
                                                                  id=0,
                                                                  editId=""
                                                                  ).pack()
                                         )
                ]
            ]
        )



