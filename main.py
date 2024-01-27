import asyncio
import logging
import os
import shutil
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
import config
import check
import patoolib
import time
import test_archivation


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text=f"Hello, {message.from_user.full_name}")


@dp.message(Command("help"))
async def hamdle_help(message: types.Message):
    text = "I,m and echo bot.\nSend me any message!"
    await message.answer(text=text)


@dp.message()
async def download_document(message: types.Message):
    file_info = await bot.get_file(message.document.file_id)
    file_path = file_info.file_path

    file = await bot.download_file(file_path)

    # сохранение файла
    archive_received_from_the_user = message.document.file_name
    with open(archive_received_from_the_user, 'wb') as new_file:
        new_file.write(file.getvalue())

    await message.reply(f"File {archive_received_from_the_user} has been downloaded")

    path = 'cookies_json//'
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    # Разархивация файла
    patoolib.extract_archive(f"{archive_received_from_the_user}", outdir=f"Cookies//")

    time.sleep(5)
    file_name_without_extension = archive_received_from_the_user.split(".")[0]

    # Get the list of all files and directories
    pathc = "Cookies//"

    dir_list = os.listdir(pathc + file_name_without_extension)



    # Конвертация файла в нужный формат
    await message.answer("Convertation...")
    print("TASK STARTED...")

    for h in dir_list:
        print("new file", h)
        check.netscape_to_json(h, path, file_name_without_extension)

    print("TASK COMPLETED...")

    # Архивация папки в нужном формате
    test_archivation.archivation()

    # Отправление архива пользователю
    try:
        file_path = "Cookies_json.zip"
        await message.reply_document(
            document=types.FSInputFile(
                path=file_path,
                filename="Cookies_json.zip"
            )
        )
    except Exception as ex:
        print(ex)
        await message.answer("Convertation is failed, please try again!")
    finally:
        # Удаление архива, который был получен от пользователя
        if archive_received_from_the_user:
            os.remove(archive_received_from_the_user)
        if os.path.exists("Cookies//"):
            shutil.rmtree("Cookies//")
        if os.path.exists("cookies_json//"):
            shutil.rmtree("cookies_json//")
        if os.path.exists("Cookies_json.zip"):
            os.remove("Cookies_json.zip")






async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
