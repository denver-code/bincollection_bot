from aiogram import types

from core.redis import is_subscribed

def inline_menu_markup(id) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Get Schedule', callback_data='get_schedule'),
        types.InlineKeyboardButton(text='Next Collection', callback_data='next_collection'),
        types.InlineKeyboardButton(
            text='Unsubscribe' if is_subscribed(id) else "Subscribe",
            callback_data='subscription_toggle'
        ),
        types.InlineKeyboardButton(text='Adjust Location', callback_data='adjust_location'),
        types.InlineKeyboardButton(text='Calendar Picture', callback_data='calendar_schedule'),
    ]
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(*buttons)

    return keyboard_markup