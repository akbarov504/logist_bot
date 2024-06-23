import pytz, random
from states import state
from keyboards import keyboard
from configs.bot_config import bot, dp
from telethon.sync import TelegramClient
from datetime import datetime, timedelta
from telethon.tl.types.auth import SentCode
from configs import filters, settings, utils
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from aiogram.types import Message, CallbackQuery, ContentType, LabeledPrice, PreCheckoutQuery
from models import language, user, message, message_group, message_group_user, promo_code, offer

utc = pytz.UTC

async def send_message_to_groups_30():
    message_list = message.Message.list()
    for msg in message_list:
        if msg[3] == 30:
            message_group_user_list = message_group_user.MessageGroupUser.list_user_id(msg[1])
            for msg_group_user in message_group_user_list:
                if msg_group_user[2] == msg[0]:
                    msg_group = message_group.MessageGroup.get(msg_group_user[3])
                    async with TelegramClient(msg[7], api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990") as client:
                        await client.send_message(msg_group[2], msg[2])
                        await client.disconnect()
    return None

async def send_message_to_groups_45():
    message_list = message.Message.list()
    for msg in message_list:
        if msg[3] == 45:
            message_group_user_list = message_group_user.MessageGroupUser.list_user_id(msg[1])
            for msg_group_user in message_group_user_list:
                if msg_group_user[2] == msg[0]:
                    msg_group = message_group.MessageGroup.get(msg_group_user[3])
                    async with TelegramClient(msg[7], api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990") as client:
                        await client.send_message(msg_group[2], msg[2])
                        await client.disconnect()
    return None
    
async def send_message_to_groups_60():
    message_list = message.Message.list()
    for msg in message_list:
        if msg[3] == 60:
            message_group_user_list = message_group_user.MessageGroupUser.list_user_id(msg[1])
            for msg_group_user in message_group_user_list:
                if msg_group_user[2] == msg[0]:
                    msg_group = message_group.MessageGroup.get(msg_group_user[3])
                    async with TelegramClient(msg[7], api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990") as client:
                        await client.send_message(msg_group[2], msg[2])
                        await client.disconnect()
    return None

async def check_promo_code_exp():
    promo_code_list = promo_code.PromoCode.list()
    for p_code in promo_code_list:
        if p_code[3] <= datetime.now():
            promo_code.PromoCode.delete(p_code[0])

async def check_user_publsh_day():
    user_list = user.User.list()
    for u in user_list:
        publish_day = user.User.get_publish_day_by_phone(u[3])
        publish_day = publish_day - 1
        user.User.set_publish_day_by_phone(u[3], publish_day)
    
    for u in user_list:
        publish_day = user.User.get_publish_day_by_phone(u[3])
        if publish_day <= 0:
            lang = u[6]
            chat_id = u[5]
            s = state.State("AUTH_MENU", {"LANG": lang}, chat_id)
            state.append(s)
            text = language.Language.get(lang, "CHOOSE_ONE_FROM_THIS_SECTION")
            await bot.send_message(chat_id, text, reply_markup=keyboard.get_auth_menu(lang))

@dp.message_handler(commands=['start'])
async def start_command(msg: Message) -> None:
    s = state.State("LANGUAGE_MENU", {}, msg.chat.id)
    state.append(s)
    text = language.Language.get("NONE", "LANGUAGE_MENU")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_language_manu())

@dp.message_handler(commands=['help'])
async def help_command(msg: Message) -> None:
    await bot.send_document(msg.chat.id, document=open("/Users/akbarovakbar/Documents/akbarov/projects/logist_smart_project/logist_smart_bot/upload/skylog-document-compressed.pdf", "rb"))

@dp.message_handler(filters.CheckState("LANGUAGE_MENU"), lambda msg: msg.text in ["English " + settings.EN_STIK, "Russian " + settings.RU_STIK, "Uzbek " + settings.UZ_STIK])
async def auth_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"LANG": msg.text})
    s = state.State("AUTH_MENU", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(msg.text, "CHOOSE_ONE_FROM_THIS_SECTION")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(msg.text))

