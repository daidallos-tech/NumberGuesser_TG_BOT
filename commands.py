from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from game_states import GameStates


user_router = Router()

# Handler /start - start bot
@user_router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer("Hello! Let's play a game!🎮\nI'm going to imagine number🎲\nAnd you going to guess this one")

# Handler /help - FAQ and rules 
@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer("The Rules:\nI guess the number from 1 to 100!\nYou have 7 attempts to guess number I guessed\nIf you do it - you'll win.\n/start - restart bot\n/help - about game and commands\n/stat - your statistic\n/cancel - to stop game in game\nIf you want to play just type 'Start', 'Go', 'Play'\nTo exit just type 'Exit', 'No', 'Stop' - in game type - /cancel")

# Handler /stat - Game statistic
@user_router.message(Command(commands='stat'))
async def process_stat_command(message: Message, state: FSMContext):
    user_data = await state.get_data()
    print(f"Debug data in commands.py: {user_data}")
    total = user_data.get('total_games', 0)
    wins = user_data.get('wins', 0)

    await message.answer(
        f"Total played💯: {total}\nWins🏆: {wins}"
    )

# Handler for other messages
@user_router.message()
async def process_any_message(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == GameStates.game_in_progress:
        await message.answer("We are playing🕹️! Sent me a number from 1 to 100!")
    else:
        await message.answer("I just can play🕹️! My boss don't allow me to speak with other people!😄")