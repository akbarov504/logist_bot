from models import language, message_group, message_group_user
from configs.settings import EN_STIK, RU_STIK, UZ_STIK
from states import state
from configs import utils
from telethon.sync import TelegramClient
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

remove_menu = ReplyKeyboardRemove(selective=True)

def get_language_manu() -> ReplyKeyboardMarkup:
    language_manu = ReplyKeyboardMarkup(resize_keyboard=True)

    en = KeyboardButton("English " + EN_STIK)
    ru = KeyboardButton("Russian " + RU_STIK)
    uz = KeyboardButton("Uzbek " + UZ_STIK)
    language_manu.add(en, ru)
    language_manu.add(uz)

    return language_manu

def get_auth_menu(lang: str) -> ReplyKeyboardMarkup:
    auth_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    login = KeyboardButton(language.Language.get(lang, "LOGIN"))
    register = KeyboardButton(language.Language.get(lang, "REGISTER"))
    auth_menu.add(login, register)

    return auth_menu

def get_contact_menu(lang: str) -> ReplyKeyboardMarkup:
    contact_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    contact = KeyboardButton(language.Language.get(lang, "SEND_CONTACT"), request_contact=True)
    contact_menu.add(contact)

    return contact_menu

def get_active_menu(lang: str) -> ReplyKeyboardMarkup:
    active_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    active = KeyboardButton(language.Language.get(lang, "ACTIVATE"))
    active_menu.add(active)

    return active_menu

def get_question_menu(lang: str) -> ReplyKeyboardMarkup:
    question_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton(language.Language.get(lang, "YES"))
    no = KeyboardButton(language.Language.get(lang, "NO"))
    question_menu.add(yes, no)

    return question_menu

def get_home_student_menu(lang: str) -> ReplyKeyboardMarkup:
    home_student_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    join_group = KeyboardButton(language.Language.get(lang, "JOIN_GROUP"))
    auto_message = KeyboardButton(language.Language.get(lang, "AUTO_MESSAGE"))
    search_cargo = KeyboardButton(language.Language.get(lang, "SEARCH_CARGO"))
    message_history = KeyboardButton(language.Language.get(lang, "HISTORY"))
    profile = KeyboardButton(language.Language.get(lang, "PROFILE"))
    home_student_menu.add(join_group, auto_message)
    home_student_menu.add(search_cargo, message_history)
    home_student_menu.add(profile)

    return home_student_menu

def get_stop_message_menu(lang: str) -> InlineKeyboardMarkup:
    stop_message_menu = InlineKeyboardMarkup()

    stop = InlineKeyboardButton(language.Language.get(lang, "STOP"), callback_data="stop")    
    stop_message_menu.add(stop)

    return stop_message_menu

def get_profile_menu(lang: str) -> ReplyKeyboardMarkup:
    profile_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    change_language = KeyboardButton(language.Language.get(lang, "CHANGE_LANGUAGE"))
    logout = KeyboardButton(language.Language.get(lang, "LOGOUT"))
    back = KeyboardButton(language.Language.get(lang, "BACK"))
    profile_menu.add(logout)
    profile_menu.add(change_language)
    profile_menu.add(back)

    return profile_menu

def get_payment_menu(lang: str) -> ReplyKeyboardMarkup:
    payment_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    # payment = KeyboardButton(language.Language.get(lang, "PAYMENT"))
    promo_code = KeyboardButton(language.Language.get(lang, "PROMO_CODE"))
    back = KeyboardButton(language.Language.get(lang, "BACK"))
    payment_menu.add(promo_code)
    payment_menu.add(back)

    return payment_menu

def get_cargo_type_menu(lang: str) -> ReplyKeyboardMarkup:
    cargo_type_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    awning = KeyboardButton(language.Language.get(lang, "AWNING"))
    ref = KeyboardButton(language.Language.get(lang, "REF"))
    isotherm = KeyboardButton(language.Language.get(lang, "ISOTHERM"))
    cargo_type_menu.add(awning)
    cargo_type_menu.add(ref, isotherm)

    return cargo_type_menu