@dp.message_handler(filters.CheckState("AUTH_MENU"), filters.CheckWord("REGISTER"))
async def register_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("REGISTER_FIRST_NAME", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_FIRST_NAME")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("REGISTER_FIRST_NAME"))
async def register_first_name_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    data.update({"FIRST_NAME": msg.text})
    s = state.State("REGISTER_LAST_NAME", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_LAST_NAME")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("REGISTER_LAST_NAME"))
async def register_last_name_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    data.update({"LAST_NAME": msg.text})
    s = state.State("REGISTER_PHONE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "SEND_YOUR_CONTACT")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_contact_menu(lang))

@dp.message_handler(filters.CheckState("REGISTER_PHONE"), content_types=ContentType.CONTACT)
async def register_phone_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    data.update({"PHONE_NUMBER": msg.contact.phone_number})
    s = state.State("REGISTER_PASSWORD", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_PASSWORD")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("REGISTER_PASSWORD"))
async def register_password_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    first_name = data.get("FIRST_NAME")
    last_name = data.get("LAST_NAME")
    phone_number = data.get("PHONE_NUMBER")
    password = msg.text
    lang = data.get("LANG")
    s = state.State("AUTH_MENU", {"LANG": lang}, msg.chat.id)
    state.append(s)
    res = user.User.register(first_name, last_name, phone_number, password, lang, msg.chat.id)
    if res:
        text = language.Language.get(lang, "SUCCESSFULLY_REGISTERED")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(lang))
    else:
        text = language.Language.get(lang, "YOU_ARE_ALREADY_REGISTERED")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(lang))

@dp.message_handler(filters.CheckState("AUTH_MENU"), filters.CheckWord("LOGIN"))
async def login_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("LOGIN_PHONE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "SEND_YOUR_CONTACT")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_contact_menu(lang))

@dp.message_handler(filters.CheckState("LOGIN_PHONE"), content_types=ContentType.CONTACT)
async def login_phone_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    data.update({"PHONE_NUMBER": msg.contact.phone_number})
    s = state.State("ENTER_YOUR_PASSWORD", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_PASSWORD")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("ENTER_YOUR_PASSWORD"))
async def login_password_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    password = msg.text
    res = user.User.login(phone, password)
    if res == "NO" or res == "ADMIN" or res == "RECEPTION":
        s = state.State("AUTH_MENU", {"LANG": lang}, msg.chat.id)
        state.append(s)
        text = language.Language.get(lang, "USER_NOT_FOUND")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(lang))
    elif res == "NOT_ACTIVE":
        s = state.State("ACTIVATE_MENU", data, msg.chat.id)
        state.append(s)
        user.User.set_chat_id_by_phone(msg.chat.id, phone)
        text = language.Language.get(lang, "YOU_IS_NOT_ACTIVE")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_active_menu(lang))
    elif res == "STUDENT":
        publish_day = user.User.get_publish_day_by_phone(phone)
        if publish_day > 0:
            s = state.State("HOME_MENU", {"LANG": lang, "role": "STUDENT", "PHONE_NUMBER": phone}, msg.chat.id)
            state.append(s)
            text = language.Language.get(lang, "HOME_MENU")
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))
        else:
            s = state.State("PAYMENT_MENU", {"LANG": lang, "PHONE_NUMBER": phone}, msg.chat.id)
            state.append(s)
            text = language.Language.get(lang, "PAYMENT_MENU")
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_payment_menu(lang))

# @dp.message_handler(filters.CheckState("PAYMENT_MENU"), filters.CheckWord("PAYMENT"))
# async def payment_menu_payment_message(msg: Message) -> None:
#     data = state.get_data(msg.chat.id)
#     lang = data.get("LANG")
#     phone = data.get("PHONE_NUMBER")
#     s = state.State("PAYMENT_MENU_OFFER", data, msg.chat.id)
#     state.append(s)

#     offer_list = offer.Offer.list()
#     for of in offer_list:
#         title = str(of[2]) + " " + language.Language.get(lang, "MONTH")
#         description = "DESCRIPTION"
#         o_price = of[1] * 100
#         price = LabeledPrice(title, int(o_price))
#         price_list = [price]
#         payload = f"IN-{phone}"
#         await bot.send_invoice(msg.chat.id, title, description, payload, "387026696:LIVE:6603d1f7a7e94322f8b5cce1", "UZS", price_list)

# @dp.pre_checkout_query_handler(lambda query: True)
# async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    # phone = pre_checkout_query.invoice_payload[2:]
    # if pre_checkout_query.total_amount == 23000000 or pre_checkout_query.total_amount == 1000:
    #     user.User.set_publish_day_by_phone(phone, 30)
    # elif pre_checkout_query.total_amount == 55200000:
    #     user.User.set_publish_day_by_phone(phone, 90)
    # elif pre_checkout_query.total_amount == 96600000:
    #     user.User.set_publish_day_by_phone(phone, 180)
    # elif pre_checkout_query.total_amount == 165600000:
    #     user.User.set_publish_day_by_phone(phone, 360)
    # else:
    #     user.User.set_publish_day_by_phone(phone, 0)
    # print("hello =================")
    # await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def process_successful_payment(msg: Message) -> None:
