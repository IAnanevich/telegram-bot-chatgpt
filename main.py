import asyncio
import json
from base64 import b64decode

import openai
from telebot.async_telebot import AsyncTeleBot, types

import settings


bot = AsyncTeleBot(settings.TOKEN)

openai.organization = settings.ORG_ID
openai.api_key = settings.API_KEY


@bot.message_handler(commands=['start'])
async def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Chat with me')
    btn2 = types.KeyboardButton('Generate Image')
    markup.add(btn1, btn2)
    print(f'{message.from_user.username}: {message.text}')
    await bot.send_message(
        message.from_user.id,
        "👋 Hello! I'm a new super duper cool bot with ChatGPT embedded! 🤖 How can I help you? Please push button below."
        "\nYou can write /help to read more about this bot."
        "\nYou can write /info to read more about ChatGPT.",
        reply_markup=markup
    )


@bot.message_handler(commands=['info'])
async def help_me(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Info', url='https://en.wikipedia.org/wiki/ChatGPT')
    markup.add(btn1)
    print(f'{message.from_user.username}: {message.text}')
    await bot.send_message(
        message.from_user.id,
        "Click the button below to go to the site with information",
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
async def help_me(message):
    print(f'{message.from_user.username}: {message.text}')
    await bot.send_message(
        message.from_user.id,
        "This bot can help you answer your questions in any language.",
    )


@bot.message_handler(content_types=['text'])
async def get_text_message(message):
    if message.text == 'Chat with me':
        print(f'{message.from_user.username}: {message.text}')
        await bot.send_message(
            message.from_user.id,
            "How can I help you?",
        )

    elif message.text == 'Generate Image':
        print(f'{message.from_user.username}: {message.text}')
        await bot.send_message(
            message.from_user.id,
            "Please write a text description of the desired image. "
            "You need to start your message with the word 'generate'."
            "\nExample: generate mountains or generate кот",
        )

    elif message.text.split()[0].lower() == 'generate':
        prompt = " ".join(message.text.split()[1:])
        response = await openai.Image.acreate(
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        print(f'{message.from_user.username}: {message.text}')

        await bot.send_photo(message.from_user.id, photo=b64decode(response['data'][0].b64_json), caption=prompt)

    else:
        text = await openai.Completion.acreate(
            engine="text-davinci-003",
            prompt=message.text,
            max_tokens=3600,
            temperature=0.5,
        )
        response = json.loads(json.dumps(text))['choices'][0]['text']
        print(f'{message.from_user.username}: {message.text} - {response}')
        await bot.reply_to(message, response)


asyncio.run(bot.polling(none_stop=True, interval=0))
