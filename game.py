from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from game_states import GameStates
import random

game_router = Router()

ATTEMPTS_LIMIT = 7

# handler /cancel
@game_router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == GameStates.game_in_progress:
        await state.set_state(None)
        await message.answer("Exit. If you want to play again, I'll be waiting for you!\nJust send me a message!")
    else:
        await message.answer("We aren't playing now! If you want to play, just send me a message!")

# Refuse to play
@game_router.message(F.text.lower().in_(["no", "i don't want", "exit", "stop"]))
async def process_exit(message: Message, state: FSMContext):
    await message.answer("Ok, maybe next time!")
    #await state.clear()
    return

# Agree to play
@game_router.message(F.text.lower().in_(["yes", "let's go" , "go", "sure", "play"]))
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
@game_router.message(GameStates.game_in_progress, F.text.isdigit())
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