#     data = state.get_data(msg.chat.id)
#     lang = data.get("LANG")
#     phone = data.get("PHONE_NUMBER")
#     s = state.State("HOME_MENU", {"LANG": lang, "role": "STUDENT", "PHONE_NUMBER": phone}, msg.chat.id)
#     state.append(s)
#     text1 = language.Language.get(lang, "SUCCESSFULLY_PAID")
#     text2 = language.Language.get(lang, "HOME_MENU")
#     await bot.send_message(msg.chat.id, text1)
#     await bot.send_message(msg.chat.id, text2, reply_markup=keyboard.get_home_student_menu(lang))

@dp.message_handler(filters.CheckState("PAYMENT_MENU"), filters.CheckWord("PROMO_CODE"))
async def payment_menu_promo_code_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("ENTER_PROMO_CODE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_PROMO_CODE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("ENTER_PROMO_CODE"))
async def enter_promo_code_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    publish_day = promo_code.PromoCode.get(msg.text)
    if publish_day is None:
        s = state.State("PAYMENT_MENU", data, msg.chat.id)
        state.append(s)
        text = language.Language.get(lang, "WRONG_PROMO_CODE")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_payment_menu(lang))
    else:
        user.User.set_publish_day_by_phone(phone, publish_day)
        publish_day = user.User.get_publish_day_by_phone(phone)
        if publish_day > 0:
            s = state.State("HOME_MENU", {"LANG": lang, "role": "STUDENT", "PHONE_NUMBER": phone}, msg.chat.id)
            state.append(s)
            text = language.Language.get(lang, "HOME_MENU")
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))
        else:
            s = state.State("PAYMENT_MENU", {"LANG": lang, "PHONE_NUMBER": phone}, msg.chat.id)
            state.append(s)
            text = language.Language.get(lang, "WRONG_PROMO_CODE")
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_payment_menu(lang))
   
@dp.message_handler(filters.CheckState("PAYMENT_MENU"), filters.CheckWord("BACK"))
async def payment_menu_back_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("AUTH_MENU", {"LANG": lang}, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "BACK")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(lang))

@dp.message_handler(filters.CheckState("HOME_MENU"), filters.CheckWord("AUTO_MESSAGE"))
async def home_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("AUTO_MESSAGE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_MESSAGE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("AUTO_MESSAGE"))
async def auto_message_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"MESSAGE": msg.text})
    lang = data.get("LANG")
    s = state.State("YOUR_MESSAGE", data, msg.chat.id)
    state.append(s)
    await bot.send_message(msg.chat.id, msg.text, reply_markup=keyboard.get_message_student_menu(lang))

