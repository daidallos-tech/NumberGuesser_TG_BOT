from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import random

BOT_TOKEN = "YOUR_TOKEN_BOT"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS_LIMIT = 5

class GameStates(StatesGroup):
    game_in_progress = State()

# Handler /start - start bot
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer("Hello! Let's play a game!\nI'm going to imagine number\nAnd you going to guess this one")

# Handler /help - FAQ and rules 
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer("The Rules:\nI guess the number from 1 to 100!\nYou have 5 attempts to guess number I guessed\nIf you do it - you'll win.")

# Handler /stat - Game statistic
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message, state: FSMContext):
    user_data = await state.get_data()
    total = user_data.get('total_games', 0)
    wins = user_data.get('wins', 0)

    await message.answer(
        f"Total played: {total}\nWins: {wins}"
    )

# handler /cancel
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == GameStates.game_in_progress:
        await state.set_state(None)
        await message.answer("Exit. If you want to play again, I'll be waiting for you!\nJust send me a message!")
    else:
        await message.answer("We aren't playing now! If you want to play, just send me a message!")

# Refuse to play
@dp.message(F.text.lower().in_(["no", "i don't want", "exit", "stop"]))
async def process_exit(message: Message, state: FSMContext):
    await message.answer("Ok, maybe next time!")
    await state.clear()
    return

# Agree to play
@dp.message(F.text.lower().in_(["yes", "let's go" , "go", "sure", "play"]))
async def process_start(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state != GameStates.game_in_progress:
        user_data = await state.get_data()
        total_games = user_data.get('total_games', 0)
        wins = user_data.get('wins', 0)

        await state.update_data(
            secret_number=random.randint(1, 100),
            attempts=ATTEMPTS_LIMIT,
            total_games=total_games,
            wins=wins
        )

        await state.set_state(GameStates.game_in_progress)
        await message.answer("I guessed a number from 1 to 100! Try to guess!")
    else:
        await message.answer("We are playing! Try to guess sent me a number!")

# Game process 
@dp.message(GameStates.game_in_progress, lambda message: message.text and message.text.isdigit())
async def process_numbers_answer(message: Message, state: FSMContext):
    assert message.text is not None
    user_guess = int(message.text)
    
    if not (1 <= user_guess <= 100):
        await message.answer('Enter a number from 1 to 100!')
        return

    user_data = await state.get_data()
    secret_number = user_data.get('secret_number', 0)
    attempts = user_data.get('attempts', ATTEMPTS_LIMIT) - 1
    total_games = user_data.get('total_games', 0)
    wins = user_data.get('wins', 0)

    if user_guess == secret_number:
        await state.update_data(total_games=total_games + 1, wins=wins + 1)
        await state.set_state(None)
        await message.answer('You right! Maybe, we play again?')
        return

    await state.update_data(attempts=attempts)

    if attempts <= 0:
        await state.update_data(total_games=total_games + 1)
        await state.set_state(None)
        await message.answer(f'You lose all attempts! I guessed a {secret_number}!')
    elif user_guess > secret_number:
        await message.answer(f'My number is less! Attempts: {attempts}')
    else:
        await message.answer(f'My number is bigger! Attempts: {attempts}')

# Handler for other messages
@dp.message()
async def process_any_message(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == GameStates.game_in_progress:
        await message.answer("We are playing! Sent me a number from 1 to 100!")
    else:
        await message.answer("I just can play! My boss don't allow me to speak with other people!")


if __name__ == "__main__":
    dp.run_polling(bot)


# TO DO
# Polish UI and add description rules etc...
# Add README