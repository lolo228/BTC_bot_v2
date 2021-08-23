import os
import sqlite3
import time
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import TOKEN, admin_id

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

connect = sqlite3.connect('users_info.bd')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users_info(
        user_id INT PRIMARY KEY,
        user_teg TEXT
    )""")

connect.commit()

connect = sqlite3.connect('ban_users.bd')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ban_users(
        ban_user_id INT PRIMARY KEY,
        ban_user_teg TEXT
    )""")

connect.commit()

connect = sqlite3.connect('btc_checks.bd')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS btc_checks(
        btc_check TEXT
    )""")

connect.commit()

connect = sqlite3.connect('products_list.bd')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS spotify_acc(
        login_pass TEXT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS youtube_acc(
        login_pass TEXT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS game_acc(
        login_pass
    )""")

connect.commit()

@dp.message_handler(commands=['start'], state=None)
async def command_start(message: types.Message):
    if message.from_user.username is None:
        await bot.send_message(message.from_user.id, '⛔️<b>Внимание!</b> чтобы пользоваться данным ботом, вы должны иметь <b>тег</b>⛔', parse_mode='html')
    else:
        connect = sqlite3.connect('ban_users.bd')
        cursor = connect.cursor()

        cursor.execute(f"SELECT ban_user_id FROM ban_users WHERE ban_user_id = {message.from_user.id}")
        data_ban = cursor.fetchone()
        connect.commit()
        if data_ban is None:
            connect = sqlite3.connect('users_info.bd')
            cursor = connect.cursor()

            people_id = message.from_user.id
            cursor.execute(f"SELECT user_id FROM users_info WHERE user_id = {people_id}")
            data = cursor.fetchone()

            if data is None:
                user_id = message.from_user.id
                user_teg = message.from_user.username

                user_inf = [user_id, user_teg]

                cursor.execute("INSERT INTO users_info VALUES(?,?)", user_inf)
                connect.commit()
                await bot.send_message(admin_id, f'Новый пользователь @{user_teg} с id{user_id} зашёл в бота!')
            else:
                pass

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            box_button = types.KeyboardButton('🗃Коробка')
            acc_button = types.KeyboardButton('💈Бесплатные аккаунты')
            BTC_obnal_button = types.KeyboardButton('📋Как вывести деньги с BTC банкир')
            bot_info_button = types.KeyboardButton('📋Информация о боте')
            markup.add(box_button, acc_button, BTC_obnal_button, bot_info_button)

            await bot.send_message(message.from_user.id, f'Приветствую тебя <b>{message.from_user.first_name}</b>!\n\n ⚜️Добро пожаловать в бота в котором ты сможешь получить не только халявный BTC чек с деньгами, но и бесплатные аккаунты, начинаю от Spotify premium заканчивая WoT⚜\n\nДля получение подробной информации пропишите команду /help', parse_mode='html', reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, 'Внимание! Вы забанены администратором')



@dp.message_handler(commands=['help'], state=None)
async def command_help(message: types.Message):
    if message.from_user.username is None:
        await bot.send_message(message.from_user.id, '⛔<b>Внимание!</b> чтобы пользоваться данным ботом, вы должны иметь <b>тег</b>⛔', parse_mode='html')
    else:
        connect = sqlite3.connect('ban_users.bd')
        cursor = connect.cursor()

        cursor.execute(f"SELECT ban_user_id FROM ban_users WHERE ban_user_id = {message.from_user.id}")
        data_ban = cursor.fetchone()
        connect.commit()
        if data_ban is None:
            await bot.send_message(message.from_user.id, 'Чтобы получить BTC чек нажмите на кнопку 🗃<em>Коробка</em>, чтобы получить бесплтаные аккаунты нажмите на кнопку 💈<em>Бесплатные аккаунты</em>.', parse_mode='html')
        else:
            await bot.send_message(message.from_user.id, 'Внимание! Вы забанены администратором')


@dp.message_handler(commands=['admin'], state=None)
async def command_admin(message: types.Message):
    if int(message.from_user.id) == admin_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        add_BTC_button = types.KeyboardButton('➕Добавить BTC чек')
        add_free_acc_button = types.KeyboardButton('➕Добавить бесплатные аккаунты')
        mailing_button = types.KeyboardButton('📣Запусить рассылку')
        exit_button = types.KeyboardButton('Выход')
        markup.add(add_BTC_button, add_free_acc_button, mailing_button, exit_button)

        await bot.send_message(message.from_user.id, '✅Администратор зарегестрирован✅', reply_markup=markup)
    else:
        await bot.send_message(message.from_user.id, '⛔Вы не являетесь администратором⛔')

@dp.message_handler(commands=['ban'], state=None)
async def command_ban(message: types.Message):
    if int(message.from_user.id) == admin_id:
        markup = types.InlineKeyboardMarkup(row_width=1)
        add_ban_user_button = types.InlineKeyboardButton('➕Добавить пользователя в список забаненных➕', callback_data='add_ban_users')
        exxxxxxxxxxit_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
        markup.add(add_ban_user_button, exxxxxxxxxxit_button)

        await bot.send_message(message.from_user.id, '✅Администратор зарегестрирован✅', reply_markup=markup)
    else:
        await bot.send_message(message.from_user.id, '⛔Вы не являетесь администратором⛔')

class Btc_ass(StatesGroup):
    reception = State()

class account_spotify_add(StatesGroup):
    spotify_add_account = State()

class account_youtube_add(StatesGroup):
    youtube_add_account = State()

class account_game_add(StatesGroup):
    game_add_account = State()

class meiling_state(StatesGroup):
    photo_meiling_state = State()
    text_meiling_state = State()

class ban_user_add_states(StatesGroup):
    ban_user_add = State()

@dp.message_handler(state=None)
async def keybord_hendler(message: types.Message):
    if message.from_user.username is None:
        await bot.send_message(message.from_user.id, '⛔<b>Внимание!</b> чтобы пользоваться данным ботом, вы должны иметь <b>тег</b>⛔', parse_mode='html')
    else:
        connect = sqlite3.connect('ban_users.bd')
        cursor = connect.cursor()

        cursor.execute(f"SELECT ban_user_id FROM ban_users WHERE ban_user_id = {message.from_user.id}")
        data_ban = cursor.fetchone()
        connect.commit()
        if data_ban is None:
            if message.text == 'Выход':
                await message.delete()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                box_button = types.KeyboardButton('🗃Коробка')
                acc_button = types.KeyboardButton('💈Бесплатные аккаунты')
                BTC_obnal_button = types.KeyboardButton('📋Как вывести деньги с BTC банкир')
                bot_info_button = types.KeyboardButton('📋Информация о боте')
                markup.add(box_button, acc_button, BTC_obnal_button, bot_info_button)

                await bot.send_message(message.from_user.id, 'Вы вышли в главное меню', reply_markup=markup)
            elif message.text == '🗃Коробка':
                await message.delete()
                markup = types.InlineKeyboardMarkup(row_width=1)
                BTC_check_button = types.InlineKeyboardButton('💸Получить чек💸', callback_data='BTC_check')
                exit_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
                markup.add(BTC_check_button, exit_button)

                await bot.send_message(message.from_user.id, '🔰Нажми чтобы получить чек🔰', reply_markup=markup)
            elif message.text == '💈Бесплатные аккаунты':
                await message.delete()
                markup = types.InlineKeyboardMarkup(row_width=1)
                spotify_button = types.InlineKeyboardButton('🎧Spotify Premium🎧', callback_data='spotify_premium_hendler')
                youtube_button = types.InlineKeyboardButton('📽YouTube Premium📽', callback_data='youtube_premium_hendler')
                game_button = types.InlineKeyboardButton('🎮Аккаунты с Играми🎮', callback_data='game_acc_hendler')
                exit_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
                markup.add(spotify_button, youtube_button, game_button, exit_button)

                await bot.send_message(message.from_user.id, '🔰Выберите категорию🔰', reply_markup=markup)
            elif message.text == '📋Как вывести деньги с BTC банкир':
                await message.delete()
                markup = types.InlineKeyboardMarkup(row_width=1)
                exiittt_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
                markup.add(exiittt_button)

                await bot.send_message(message.from_user.id, 'https://telegra.ph/Kak-vyvesti-dengi-s-BTC-bankir-08-21\n\nВот моя статься на эту тему', reply_markup=markup)
            elif message.text == '📋Информация о боте':
                connect = sqlite3.connect('users_info.bd')
                cursor = connect.cursor()

                cursor.execute("SELECT COUNT (user_id) FROM users_info")
                lines = cursor.fetchone()

                markup = types.InlineKeyboardMarkup(row_width=1)
                es_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
                markup.add(es_button)

                await bot.send_message(message.from_user.id, f'В боте всего {lines[0]} пользователей👥\n\nАдминистратор проекта - @SPICERMr', reply_markup=markup)
                await message.delete()
            if int(message.from_user.id) == admin_id:
                if message.text == '➕Добавить BTC чек':
                    await message.delete()
                    await bot.send_message(message.from_user.id, 'Для добавления отправьте мне BTC чек, чтобы отменить действие напишите -')

                    await Btc_ass.reception.set()
                elif message.text == '➕Добавить бесплатные аккаунты':
                    await message.delete()
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    spotify_add = types.InlineKeyboardButton('🎧Добавить Spotify Premium🎧', callback_data='add_spotify_premium')
                    youtube_add = types.InlineKeyboardButton('📽Добавить YouTube Premium📽', callback_data='add_youtube_premium')
                    game_add = types.InlineKeyboardButton('🎮Добавить Аккаунты с Играми🎮', callback_data='add_game_acc')
                    exiiiit_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
                    markup.add(spotify_add, youtube_add, game_add, exiiiit_button)

                    await bot.send_message(message.from_user.id, 'Выберите что вы хотите добавить?', reply_markup=markup)
                elif message.text == '📣Запусить рассылку':
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    Photo_meiling_button = types.InlineKeyboardButton('📷Рассылка с фото📷', callback_data='photo_meiling')
                    Text_meiling_button = types.InlineKeyboardButton('📝Текстовая рассылка', callback_data='text_meiling')
                    exxxxit_button = types.InlineKeyboardButton('💢Выход💢', callback_data='exit_inline_button')
                    markup.add(Photo_meiling_button, Text_meiling_button, exxxxit_button)

                    await bot.send_message(message.from_user.id, '🔰Выберите способ рассылки🔰', reply_markup=markup)
                    await message.delete()
        else:
            await bot.send_message(message.from_user.id, 'Внимание! Вы забанены администратором!')

@dp.callback_query_handler(lambda c: c.data == 'add_ban_users', state=None)
async def add_ba_users_hendler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Отправьте тег пользователя, которого хотите забанить, для отмены действия напиште -')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await ban_user_add_states.ban_user_add.set()

@dp.message_handler(state=ban_user_add_states.ban_user_add)
async def bab(message: types.Message, state: FSMContext):
    ban_user_teg = message.text
    if ban_user_teg == '-':
        await bot.send_message(message.from_user.id, '❌Действие отменено❌')
        await state.finish()
    else:
        connect = sqlite3.connect('users_info.bd')
        cursor = connect.cursor()

        cursor.execute("SELECT user_id FROM users_info WHERE user_teg = ?", (ban_user_teg,))
        ban_user_id = cursor.fetchone()
        if ban_user_id is None:
            await bot.send_message(admin_id, '⛔️Внимание! Данный пользователь уже забанен, или такового просто нету⛔️')
        else:
            cursor.execute("DELETE FROM users_info WHERE user_id = ?", (ban_user_id[0],))
            connect.commit()

            connect = sqlite3.connect('ban_users.bd')
            cursor = connect.cursor()

            cursor.execute(f"SELECT ban_user_id FROM ban_users WHERE ban_user_id = {ban_user_id[0]}")
            data = cursor.fetchone()

            if data is None:
                ban_user_info = [ban_user_id[0], ban_user_teg]
                print(ban_user_info)
                cursor.execute("INSERT INTO ban_users VALUES(?,?)", ban_user_info)
                connect.commit()
                await bot.send_message(admin_id, '✅Пользователь упешно забанен✅')
                
                await state.finish()
            else:
                pass

@dp.callback_query_handler(lambda c: c.data == 'text_meiling', state=None)
async def text_mailing(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Отправьте текс рассылки, для отмены напишите -')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await meiling_state.text_meiling_state.set()

@dp.message_handler(state=meiling_state.text_meiling_state)
async def text_meiling_hendler(message: types.Message, state: FSMContext):
    mailing_text = message.text
    if mailing_text == '-':
        await message.answer('Действие отменено')
        await state.finish()
    else:
        connect = sqlite3.connect('users_info.bd')
        cursor = connect.cursor()

        cursor.execute("SELECT user_id FROM users_info")
        all_users_id = cursor.fetchall()
        connect.commit()

        await bot.send_message(admin_id, '✅Рассылка начата✅')

        for i in range(len(all_users_id)):
            try:
                time.sleep(1)
                await bot.send_message(all_users_id[i][0], mailing_text)
            except:
                pass

        await bot.send_message(admin_id, '✅Рассылка завершена✅')

        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'photo_meiling', state=None)
async def photo_meiling(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Отправьте мне фото, для отмены напишите -')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await meiling_state.photo_meiling_state.set()


@dp.message_handler(content_types=['photo'], state=meiling_state.photo_meiling_state)
async def photo_meiling_hendler(message: types.Message, state: FSMContext):
    sent_message = message.text
    if sent_message == '-':
        await message.answer('Действие отменено!')
        await state.finish()
    else:
        photo_id = message.photo[-1].file_id
        file_photo = await bot.get_file(photo_id)
        photo_name, photo_extension = os.path.splitext(file_photo.file_path)

        downloaded_photo = await bot.download_file(file_photo.file_path)

        src = 'Photo/' + photo_id + photo_extension
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_photo.getvalue())
        await bot.send_message(message.chat.id, 'Отправьте текст для рассылки')

        async with state.proxy() as data:
            data['photo_id'] = photo_id
            data['photo_extension'] = photo_extension

        await meiling_state.text_meiling_state.set()

@dp.message_handler(state=meiling_state.text_meiling_state)
async def text_meiling_state(message: types.Message, state: FSMContext):
    mailing_text = message.text
    connect = sqlite3.connect('users_info.bd')
    cursor = connect.cursor()

    cursor.execute("SELECT user_id FROM users_info")
    all_users_id = cursor.fetchall()
    connect.commit()

    await bot.send_message(admin_id, '✅Рассылка начата✅')

    for i in range(len(all_users_id)):
        try:
            time.sleep(1)
            data=await state.get_data()
            photo_id = data.get("photo_id")
            photo_extension = data.get("photo_extension")
            photo_path = 'Photo/' + photo_id + photo_extension
            photo = open(photo_path, 'rb')
            await bot.send_photo(all_users_id[i][0], photo, caption=mailing_text)
        except:
            pass
    await bot.send_message(admin_id, '✅Рассылка зевершена✅')

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'add_game_acc')
async def add_you(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите данные от аккаунта ввиде логин:пароль, для отмены напишите -')
    await account_game_add.game_add_account.set()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.message_handler(state=account_game_add.game_add_account)
async def add_game(message: types.Message, state: FSMContext):
    acc = message.text
    if acc == '-':
        await bot.send_message(message.from_user.id, '❌Добавление Игрового аккаунта отменено❌')
        await state.finish()
    else:
        connect = sqlite3.connect('products_list.bd')
        cursor = connect.cursor()

        cursor.execute("INSERT INTO game_acc VALUES(?)", (acc,))
        connect.commit()
        await bot.send_message(admin_id, '✅Игровой аккаунт успешно добавлен✅')

        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'add_youtube_premium')
async def add_you(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите данные от аккаунта ввиде логин:пароль, для отмены напишите -')
    await account_youtube_add.youtube_add_account.set()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.message_handler(state=account_youtube_add.youtube_add_account)
async def aff_acc_you(message: types.Message, state: FSMContext):
    acc = message.text
    if acc == '-':
        await bot.send_message(message.from_user.id, '❌Добавление YouTube аккаунта отменено❌')
        await state.finish()
    else:
        connect = sqlite3.connect('products_list.bd')
        cursor = connect.cursor()

        cursor.execute("INSERT INTO youtube_acc VALUES(?)", (acc,))
        connect.commit()
        await bot.send_message(admin_id, '✅YouTube аккаунт успешно добавлен✅')

        await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'add_spotify_premium')