@dp.callback_query_handler(filters.CheckStateWithCall("YOUR_MESSAGE"), lambda call: call.data == "edit_text")
async def edit_text_student(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")
    s = state.State("AUTO_MESSAGE", data, call.message.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_EDITED_MESSAGE")
    await bot.send_message(call.message.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.callback_query_handler(filters.CheckStateWithCall("YOUR_MESSAGE"), lambda call: call.data == "edit_group")
async def edit_group_student(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")
    s = state.State("EDIT_GROUP", data, call.message.chat.id)
    state.append(s)
    text1 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/RHNZfUlgvrw4NjMy"
    text2 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/XcVvS4iCkjgxODIy"
    text3 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/JpYEd0NARAg1NGIy"
    text4 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/RvBrbkj_ygAwODk6"
    await bot.send_message(call.message.chat.id, text1, reply_markup=keyboard.remove_menu)
    await bot.send_message(call.message.chat.id, text2, reply_markup=keyboard.remove_menu)
    await bot.send_message(call.message.chat.id, text3, reply_markup=keyboard.remove_menu)
    await bot.send_message(call.message.chat.id, text4, reply_markup=keyboard.get_done_student_menu(lang))

@dp.message_handler(filters.CheckStateList(["EDIT_GROUP", "JOIN_GROUP"]), filters.CheckWord("DONE"))
async def done_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"PAGE": 0})
    lang = data.get("LANG")
    s = state.State("GROUP_BTN", data, msg.chat.id)
    state.append(s)
    my_groups = await utils.get_my_groups(msg.chat.id)
    text = language.Language.get(lang, "CORRECT_OR_INCORRECT")
    await bot.send_message(msg.chat.id, text, reply_markup=await keyboard.get_add_group_student_menu(lang, 0, msg.chat.id, my_groups))
        
@dp.callback_query_handler(filters.CheckStateWithCall("GROUP_BTN"))
async def group_btn_student(call: CallbackQuery) -> None:
    my_groups = await utils.get_my_groups(call.message.chat.id)
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")
    if call.data in my_groups:
        group_list:list = data.get("GROUP_LIST", [])
        if call.data in group_list:
            group_list.remove(call.data)
            data.update({"GROUP_LIST": group_list})
        else:
            group_list.append(call.data)
            data.update({"GROUP_LIST": group_list})
        s = state.State("GROUP_BTN", data, call.message.chat.id)
        state.append(s)
        page = data.get("PAGE")
        await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=await keyboard.get_add_group_student_menu(lang, page, call.message.chat.id, my_groups))
        return None
    elif call.data == "prev":
        page = data.get("PAGE") - 1
        data.update({"PAGE": page})
        s = state.State("GROUP_BTN", data, call.message.chat.id)
        state.append(s)
        await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=await keyboard.get_add_group_student_menu(lang, page, call.message.chat.id, my_groups))
    elif call.data == "next":
        page = data.get("PAGE") + 1
        data.update({"PAGE": page})
        s = state.State("GROUP_BTN", data, call.message.chat.id)
        state.append(s)
        await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=await keyboard.get_add_group_student_menu(lang, page, call.message.chat.id, my_groups))
    elif call.data == "select_all":
        group_list:list = data.get("GROUP_LIST", [])
        page = data.get("PAGE")
        for m_g in my_groups:
            group_list.append(m_g)
        data.update({"GROUP_LIST": group_list})
        s = state.State("GROUP_BTN", data, call.message.chat.id)
        state.append(s)
        await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=await keyboard.get_add_group_student_menu(lang, page, call.message.chat.id, my_groups))
    else:
        text = language.Language.get(lang, "WRONG_MESSAGE")
        await bot.send_message(call.message.chat.id, text)
        return None

@dp.message_handler(filters.CheckState("GROUP_BTN"), filters.CheckWord("DONE"))
async def group_done_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    
    phone = data.get("PHONE_NUMBER")
    user_id = user.User.get_id_by_phone(phone)
    message_group_user.MessageGroupUser.add_groups_to_user(user_id, msg.chat.id)
    text1 = language.Language.get(lang, "SUCCESSFULLY_SELECTED_GROUPS")

    text2 = data.get("MESSAGE")
    if text2 is None:
        s = state.State("HOME_MENU", data, msg.chat.id)
        state.append(s)
        text2 = language.Language.get(lang, "HOME_MENU")
        await bot.send_message(msg.chat.id, text1, reply_markup=keyboard.remove_menu)
        await bot.send_message(msg.chat.id, text2, reply_markup=keyboard.get_home_student_menu(lang))
    else:
        s = state.State("YOUR_MESSAGE", data, msg.chat.id)
        state.append(s)
        await bot.send_message(msg.chat.id, text1, reply_markup=keyboard.remove_menu)
        await bot.send_message(msg.chat.id, text2, reply_markup=keyboard.get_message_student_menu(lang))

@dp.callback_query_handler(filters.CheckStateWithCall("YOUR_MESSAGE"), lambda call: call.data == "edit_timer")
async def edit_timer_student(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")
    s = state.State("EDIT_TIMER", data, call.message.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_TIMER")
    await bot.send_message(call.message.chat.id, text, reply_markup=keyboard.get_timer_student_menu(lang))

@dp.message_handler(filters.CheckState("EDIT_TIMER"), filters.CheckWord("MINUTE_30"))
async def start_time_student_30_minute(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    id = user.User.get_id_by_phone(phone)
    mess = data.get("MESSAGE")

    res = message.Message.create(id, mess, 30, phone)
    data.update({"MESSAGE_ID": res[0]})

    s = state.State("YOUR_MESSAGE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "SUCCESSFULLY_CREATED_YOUR_MESSAGE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)
    await bot.send_message(msg.chat.id, mess, reply_markup=keyboard.get_message_student_menu(lang))

@dp.message_handler(filters.CheckState("EDIT_TIMER"), filters.CheckWord("MINUTE_45"))
async def start_time_student_45_minute(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    id = user.User.get_id_by_phone(phone)
    mess = data.get("MESSAGE")

    res = message.Message.create(id, mess, 45, phone)
    data.update({"MESSAGE_ID": res[0]})

    s = state.State("YOUR_MESSAGE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "SUCCESSFULLY_CREATED_YOUR_MESSAGE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)
    await bot.send_message(msg.chat.id, mess, reply_markup=keyboard.get_message_student_menu(lang))

@dp.message_handler(filters.CheckState("EDIT_TIMER"), filters.CheckWord("MINUTE_60"))
async def start_time_student_60_minute(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    id = user.User.get_id_by_phone(phone)
    mess = data.get("MESSAGE")

    res = message.Message.create(id, mess, 60, phone)
    data.update({"MESSAGE_ID": res[0]})

    s = state.State("YOUR_MESSAGE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "SUCCESSFULLY_CREATED_YOUR_MESSAGE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)
    await bot.send_message(msg.chat.id, mess, reply_markup=keyboard.get_message_student_menu(lang))

@dp.callback_query_handler(filters.CheckStateWithCall("YOUR_MESSAGE"), lambda call: call.data == "start")
async def start_student(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")

    message_id = data.get("MESSAGE_ID")
    if message_id is None:
        text = language.Language.get(lang, "PLEASE_SELECT_TIMER")
        await bot.send_message(call.message.chat.id, text)
        return None
    
    page = data.get("PAGE")
    group_list = data.get("GROUP_LIST")
    if group_list is None or page is None:
        text = language.Language.get(lang, "PLEASE_SELECT_GROUPS")
        await bot.send_message(call.message.chat.id, text)
        return None
    
    if group_list == []:
        text = language.Language.get(lang, "PLEASE_SELECT_GROUPS")
        await bot.send_message(call.message.chat.id, text)
        return None
    mess = data.get("MESSAGE")
    data.pop("MESSAGE")
    data.pop("MESSAGE_ID")
    data.pop("PAGE")
    data.pop("GROUP_LIST")
    s = state.State("HOME_MENU", data, call.message.chat.id)
    state.append(s)
    phone = data.get("PHONE_NUMBER")
    user_id = user.User.get_id_by_phone(phone)
    await message.Message.change_status(user_id, message_id, True, mess, phone)
    text = language.Language.get(lang, "BACK_HOME_MENU")
    await bot.send_message(call.message.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))

@dp.message_handler(filters.CheckState("HOME_MENU"), filters.CheckWord("SEARCH_CARGO"))
async def search_cargo_from_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"MESSAGE_PAGE": 1})
    lang = data.get("LANG")
    s = state.State("SEARCH_CARGO_FROM", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_CARGO_FROM")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("SEARCH_CARGO_FROM"))
async def search_cargo_to_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"CARGO_FROM": msg.text})
    lang = data.get("LANG")
    s = state.State("SEARCH_CARGO_TO", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_CARGO_TO")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("SEARCH_CARGO_TO"))
async def search_cargo_type_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"CARGO_TO": msg.text})
    lang = data.get("LANG")
    s = state.State("SEARCH_CARGO", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_CARGO_TYPE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_cargo_type_menu(lang))

@dp.message_handler(filters.CheckState("SEARCH_CARGO"), filters.CheckWordList(["ISOTHERM", "REF", "AWNING"]))
async def search_cargo_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"CARGO_TYPE": msg.text})

    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    cargo_from = data.get("CARGO_FROM")
    cargo_from = cargo_from.lower()
    cargo_to = data.get("CARGO_TO")
    cargo_to = cargo_to.lower()
    cargo_type = msg.text
    cargo_type = cargo_type.lower()
    message_page = data.get("MESSAGE_PAGE")
    
    date = datetime.now() - timedelta(days=1)
    message_group_list = await utils.get_my_groups(msg.chat.id)
    mes_list = []
    async with TelegramClient(session=phone, api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990") as client:
        await client.connect()
        for msg_group in message_group_list:
            message_counter = 0
            async for ms in client.iter_messages(msg_group, min_id=1):
                message_counter = message_counter + 1
                date = date.replace(tzinfo=utc)
                ms.date = ms.date.replace(tzinfo=utc)
                if ms.message is None:
                    continue
                for msss in mes_list:
                    if ms.message == msss.message:
                        mes_list.remove(msss)
                        
                messa = ms.message.lower()
                res1 = messa.find(cargo_from)
                res2 = messa.find(cargo_to)
                res3 = messa.find(cargo_type)
                if  ms.date >= date and res1 != -1 and res2 != -1 and res3 != -1:
                    mes_list.append(ms)

                if len(mes_list) == message_page * 5:
                    break

                if message_counter == 300:
                    break
    
        await client.disconnect()
    
    s = state.State("SEARCH_CARGO", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_ONE_OF_THE_CARGOS")
    text+=f"\nPage: {message_page}"
    await bot.send_message(msg.chat.id, text, reply_markup=await keyboard.get_cargo_menu(lang, mes_list, message_page, cargo_from, cargo_to, phone))

@dp.callback_query_handler(filters.CheckStateWithCall("SEARCH_CARGO"), lambda call: call.data == "next")
async def search_cargo_next_student(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    page = data.get("MESSAGE_PAGE") + 1
    data.update({"MESSAGE_PAGE": page})

    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    cargo_from = data.get("CARGO_FROM")
    cargo_from = cargo_from.lower()
    cargo_to = data.get("CARGO_TO")
    cargo_to = cargo_to.lower()
    cargo_type = data.get("CARGO_TYPE")
    cargo_type = cargo_type.lower()

    date = datetime.now() - timedelta(days=1)
    message_group_list = await utils.get_my_groups(call.message.chat.id)

    mes_list = []
    async with TelegramClient(session=phone, api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990") as client:
        await client.connect()
        for msg_group in message_group_list:
            message_counter = 0
            async for ms in client.iter_messages(msg_group, min_id=1):
                message_counter = message_counter + 1
                date = date.replace(tzinfo=utc)
                ms.date = ms.date.replace(tzinfo=utc)
                if ms.message is None:
                    continue
                for msss in mes_list:
                    if ms.message == msss.message:
                        mes_list.remove(msss)

                messa = ms.message.lower()
                res1 = messa.find(cargo_from)
                res2 = messa.find(cargo_to)
                res3 = messa.find(cargo_type)
                if  ms.date >= date and res1 != -1 and res2 != -1 and res3 != -1:
                    mes_list.append(ms)

                if len(mes_list) == page * 5:
                    break

                if message_counter == 300:
                    break
        await client.disconnect()

    s = state.State("SEARCH_CARGO", data, call.message.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_ONE_OF_THE_CARGOS")
    text+=f"\nPage: {page}"
    await bot.edit_message_text(text, call.message.chat.id, message_id=call.message.message_id, reply_markup=await keyboard.get_cargo_menu(lang, mes_list, page, cargo_from, cargo_to, phone))

@dp.callback_query_handler(filters.CheckStateWithCall("SEARCH_CARGO"), lambda call: call.data == "prev")
async def search_cargo_prev_student(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    page = data.get("MESSAGE_PAGE") - 1
    data.update({"MESSAGE_PAGE": page})

    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    cargo_from = data.get("CARGO_FROM")
    cargo_from = cargo_from.lower()
    cargo_to = data.get("CARGO_TO")
    cargo_to = cargo_to.lower()
    cargo_type = data.get("CARGO_TYPE")
    cargo_type = cargo_type.lower()
    message_page = data.get("MESSAGE_PAGE")

    date = datetime.now() - timedelta(days=1)
    message_group_list = await utils.get_my_groups(call.message.chat.id)

    mes_list = []
    async with TelegramClient(session=phone, api_id=24963729, api_hash="1bab3b9c3675227b43619d2175bd6990") as client:
        await client.connect()
        for msg_group in message_group_list:
            message_counter = 0
            async for ms in client.iter_messages(msg_group, min_id=1):
                message_counter = message_counter + 1
                date = date.replace(tzinfo=utc)
                ms.date = ms.date.replace(tzinfo=utc)
                if ms.message is None:
                    continue
                for msss in mes_list:
                    if ms.message == msss.message:
                        mes_list.remove(msss)

                messa = ms.message.lower()
                res1 = messa.find(cargo_from)
                res2 = messa.find(cargo_to)
                res3 = messa.find(cargo_type)
                if  ms.date >= date and res1 != -1 and res2 != -1 and res3 != -1:
                    mes_list.append(ms)

                if len(mes_list) == message_page * 5:
                    break
                if message_counter == 300:
                    break
        await client.disconnect()

    s = state.State("SEARCH_CARGO", data, call.message.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_ONE_OF_THE_CARGOS")
    text+=f"\nPage: {page}"
    await bot.edit_message_text(text, call.message.chat.id, message_id=call.message.message_id, reply_markup=await keyboard.get_cargo_menu(lang, mes_list, page, cargo_from, cargo_to, phone))

@dp.callback_query_handler(filters.CheckStateWithCall("SEARCH_CARGO"), lambda call: call.data == "back")
async def search_cargo_back_message(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    s = state.State("HOME_MENU", {"LANG": lang, "role": "STUDENT", "PHONE_NUMBER": phone}, call.message.chat.id)
    state.append(s)
    text = language.Language.get(lang, "BACK")
    await bot.send_message(call.message.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))

@dp.message_handler(filters.CheckState("HOME_MENU"), filters.CheckWord("HISTORY"))
async def message_history_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    user_id = user.User.get_id_by_phone(phone)
    s = state.State("HISTORY", data, msg.chat.id)
    state.append(s)

    messages = message.Message.list_by_user_id(user_id)
    for ms in messages:
        text = f"""ID: {ms[0]}
Message: {ms[2]}
Timer: {ms[3]}
Status: {ms[4]}"""
        if ms[4] == True:
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_stop_message_menu(lang))
        else:
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)
    text = language.Language.get(lang, "BACK")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_history_back_menu(lang))

@dp.message_handler(filters.CheckState("HISTORY"), filters.CheckWord("BACK"))
async def back_history_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("HOME_MENU", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "BACK")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))

@dp.callback_query_handler(filters.CheckStateWithCall("HISTORY"), lambda call: call.data == "stop")
async def history_menu(call: CallbackQuery) -> None:
    data = state.get_data(call.message.chat.id)
    lang = data.get("LANG")
    s = state.State("HISTORY_STOP", data, call.message.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_MESSAGE_ID")
    await bot.send_message(call.message.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("HISTORY_STOP"))
async def history_stop_menu(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    user_id = user.User.get_id_by_phone(phone)
    s = state.State("HOME_MENU", data, msg.chat.id)
    state.append(s)

    messages = message.Message.list_by_user_id(user_id)
    for ms in messages:
        if str(ms[0]) == msg.text:
            message.Message.set_status(user_id, ms[0], False)
    text = language.Language.get(lang, "HOME_MENU")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))

@dp.message_handler(filters.CheckState("HOME_MENU"), filters.CheckWord("PROFILE"))
async def profile_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    s = state.State("PROFILE", data, msg.chat.id)
    state.append(s)

    u = user.User.get_by_phone(phone)
    info = language.Language.get(lang, "FIRST_NAME") + f": {u[1]}\n"
    info += language.Language.get(lang, "LAST_NAME") + f": {u[2]}\n"
    info += language.Language.get(lang, "PHONE_NUMBER") + f": {u[3]}\n"
    info += language.Language.get(lang, "PUBLISH_DAY") + f": {u[8]} " + language.Language.get(lang, "DAY")
    text = language.Language.get(lang, "CHOOSE_ONE_FROM_THIS_SECTION")
    await bot.send_message(msg.chat.id, info)
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_profile_menu(lang))

@dp.message_handler(filters.CheckState("PROFILE"), filters.CheckWord("CHANGE_LANGUAGE"))
async def profile_change_language_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    s = state.State("PROFILE_CHANGE_LANGUAGE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get("NONE", "LANGUAGE_MENU")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_language_manu())

@dp.message_handler(filters.CheckState("PROFILE_CHANGE_LANGUAGE"), lambda msg: msg.text in ["English " + settings.EN_STIK, "Russian " + settings.RU_STIK, "Uzbek " + settings.UZ_STIK])
async def profile_change_language_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"LANG": msg.text})
    lang = msg.text
    s = state.State("PROFILE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_ONE_FROM_THIS_SECTION")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_profile_menu(lang))

