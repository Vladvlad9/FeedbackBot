from aiogram import F, types, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from config import CONFIG
from crud import CRUDUsers, CRUDBots, CRUDChats
from keyboards.inline.users.formMain import MyCallback
from loader import dp
from states.users.mainState import UserStates


@dp.callback_query(MyCallback.filter())
async def main_forms(callback: types.CallbackQuery, callback_data: MyCallback, state: FSMContext):
    if callback_data.main == "AddBot":
        text = "Чтобы подключить бот, вам нужно выполнить два действия:\n\n" \
               "1. Перейдите в @BotFather и создайте новый бот\n" \
               "2. После создания бота вы получите токен (12345:6789ABCDEF) — скопируйте и напишите в этот чат" \
               "/add_bot (Ваш токен)\n\n" \
               "Важно: не подключайте боты, которые уже используются другими сервисами " \
               "(Controller Bot, разные CRM и т.д.)"
        await callback.message.edit_text(text=text,
                                         reply_markup=await MyCallback.back_main_menu_ikb(target="BackMainMenu"))

    elif callback_data.main == "Statistics":
        get_all_user = await CRUDUsers.get_all()
        get_blocked_bot = await CRUDUsers.get_all(block=True)
        get_ban_bot = await CRUDUsers.get_all(ban=True)
        count_message_user = CONFIG.COUNTER.USER_MESSAGE
        count_message_admin = CONFIG.COUNTER.ADMIN_MESSAGE

        text = "📈 Статистика бота\n\n" \
               f"📤 Количество сообщений отправлено пользователем : {count_message_user}\n" \
               f"📥 Количество сообщений отвечено пользователям : {count_message_admin}\n\n" \
               f"❗️ Количество человек в боте : {len(get_all_user)}\n" \
               f"🚫 Количество забаненых в чате : {len(get_ban_bot)}\n" \
               f"☠️ Количество человек которые удалили/остановили бота : {len(get_blocked_bot)}\n\n" \
               f"<i>Счетчик тех, кто заблокировал бот, обновляется после каждой рассылки.</i>"

        await callback.message.edit_text(text=text,
                                         reply_markup=await MyCallback.back_main_menu_ikb(target="BackMainMenu"),
                                         parse_mode="HTML")

    elif callback_data.main == "MyBots":
        my_bots = await CRUDBots.get_all(user_id=callback.from_user.id)
        all_bot = []
        # for i in my_bots:
        #     if i.bot_token != "None":
        #         all_bot.append(i)

        if my_bots:
            await callback.message.edit_text(text="Выберите бот из списка ниже.",
                                             reply_markup=await MyCallback.my_bots_ikb(
                                                 user_id=callback.from_user.id)
                                             )
        else:
            await callback.message.edit_text(text="Вы не добавили ботов",
                                             reply_markup=await MyCallback.back_main_menu_ikb(target="BackMainMenu")
                                             )

    elif callback_data.main == "BackMainMenu":
        await callback.message.edit_text(text="Добро пожаловать в FeedBack Bot – это бот обратной связи в Telegram",
                                         reply_markup=await MyCallback.main_menu_ikb(user_id=callback.from_user.id)
                                         )

    elif callback_data.main == "ShowBot":
        bot_name = callback_data.editId
        bot_id = int(callback_data.id)
        await callback.message.edit_text(text=f"Управление ботом https://t.me/{bot_name}",
                                         reply_markup=await MyCallback.settings_current_bot(bot_id=bot_id))

    elif callback_data.main == "BlockedUser":
        pass

    elif callback_data.main == "NewslettersBot":
        pass

    elif callback_data.main == "StatisticsBot":
        pass

    elif callback_data.main == "WelcomeText":
        bot_id = int(callback_data.id)
        await state.update_data(any_bot_id=bot_id)
        get_bot = await CRUDBots.get(id=bot_id)
        if get_bot:
            welcome_txt = get_bot.welcome_text
            if welcome_txt == "None":
                await callback.message.edit_text(text="У вас не добавлен стартовый текст\n"
                                                      "Желаете добавить новый?",
                                                 reply_markup=await MyCallback.approve_ikb(user_id=callback.from_user.id,
                                                                                           bot_id=bot_id)
                                                 )
            else:
                await callback.message.edit_text(text="Ваш стартовый текст:\n\n"
                                                      f"{welcome_txt}\n\n"
                                                      f"Желеаете добавить новый?",
                                                 reply_markup=await MyCallback.approve_ikb(user_id=callback.from_user.id,
                                                                                           bot_id=bot_id)
                                                 )
        else:
            await callback.message.edit_text(text="Бота не найдено!",
                                             reply_markup=await MyCallback.back_main_menu_ikb(target="ShowBot")
                                             )

    elif callback_data.main == "AddChat":
        bot_id = int(callback_data.id)
        get_bot = await CRUDBots.get(id=bot_id)
        get_chat_bot = await CRUDChats.get(bot_id=get_bot.bot_id)
        if get_chat_bot:
            if get_chat_bot.chat_id == 1:
                await callback.message.edit_text(text="Этот бот не добавлен в чаты, "
                                                      "поэтому все сообщения будут приходить в диалог с ботом.\n\n"
                                                      "Чтобы подключить чат — добавьте бот "
                                                      "как нового участника.",
                                                 reply_markup=await MyCallback.back_main_menu_ikb(target="ShowBot"))
            else:
                my_bot = Bot(token=get_bot.bot_token)
                get_chat = await my_bot.get_chat(chat_id=f"<i>{get_chat_bot.chat_id}</i>")
                await callback.message.edit_text(text=f"Бот подключен к группе: {get_chat.title}",
                                                 reply_markup=await MyCallback.back_main_menu_ikb(target="ShowBot",
                                                                                                  bot_id=bot_id),
                                                 parse_mode="HTML")
                print("yes")
        else:
            await callback.message.edit_text(text="Бот не найден!")

    elif callback_data.main == "AddWelcomeTxt":
        await callback.message.edit_text(text="Введите тест")
        await state.set_state(UserStates.AddWelcomeTxt)