async def add_spott(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите данные от аккаунта ввиде логин:пароль, для отмены напишите -')
    await account_spotify_add.spotify_add_account.set()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.message_handler(state=account_spotify_add.spotify_add_account)
async def add_account_spot(message: types.Message, state: FSMContext):
    acc = message.text
    if acc == '-':
        await bot.send_message(message.from_user.id, '❌Добавление Spotify аккаунта отменено❌')
        await state.finish()
    else:
        connect = sqlite3.connect('products_list.bd')
        cursor = connect.cursor()

        cursor.execute("INSERT INTO spotify_acc VALUES(?)", (acc,))
        connect.commit()
        await bot.send_message(admin_id, '✅Spotify аккаунт успешно добавлен✅')

        await state.finish()


@dp.message_handler(state=Btc_ass.reception)
async def btc_check_save(message: types.Message, state: FSMContext):
    btc_check = message.text
    if btc_check == '-':
        await message.reply('❌Добавление чека отменено❌')
        await state.finish()
    else:
        connect = sqlite3.connect('btc_checks.bd')
        cursor = connect.cursor()

        cursor.execute("INSERT INTO btc_checks VALUES(?)", (btc_check,))
        connect.commit()
        await bot.send_message(admin_id, '✅Чек успешно добавлен✅')

        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'game_acc_hendler', state=None)
async def game_acc_hendler(callback_query: types.CallbackQuery):
    connect = sqlite3.connect('products_list.bd')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM game_acc")
    game_acc = cursor.fetchone()

    connect.commit()

    if game_acc is None:
        await bot.answer_callback_query(callback_query.id, '☹️Увы, аккаунтов пока нет☹️')
    else:
        await bot.send_message(callback_query.from_user.id, f'{game_acc[0]} вид логин:пароль')

        connect = sqlite3.connect('products_list.bd')
        cursor = connect.cursor()

        cursor.execute("DELETE FROM game_acc WHERE login_pass = ?", (game_acc[0],))
        connect.commit()

        preser_teg = callback_query.from_user.username
        await bot.send_message(admin_id, f'@{preser_teg} забрал игровой аккаунт!')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'youtube_premium_hendler', state=None)
async def youtube_premium_hendler(callback_query: types.CallbackQuery):
    connect = sqlite3.connect('products_list.bd')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM youtube_acc")
    youtube_acc = cursor.fetchone()

    connect.commit()

    if youtube_acc is None:
        await bot.answer_callback_query(callback_query.id, '☹️Увы, аккаунтов пока нет☹️')
    else:
        await bot.send_message(callback_query.from_user.id, f'{youtube_acc[0]} вид логин:пароль')
        connect = sqlite3.connect('products_list.bd')
        cursor = connect.cursor()

        cursor.execute("DELETE FROM youtube_acc WHERE login_pass = ?", (youtube_acc[0],))

        connect.commit()

        preser_teg = callback_query.from_user.username
        await bot.send_message(admin_id, f'@{preser_teg} забрал аккаунт YouTube Premium!')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'spotify_premium_hendler', state=None)
async def spotify_premium_hendler(callback_query: types.CallbackQuery):
    connect = sqlite3.connect('products_list.bd')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM spotify_acc")
    spotify_acc = cursor.fetchone()
    connect.commit()

    if spotify_acc is None:
        await bot.answer_callback_query(callback_query.id, text='☹️Увы, аккаунтов пока нет☹️')
    else:
        await bot.send_message(callback_query.from_user.id, f'{spotify_acc[0]} вид логин:пароль')

        connect = sqlite3.connect('products_list.bd')
        cursor = connect.cursor()

        cursor.execute("DELETE FROM spotify_acc WHERE login_pass = ?", (spotify_acc[0],))

        connect.commit()

        preser_teg = callback_query.from_user.username

        await bot.send_message(admin_id, f'@{preser_teg} забрал аккаунт Spotify Premium!')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'exit_inline_button')
async def exit_button_hendler_inline(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'BTC_check')
async def BTC_check_hendler(callback_query: types.CallbackQuery):
    connect = sqlite3.connect('btc_checks.bd')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM btc_checks")
    btc_check = cursor.fetchone()

    connect.commit()

    if btc_check is None:
        await bot.answer_callback_query(callback_query.id, text='☹️Увы, чеков пока нет☹️')
    else:
        await bot.send_message(callback_query.from_user.id, btc_check)

        connect = sqlite3.connect('btc_checks.bd')
        cursor = connect.cursor()

        cursor.execute("""DELETE FROM btc_checks""")

        connect.commit()

        btc_winner = callback_query.from_user.username

        await bot.send_message(admin_id, f'@{btc_winner} забрал BTC чек!')
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp)
