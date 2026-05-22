from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import random

BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class GameStates(StatesGroup):
    game_in_progress = State()

@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer("Hello! Let's play a game!\nI'm going to imagine number\nAnd you going to guess this one")

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer("The Rules:\n")

@dp.message(F.text.lower().in_(["no", "i don't want", "exit", "stop"]))
async def process_exit(message: Message, state: FSMContext):
    await message.answer("Ok, maybe next time!")
    await state.clear()
    return

@dp.message(F.text.lower().in_(["yes", "let's go" , "go", "sure", "play"]))
async def process_start(message: Message, state: FSMContext):
    await message.answer("Ok, lets play!")
    random_number = random.randint(1, 100)

    await state.update_data(random_number=random_number, attempts=0)
    await state.set_state(GameStates.game_in_progress)
    await message.answer("I guessed the number from 1 to 100? What is your guess?")

@dp.message(GameStates.game_in_progress)  
async def process_guess(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Enter a number!")
        return
    
    user_guess = int(message.text)
    
    user_data = await state.get_data()
    random_number = user_data.get("random_number", 0)
    attempts = user_data.get("attempts", 0) + 1

    await state.update_data(attempts=attempts)
 
    if user_guess == random_number:
        await message.answer(f"Yeah! You're right! Total attempts: {attempts}")
        await state.clear()
    elif user_guess > random_number:
        await message.answer(f"Nope! Your number is bigger than I guessed! Your attempts: {attempts}")
    else:
         await message.answer(f"Nope! Your number is lesser than I guessed! Your attempts: {attempts}")   


if __name__ == "__main__":
    dp.run_polling(bot)


# TO DO 
# add buttons, polish UI/UX
# give opportunity to user choose how many guess he/she wants
# think about database 
# check with bot from course