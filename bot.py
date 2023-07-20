from aiogram import Bot
from aiogram.types import *
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from database import create_tasks_table
from models import Task
from config import TOKEN




bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    reply_text = "Здравствуйте! Я бот для управления списком задач. Мои команды:\n" \
                 "/add <задача> - добавление новой задачи\n" \
                 "/done <индекс> - отметка задачи как выполненной\n" \
                 "/list - вывод списка задач\n" \
                 "/delete <индекс> - удаление задачи\n"
    await message.reply(reply_text)


@dp.message_handler(commands=["add"])
async def add_task_command(message: Message):
    ''' Получаем задачу после команды "/add " '''     
    task_text = message.text[5:].strip() 
    if not task_text:   
        await message.reply('Укажите задачу после комманды /add')
        return
    
    task = Task(task_text, "", "невыполнена")
    task.save()
    await message.reply("Задача успешно добавлена!")


@dp.message_handler(commands=["done"])
async def done_command(message: Message):
    '''Получаем индекс задачи после команды "/done "'''
    task_id = int(message.text[6:]) 
    tasks = Task.get_all()

    if task_id < 1 or task_id > len(tasks):
        await message.reply("Укажите номер задачи из списка после комманды /done")
        return

    task = tasks[task_id - 1]
    Task.mark_as_done(task_id)
    await message.reply(f"Задача '{task.title}' выполнено!")


@dp.message_handler(commands=["list"])
async def list_command(message: Message):
    ''' эта комманда показывает все задачи'''
    tasks = Task.get_all()

    if not tasks:
        await message.reply("Список задач пуст!")
        return

    reply_text = "Список задач:\n"
    for i, task in enumerate(tasks):
        status = "✅" if task.status == "выполнена" else "❌"
        reply_text += f"{i + 1}. {status} {task.title}\n"

    await message.reply(reply_text)


@dp.message_handler(commands=["delete"])
async def delete_command(message: Message):
    '''удаляем по индексу задачи после команды "/delete "'''
    task_id = int(message.text[8:])  
    tasks = Task.get_all()

    if task_id < 1 or task_id > len(tasks):
        await message.reply("Некорректный индекс задачи!")
        return

    task = tasks[task_id - 1]
    Task.delete(task_id)
    await message.reply(f"Задача '{task.title}' удалена!")


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_command(message: Message):
    await message.reply("Неизвестная команда. Введите /help для получения списка команд.")


if __name__ == '__main__':
    create_tasks_table()
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass