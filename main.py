import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cours_info import COURSE_PROGRAMMING_BASICS, COURSE_PYTHON_BASICS, courses

# Логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота і диспетчера
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

course_selection = int(0)

channel_names = ['https://t.me/Kh_Sergii']
channel_invite_link = 'https://t.me/+gANNq7WHXUlhOTU6'  # Замініть на посилання на ваш канал


# Ціна за курс
PRICE_1 = LabeledPrice(label="Курс 1", amount=1000 * 100)  # 1000 грн
PRICE_2 = LabeledPrice(label="Курс 2", amount=1500 * 100)  # 1500 грн




# Стартове повідомлення
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Зробіть свій вибір..."
    )
    keyboard.row(types.KeyboardButton(text="🔁 Почати заново"))
    keyboard.row(
        types.KeyboardButton(text="📖 Курс 1"),
        types.KeyboardButton(text="📚 Курс 2")
    )
    keyboard.row(types.KeyboardButton("🆘 Підтримка"))

 
    # Відправляємо привітання і кнопки                  
    await message.answer( f"Привіт, {message.from_user.first_name} ! Цей бот допоможе тобі зробити оплату за курс.\n"
                         "<u>Оберіть один із курсів:</u>\n\n"
                         "<b>Курс 1: Основи програмування 💻</b>\n"
                         "<b>Курс 2: Основи Python 🐍</b>", parse_mode='HTML', reply_markup=keyboard)





@dp.message_handler(lambda message: message.text == "🔁 Почати заново")
async def repit(message: types.Message):
     # Відправляємо привітання і кнопки
    await message.answer("Привіт! Цей бот допоможе тобі зробити оплату за курс.\n"
                         "<u>Оберіть один із курсів:</u>\n\n"
                         "<b>Курс 1: Основи програмування 💻</b>\n"
                         "<b>Курс 2: Основи Python 🐍</b>", parse_mode='HTML')



# Обробник для Курс 1

@dp.message_handler(lambda message: message.text == "📖 Курс 1")
async def show_course_1_info(message: types.Message):
    # Отримуємо інформацію про курс з основ програмування
    course_info = COURSE_PROGRAMMING_BASICS
    topics_list = '\n'.join(course_info["topics"])

    global course_selection
    course_selection = 2

    # Виводимо інформацію про курс
    # Форматування тексту
    await message.answer(f"<b>{course_info['name']}</b>\n\n"
                        f"{course_info['description']}\n\n"
                        f"<u>Базові теми курсу:</u>\n{topics_list}", parse_mode='HTML')
    
    # Відправляємо зображення, яке характеризує програмування
    await bot.send_photo(message.chat.id, photo=course_info['image_url'])
    
    # Відправляємо кнопку для оплати за курс
    await send_invoice_for_course_1(message)




# Обробник для Курс 2

@dp.message_handler(lambda message: message.text == "📚 Курс 2")
async def show_course_2_info(message: types.Message):
    # Отримуємо інформацію про курс з основ програмування
    course_info = COURSE_PYTHON_BASICS
    topics_list = '\n'.join(course_info["topics"])

    global course_selection
    course_selection = 2

    # Виводимо інформацію про курс
    # Форматування тексту
    await message.answer(f"<b>{course_info['name']}</b>\n\n"
                        f"{course_info['description']}\n\n"
                        f"<u>Базові теми курсу:</u>\n{topics_list}", parse_mode='HTML')
    
    # Відправляємо зображення, яке характеризує програмування
    await bot.send_photo(message.chat.id, photo=course_info['image_url'])

    # Відправляємо кнопку для оплати за курс
    await send_invoice_for_course_2(message)




# Функція для надсилання інвойсу за Курс 1
async def send_invoice_for_course_1(message: types.Message):

    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Придбати - Основи програмування 💻: 1000грн', url="https://prt.mn/qxnf_m7X-H")
    inline_kb.add(inline_btn)

    await message.answer("<b>Для того щоб оплатити курс, будь ласка, натисни на кнопку нижче.\n"
                        "Після успішної оплати, зроби скріншот або фото квитанції та надішли його сюди, у наш чат-бот.\n\n"
                        "<i>Дякуємо за твою довіру та бажаємо успіху у навчанні!</i></b> "
                         , parse_mode='HTML', reply_markup=inline_kb)



