from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text,IDFilter

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Виберіть що ви зочете замовити, напої (/drinks) чи їжу (/food)', reply_markup=types.ReplyKeyboardRemove)

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Дію відсінено', reply_markup=types.ReplyKeyboardRemove)

def registr_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals='відміна', ignore_case=True), state='*')