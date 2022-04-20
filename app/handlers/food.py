from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

available_food_names = ['суші', 'паста', 'піцца']
available_food_sizes = ['маленька', 'середня', 'велика']

class orderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()

async def food_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await message.answer('Виберіть блюдо: ', reply_markup=keyboard)
    await orderFood.waiting_for_food_name.set()

async def food_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_names:
        await message.answer('Будь-ласка виберіть блюдо завдяки клавіатурі: ')
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)

    await orderFood.next()
    await message.answer('Тепер виберіть розмір: ', reply_markup=keyboard)

async def food_size_start(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_sizes:
        await message.answer('Будь-ласка виберіть порцію завдяки клавіатурі: ')
        return
    user_data = await state.get_data()
    await message.answer(f'Ви замовили {message.text.lower()} порцію {user_data["food_chosen"]}.\n'
                         f'Тепер ви можете вибрати напій: /drinks', reply_markup=types.ReplyKeyboardRemove)
    await state.finish()

def registr_food_handlers(dp: Dispatcher):
    dp.register_message_handler(food_start, commands='food', state='*')
    dp.register_message_handler(food_chosen, state=orderFood.waiting_for_food_name)
    dp.register_message_handler(food_size_start, state=orderFood.waiting_for_food_size)