# Функція для надсилання інвойсу за Курс 2
async def send_invoice_for_course_2(message: types.Message):

    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Придбати - Основи Python 🐍: 1000грн', url="https://prt.mn/qxnf_m7X-H")
    inline_kb.add(inline_btn)

    
    await message.answer("<b>Для того щоб оплатити курс, будь ласка, натисни на кнопку нижче.\n"
                        "Після успішної оплати, зроби скріншот або фото квитанції та надішли його сюди, у наш чат-бот.\n\n"
                        "<i>Дякуємо за твою довіру та бажаємо успіху у навчанні!</i></b> "
                         , parse_mode='HTML', reply_markup=inline_kb)






@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    user_id = message.from_user.id

    name_course = ""
    chat_id = ""
    invite_link = ""

    if course_selection in courses:
        name_course, chat_id = courses[course_selection]
        invite_link = channel_invite_link  # Генеруємо посилання на канал

    try:
        # Відправте запит на додавання користувача до каналу за посиланням
        invite_kb = InlineKeyboardMarkup()
        invite_btn = InlineKeyboardButton(name_course, url=invite_link)
        invite_kb.add(invite_btn)

        await message.answer(
            f"{message.from_user.first_name} Перейдіть за посиланням та надішліть запит для вступу. \n"
            "<b>Запрошення на вступ до групи дійсне одну годину !</b>",
            parse_mode='HTML', reply_markup=invite_kb
        )

        await message.answer(
            "<u>Як тільки вас додадуть, ви отримаєте сповіщення через цей Телеграм - Бот.</u>",
            parse_mode='HTML'
        )


        # Запускаємо перевірку на приєднання до каналу
        asyncio.create_task(periodic_membership_check(user_id, chat_id))

        my_user_id = 5867537861

        # посилання на профіль користувача
        username = message.from_user.username
        if username:
            profile_link = f"[@{username}](https://t.me/{username})"
        else:
            profile_link = "Користувач без ім'я користувача"
        await bot.send_message(my_user_id,
                               f"{message.from_user.first_name} {message.from_user.last_name}.\nПосилання на профіль: {profile_link}\n"
                               f"ID: {message.from_user.id}\n[>{name_course}<]")

        # фотографію користувача
        photo = message.photo[-1]  # Останнє (найвища якість) зображення зі списку

        await bot.send_photo(chat_id=my_user_id, photo=photo.file_id)


    except Exception as e:
        logging.exception("Помилка після успішного платежу", e)
        await bot.send_message(user_id, "Виникла помилка після успішного платежу. Спробуйте пізніше.")







@dp.message_handler(lambda message: message.text == "🆘 Підтримка")
async def help_handler(message: types.Message):
    inline_kb = types.InlineKeyboardMarkup()
    inline_btn = types.InlineKeyboardButton('Зв\'язок з адміністратором', url='https://t.me/SKh_telegram')
    inline_kb.add(inline_btn)

    await message.answer(f"Привіт, {message.from_user.first_name}, "
                        "для отримання консультації, перейди за посиланням до чату:",
                         reply_markup=inline_kb)






# Функція для перевірки статусу користувача
async def check_user_membership(user_id, chat_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if chat_member.status == 'member':
            # Якщо користувач став членом каналу
            await bot.send_message(user_id, "Ви успішно приєдналися до каналу!")
            return True  # Повідомляємо, що користувач був доданий
        else:
            return False  # Користувач ще не приєднався
    except Exception as e:
        logging.error(f"Помилка при перевірці членства: {e}")
        return False




# Функція для періодичної перевірки:
async def periodic_membership_check(user_id, chat_id, timeout=600):
    # Час для перевірки (в секундах)
    check_interval = 30
    elapsed_time = 0

    while elapsed_time < timeout:
        if await check_user_membership(user_id, chat_id):
            break  # Виходимо з циклу, якщо користувач доданий до каналу
        await asyncio.sleep(check_interval)  # Чекаємо перед наступною перевіркою
        elapsed_time += check_interval

    if elapsed_time >= timeout:
        await bot.send_message(user_id, "Час на приєднання до каналу закінчився.")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
