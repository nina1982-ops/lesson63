# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher import FSMContext
# from  aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# import asyncio
#
# api = '8143181263:AAHYq9di-YxBuZlHf1bP_ddnqmGky_2rovI'
# bot = Bot(token=api)
# dp = Dispatcher(bot, storage=MemoryStorage())
#
# kb = ReplyKeyboardMarkup()
# button_1 = KeyboardButton(text='Информация')
# button_2 = KeyboardButton(text='Начало')
# kb.add(button_1)
# kb.add(button_2)
#
# @dp.message_handler(commands=['start'])
# async def start(message):
#     await message.answer('Привет!', reply_markup=kb)
#
# @dp.message_handler(text='Информация')
# async def inform(message):
#     await message.answer('Информация о боте')


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from  aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button_1)
kb.add(button_2)

@dp.message_handler(commands=['Start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    bmr = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f'Ваша норма калорий: {bmr} ккал. ')
    await state.finish()





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




