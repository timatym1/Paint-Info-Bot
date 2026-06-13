import asyncio
from aiogram import Bot, Dispatcher, types
from google import genai
from google.genai.errors import APIError

TELEGRAM_BOT_TOKEN = "token"
GEMINI_API_KEY = "token"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = ("Prompt example")

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    for attempt in range(2):
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\nВопрос пользователя: {user_text}"
            
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt
            )
            
            ai_answer = response.text
            ai_answer = ai_answer.replace("**", "").replace("*", "").replace("#", "").replace("_", "")
            
            await message.answer(ai_answer)
            return

        except APIError as e:
            if attempt == 0:
                await asyncio.sleep(2)
                continue
            print(f"[КРИТИЧЕСКАЯ ОШИБКА В КОДЕ]: {e}")
            await message.answer("Извините, сервер ИИ сейчас перегружен. Пожалуйста, попробуйте повторить ваш вопрос через минуту.")
            return
            
        except Exception as e:
            print(f"[ДРУГАЯ ОШИБКА]: {e}")
            await message.answer("Извините, произошла непредвиденная техническая ошибка")
            return

async def main():
    print("БОТ ЗАПУЩЕН")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
