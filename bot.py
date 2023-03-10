import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.command import Command, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from aiogram.utils.markdown import html_decoration as fmt
from aiogram.utils.token import TokenValidationError

from config import CONFIG
from crud import CRUDBots, CRUDChats, CRUDUsers
from keyboards.inline.users.formMain import MyCallback

from polling_manager import PollingManager
from schemas import BotTGSchema, ChatSchema, UserSchema
from loader import dp
from states.users.mainState import UserStates

logger = logging.getLogger(__name__)





async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="add_bot",
            description="add bot, usage '/add_bot 123456789:qwertyuiopasdfgh'",
        ),
        BotCommand(
            command="stop_bot",
            description="stop bot, usage '/stop_bot 123456789'",
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


# async def on_bot_startup(bot: Bot):
#     await set_commands(bot)
#     await bot.send_message(chat_id=ADMIN_ID, text="Bot started!")
#
#
# async def on_bot_shutdown(bot: Bot):
#     await bot.send_message(chat_id=ADMIN_ID, text="Bot shutdown!")


async def stop_bot(
        message: types.Message, command: CommandObject, polling_manager: PollingManager
):
    if command.args:
        try:
            polling_manager.stop_bot_polling(int(command.args))
            await message.answer("Bot stopped")
        except (ValueError, KeyError) as err:
            await message.answer(fmt.quote(f"{type(err).__name__}: {str(err)}"))
    else:
        await message.answer("Please provide bot id")


@dp.message(UserStates.AddWelcomeTxt)
async def add_welcome_txt(message: Message, state: FSMContext) -> None:
    try:
        data = await state.get_data()
        get_bot = await CRUDBots.get(id=int(data["any_bot_id"]))
        get_bot.welcome_text = message.text
        await CRUDBots.update(bot=get_bot)
        await message.answer(text="?????????????????? ?????????? ?????????????? ?????????????? ????\n\n"
                                  f"{message.text}",
                             reply_markup=await MyCallback.main_menu_ikb(user_id=message.from_user.id)
                             )
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer(text="???????????????? ???????????? ?????? ?????????????????? ????????????\n\n"
                                  "???????????????????? ?????? ?????? ???????????????? ????????",
                             reply_markup=await MyCallback.main_menu_ikb(user_id=message.from_user.id)
                             )


@dp.message(UserStates.Newsletters)
async def NewslettersBot_txt(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    txt = message.text
    await state.clear()


@dp.message(content_types=["new_chat_members"])
async def add_chat(message: types.Message):
    if message.new_chat_members[0].is_bot:
        get_bot = await CRUDBots.get(bot_id=message.new_chat_members[0].id)
        get_chat = await CRUDChats.get(bot_id=get_bot.bot_id)
        if get_bot:
            if get_chat:
                get_chat.chat_id = message.chat.id
                await CRUDChats.update(chat=get_chat)
            else:
                await CRUDChats.add(chat=ChatSchema(chat_id=message.chat.id,
                                                    bot_id=int(get_bot.bot_id))
                                    )
                CONFIG.CHAT.append(str(message.chat.id))
        else:
            await message.answer("Please provide bot")


@dp.message(content_types=["left_chat_member"])
async def delete_chat(message: types.Message):
    if message.left_chat_member.is_bot:
        CONFIG.CHAT.append(str(message.chat.id))
        print("asd")


@dp.message(commands=["add_bot"])
async def add_bot(
        message: types.Message,
        command: CommandObject,
        dp_for_new_bot: Dispatcher,
        polling_manager: PollingManager,
):
    bot = Bot.get_current()
    if bot.token == CONFIG.BOT.TOKEN[0]:
        if message.from_user.id in CONFIG.BOT.ADMINS:
            if command.args:
                try:
                    bot = Bot(command.args)
                    my_bot = await CRUDBots.get(bot_token=command.args)
                    if my_bot:
                        await message.answer("?????? ?? ???????? ?????????????? ?????? ????????????????")
                        return
                    else:
                        if bot.id in polling_manager.polling_tasks:
                            await message.answer("?????? ?? ???????? ?????????????? ?????? ????????????????")
                            return
                        await CRUDBots.add(bot=BotTGSchema(user_id=message.from_user.id,
                                                           bot_id=bot.id,
                                                           bot_token=command.args)
                                           )
                        await CRUDChats.add(chat=ChatSchema(bot_id=bot.id,
                                                            chat_id=1)
                                            )
                        CONFIG.BOT.TOKEN.append(command.args)
                        # also propagate dp and polling manager to new bot to allow new bot add bots
                        polling_manager.start_bot_polling(
                            dp=dp_for_new_bot,
                            bot=bot,
                            # on_bot_startup=on_bot_startup(bot),
                            # on_bot_shutdown=on_bot_shutdown(bot),
                            polling_manager=polling_manager,
                            dp_for_new_bot=dp_for_new_bot,
                        )
                        bot_user = await bot.get_me()
                        await message.answer(f"???????????? ???????????? ????????: @{bot_user.username}")
                except (TokenValidationError, TelegramUnauthorizedError) as err:
                    await message.answer(fmt.quote(f"{type(err).__name__}: {str(err)}"))
            else:
                await message.answer("????????????????????, ?????????????? ??????????")
    else:
        await message.answer("??????")


@dp.message(commands=["ban"])
async def ban_user(message: types.Message):
    if message.reply_to_message:
        user = await CRUDUsers.get(user_id=message.from_user.id)
        if user:
            user.ban = True
            await CRUDUsers.update(user=user)
            await message.answer(text="???????????????????????? ??????????????")
        else:
            await message.answer(text="???????????? ???????????????????????? ???? ????????????????????")


@dp.message(commands=["start"])
async def registration_start(message: types.Message):
    bot = Bot.get_current()
    text: str = "?????????? ???????????????????? ?? FeedBack Bot ??? ?????? ?????? ???????????????? ?????????? ?? Telegram"

    if bot.token == CONFIG.BOT.TOKEN[0]:
        if message.from_user.id not in CONFIG.BOT.ADMINS:
            CONFIG.BOT.ADMINS.append(message.from_user.id)

        main_bot = Bot(token=CONFIG.BOT.TOKEN[0])
        await main_bot.send_message(text=text,
                                    chat_id=message.from_user.id,
                                    reply_markup=await MyCallback.main_menu_ikb(user_id=message.from_user.id))
    else:
        get_chat_bot = await CRUDChats.get(bot_id=bot.id)
        if get_chat_bot.chat_id == 1:
            await message.answer(text="???????????? ?????? ???? ???????????????? ???? ?? ???????? ??????")
        else:
            user = await CRUDUsers.get(user_id=message.from_user.id)
            if get_chat_bot is None:
                await message.answer(text="???????????? ?????? ???? ???????????????? ???? ?? ???????? ??????")
            else:
                if user:
                    welcome_txt = await CRUDBots.get(bot_id=bot.id)
                    if welcome_txt.welcome_text == "None":
                        await message.answer(text=text)
                    else:
                        await message.answer(text=welcome_txt.welcome_text)
                else:
                    await CRUDUsers.add(user=UserSchema(user_id=message.from_user.id,
                                                        chat_id=int(get_chat_bot.chat_id),
                                                        use_bot_id=int(bot.id)
                                                        )
                                        )
                    await message.answer(text=text)


@dp.message(content_types="any")
async def echo(message: types.Message):
    bot = Bot.get_current()
    if bot.token != CONFIG.BOT.TOKEN[0]:
        get_bot = await CRUDBots.get(bot_id=bot.id)
        chat = await CRUDChats.get(bot_id=get_bot.bot_id)
        user = await CRUDUsers.get(user_id=message.from_user.id)
        if user:
            if not user.ban:
                if not message.reply_to_message:
                    if user:
                        if user.chat_id == 1:
                            user.chat_id = chat.chat_id
                            await CRUDUsers.update(user=user)

                            current_bot = Bot(token=get_bot.bot_token)
                            await current_bot.forward_message(chat_id=chat.chat_id,
                                                              from_chat_id=message.from_user.id,
                                                              message_id=message.message_id)
                        else:
                            current_bot = Bot(token=get_bot.bot_token)
                            await current_bot.forward_message(chat_id=chat.chat_id,
                                                              from_chat_id=message.from_user.id,
                                                              message_id=message.message_id)
                            CONFIG.COUNTER.USER_MESSAGE += 1
                    else:
                        await message.answer(text="???????????????????????? ???? ??????????????")
                else:
                    get_user_id = await CRUDUsers.get(user_id=message.reply_to_message.forward_from.id)
                    if get_user_id:
                        current_bot = Bot(token=get_bot.bot_token)
                        await current_bot.send_message(chat_id=message.reply_to_message.forward_from.id,
                                                       text=message.text)
                        CONFIG.COUNTER.ADMIN_MESSAGE += 1
                    else:
                        await message.answer(text="???????????????????????? ???? ??????????????")
            else:
                await message.delete()
                await message.answer(text="?????? ?????????????????? ????????????, ???? ???????????????????? ?? ????????!")
        else:
            await message.answer(text="?????????????? ?????? ?????? /start")


async def on_bot_startup(bot: Bot):
    #await set_commands(bot)
    await bot.send_message(chat_id=CONFIG.BOT.ADMINS[0], text="Bot started!")


async def on_bot_shutdown(bot: Bot):
    await bot.send_message(chat_id=CONFIG.BOT.ADMINS[0], text="Bot shutdown!")


async def on_startup(bots: List[Bot]):
    for bot in bots:
        await on_bot_startup(bot)


async def on_shutdown(bots: List[Bot]):
    for bot in bots:
        await on_bot_shutdown(bot)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    from handlers import dp
    polling_manager = PollingManager()
    # dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    # dp.message.register(add_bot, Command(commands="add_bot"))
    # dp.message.register(stop_bot, Command(commands="stop_bot"))
    #
    # dp.include_router(admin_router)
    # dp.include_router(user_router)
    # dp.include_router(admin_router1)

    get_tokens = await CRUDBots.get_all()
    for token in get_tokens:
        CONFIG.BOT.TOKEN.append(token.bot_token)

    bots = [Bot(token) for token in CONFIG.BOT.TOKEN]
    for bot in bots:
        await bot.get_updates(offset=-1)

    await dp.start_polling(*bots, dp_for_new_bot=dp, polling_manager=polling_manager, polling_timeout=1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Exit")