def get_message_student_menu(lang: str) -> InlineKeyboardMarkup:
    message_student_menu = InlineKeyboardMarkup()

    edit_text = InlineKeyboardButton(language.Language.get(lang, "EDIT_TEXT"), callback_data="edit_text")
    edit_group = InlineKeyboardButton(language.Language.get(lang, "EDIT_GROUP"), callback_data="edit_group")
    edit_timer = InlineKeyboardButton(language.Language.get(lang, "EDIT_TIMER"), callback_data="edit_timer")
    start = InlineKeyboardButton(language.Language.get(lang, "START"), callback_data="start")

    message_student_menu.add(edit_text)
    message_student_menu.add(edit_group)
    message_student_menu.add(edit_timer)
    message_student_menu.add(start)

    return message_student_menu

def get_done_student_menu(lang: str) -> ReplyKeyboardMarkup:
    done_student_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    done = KeyboardButton(language.Language.get(lang, "DONE"))
    done_student_menu.add(done)
    
    return done_student_menu

def get_history_back_menu(lang: str) -> ReplyKeyboardMarkup:
    history_back_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    back = KeyboardButton(language.Language.get(lang, "BACK"))
    history_back_menu.add(back)
    
    return history_back_menu

async def get_add_group_student_menu(lang: str, page: int, chat_id: int, my_groups: list) -> InlineKeyboardMarkup:
    add_group_menu = InlineKeyboardMarkup()
    
    data = state.get_data(chat_id)
    group_list = data.get("GROUP_LIST")
    page = page * 5
    for group in my_groups[page:page+5]:
        if group_list is None or group_list == []:
            add_group_menu.add(InlineKeyboardButton(group, callback_data=group))
        elif group in group_list:
            add_group_menu.add(InlineKeyboardButton(group + " ✅", callback_data=group))
        else:
            add_group_menu.add(InlineKeyboardButton(group, callback_data=group))

    size = len(my_groups)
    if page == 0:
        add_group_menu.add(InlineKeyboardButton(language.Language.get(lang, "NEXT"), callback_data="next"))    
    elif (page + 1) >  size / 5:
        add_group_menu.add(InlineKeyboardButton(language.Language.get(lang, "PREVIOUS"), callback_data="prev"), InlineKeyboardButton(language.Language.get(lang, "NEXT"), callback_data="next"))
    else:
        add_group_menu.add(InlineKeyboardButton(language.Language.get(lang, "PREVIOUS"), callback_data="prev"))
    add_group_menu.add(InlineKeyboardButton(language.Language.get(lang, "SELECT_ALL"), callback_data="select_all"))
    return add_group_menu

def get_timer_student_menu(lang: str) -> ReplyKeyboardMarkup:
    timer_student_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    one = KeyboardButton(language.Language.get(lang, "MINUTE_30"))
    two = KeyboardButton(language.Language.get(lang, "MINUTE_45"))
    three = KeyboardButton(language.Language.get(lang, "MINUTE_60"))
    timer_student_menu.add(one, two)
    timer_student_menu.add(three)

    return timer_student_menu

async def get_cargo_menu(lang: str, msg_list: list, message_page: int, cargo_from: str, cargo_to: str, phone: str) -> InlineKeyboardMarkup:
    cargo_menu = InlineKeyboardMarkup()
    message_page = message_page - 1
    msg_list = msg_list[message_page*5:]
    client:TelegramClient = await utils.get_client(phone)
    await client.connect()
    for msg in msg_list:
        channel_entity = await client.get_entity(msg.peer_id)
        url = f"https://t.me/{channel_entity.username}/{msg.id}"
        btn = InlineKeyboardButton(text=cargo_from + " - " + cargo_to, url=url)
        cargo_menu.add(btn)
    await client.disconnect()
    if message_page == 0:
        cargo_menu.add(InlineKeyboardButton(language.Language.get(lang, "NEXT"), callback_data="next"))    
        cargo_menu.add(InlineKeyboardButton(language.Language.get(lang, "BACK"), callback_data="back"))
    elif message_page >  0:
        cargo_menu.add(InlineKeyboardButton(language.Language.get(lang, "PREVIOUS"), callback_data="prev"), InlineKeyboardButton(language.Language.get(lang, "NEXT"), callback_data="next"))
        cargo_menu.add(InlineKeyboardButton(language.Language.get(lang, "BACK"), callback_data="back"))
    return cargo_menu
