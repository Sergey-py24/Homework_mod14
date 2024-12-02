from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio





api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Старт')
button2 = KeyboardButton(text='Инфо')
button3 = KeyboardButton(text='Мои калории')
button4 = KeyboardButton(text='Приобрести')
kb.add(button)
kb.row(button2, button3, button4)
ikb = InlineKeyboardMarkup()
button5 = InlineKeyboardButton(text='Формула', callback_data='формула')
button6 = InlineKeyboardButton(text='Расчет', callback_data='Мои калории')
ikb.add(button5, button6)
ikb1 = InlineKeyboardMarkup()
button7 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
button9 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
button10 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
ikb1.add(button7, button8, button9, button10)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Приобрести')
async def get_buying_list(message):
    for i in range(1, 5):
        with open('Продукт.jpg', 'rb') as image:
            await message.answer_photo(image, f'Название:Продукт {i} | Описание:Описание {i} | Цена:{i*100}')
    await message.answer('Выберите продукт для покупки.', reply_markup=ikb1)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='Мои калории')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    clr = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'{message.from_user.first_name}, ваша норма калорий - {clr}.')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f"Приветствуем вас,{message.from_user.first_name} {message.from_user.last_name}!"
                         ,reply_markup = kb)

@dp.message_handler(text='Мои калории')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = ikb)

@dp.callback_query_handler(text='формула')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.message.answer('для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.message_handler(text="Инфо")
async def inform(message):
    await message.answer('Я бот,помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(message):
    await message.answer('Доброго времени суток!'
                         'Введите команду /start, чтобы начать общение')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