@dp.message_handler(filters.CheckState("PROFILE"), filters.CheckWord("LOGOUT"))
async def profile_logout_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("AUTH_MENU", {"LANG": lang}, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "GOODBYE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(lang))

@dp.message_handler(filters.CheckState("PROFILE"), filters.CheckWord("BACK"))
async def profile_back_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("HOME_MENU", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_ONE_FROM_THIS_SECTION")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))

@dp.message_handler(filters.CheckState("HOME_MENU"), filters.CheckWord("JOIN_GROUP"))
async def join_group_menu_student(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("JOIN_GROUP", data, msg.chat.id)
    state.append(s)
    text1 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/RHNZfUlgvrw4NjMy"
    text2 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/XcVvS4iCkjgxODIy"
    text3 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/JpYEd0NARAg1NGIy"
    text4 = language.Language.get(lang, "SUBSCRIBE")+"\n\n" + "https://t.me/addlist/RvBrbkj_ygAwODk6"
    await bot.send_message(msg.chat.id, text1, reply_markup=keyboard.remove_menu)
    await bot.send_message(msg.chat.id, text2, reply_markup=keyboard.remove_menu)
    await bot.send_message(msg.chat.id, text3, reply_markup=keyboard.remove_menu)
    await bot.send_message(msg.chat.id, text4, reply_markup=keyboard.get_done_student_menu(lang))

@dp.message_handler(filters.CheckState("ACTIVATE_MENU"), filters.CheckWord("ACTIVATE"))
async def activate_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("HAVE_2FA", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "YOU_HAVE_2FA")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_question_menu(lang))

@dp.message_handler(filters.CheckState("HAVE_2FA"), filters.CheckWord("YES"))
async def have_2fa_yes(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    phone = data.get("PHONE_NUMBER")
    client = await utils.get_client(phone)
    await client.connect()
    res: SentCode = await client.send_code_request(phone)
    client.session.save()
    await client.disconnect()
    data.update({"HASH": res.phone_code_hash})
    lang = data.get("LANG")
    s = state.State("ENTER_ACTIVATE_PASSWORD", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_PASSWORD_TG")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("HAVE_2FA"), filters.CheckWord("NO"))
async def have_2fa_NO(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    phone = data.get("PHONE_NUMBER")
    client = await utils.get_client(phone)
    await client.connect()
    res: SentCode = await client.send_code_request(phone)
    client.session.save()
    await client.disconnect()
    data.update({"HASH": res.phone_code_hash})
    lang = data.get("LANG")
    s = state.State("ASK_LOGIN", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ASK_LOGIN")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_question_menu(lang))
    
@dp.message_handler(filters.CheckState("ENTER_ACTIVATE_PASSWORD"))
async def enter_activate_password_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    data.update({"PASSWORD": msg.text})
    lang = data.get("LANG")
    s = state.State("ASK_LOGIN", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ASK_LOGIN")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_question_menu(lang))

@dp.message_handler(filters.CheckState("ASK_LOGIN"), filters.CheckWord("YES"))
async def ask_login_yes(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("ENTER_ACTIVATE_CODE", data, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "ENTER_YOUR_CODE")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.remove_menu)

@dp.message_handler(filters.CheckState("ASK_LOGIN"), filters.CheckWord("NO"))
async def ask_login_no(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    s = state.State("AUTH_MENU", {"LANG": lang}, msg.chat.id)
    state.append(s)
    text = language.Language.get(lang, "CHOOSE_ONE_FROM_THIS_SECTION")
    await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_auth_menu(lang))

@dp.message_handler(filters.CheckState("ENTER_ACTIVATE_CODE"))
async def enter_activate_code_message(msg: Message) -> None:
    data = state.get_data(msg.chat.id)
    lang = data.get("LANG")
    phone = data.get("PHONE_NUMBER")
    password = data.get("PASSWORD", "")
    hash = data.get("HASH") 
    s = state.State("LANGUAGE_MENU", {"PHONE_NUMBER": phone, "LANG": lang}, msg.chat.id)
    state.append(s)
    client = await utils.get_client(phone)
    await client.connect()
    try:
        await client.sign_in(phone=phone, code=str(msg.text), phone_code_hash=hash)
    except SessionPasswordNeededError as e:
        await client.sign_in(password=str(password))
    await client.disconnect()
    user.User.change_active(phone, msg.chat.id)

    publish_day = user.User.get_publish_day_by_phone(phone)
    if publish_day > 0:
        s = state.State("HOME_MENU", {"LANG": lang, "role": "STUDENT", "PHONE_NUMBER": phone}, msg.chat.id)
        state.append(s)
        text = language.Language.get(lang, "HOME_MENU")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_home_student_menu(lang))
    else:
        s = state.State("PAYMENT_MENU", {"LANG": lang, "PHONE_NUMBER": phone}, msg.chat.id)
        state.append(s)
        text = language.Language.get(lang, "PAYMENT_MENU")
        await bot.send_message(msg.chat.id, text, reply_markup=keyboard.get_payment_menu(lang))
