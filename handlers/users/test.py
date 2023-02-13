from typing import Optional

from aiogram import types
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

from loader import curDP
user_data = {}


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]

    @staticmethod
    async def get_keyboard_fab():
        builder = InlineKeyboardBuilder()
        builder.button(
            text="-2", callback_data=NumbersCallbackFactory(action="change", value=-2)
        )
        builder.button(
            text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1)
        )
        builder.button(
            text="+1", callback_data=NumbersCallbackFactory(action="change", value=1)
        )
        builder.button(
            text="+2", callback_data=NumbersCallbackFactory(action="change", value=2)
        )
        builder.button(
            text="Подтвердить", callback_data=NumbersCallbackFactory(action="finish")
        )
        # Выравниваем кнопки по 4 в ряд, чтобы получилось 4 + 1
        builder.adjust(4)
        return builder.as_markup()

    @staticmethod
    async def update_num_text_fab(message: types.Message, new_value: int):
        with suppress(TelegramBadRequest):
            await message.edit_text(
                f"Укажите число: {new_value}",
                reply_markup=await NumbersCallbackFactory.get_keyboard_fab()
            )


@curDP.message(commands=["numbers_fab"])
async def cmd_numbers_fab(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=await NumbersCallbackFactory.get_keyboard_fab())


@curDP.callback_query(NumbersCallbackFactory.filter())
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)
    # Если число нужно изменить
    if callback_data.action == "change":
        user_data[callback.from_user.id] = user_value + callback_data.value
        await NumbersCallbackFactory.update_num_text_fab(callback.message, user_value + callback_data.value)
    # Если число нужно зафиксировать
    else:
        await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()