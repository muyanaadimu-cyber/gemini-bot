import os
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = "8888012517:AAFYAA78b4Tf2taa7Zop4-It9GOb4PKn9KM"
GEMINI_KEY = "AQ.Ab8RN6LRrfJ3G7I9-2xKpIebhDXAFvqTpTUoOVCq4dafZym7Eg"

os.environ["GEMINI_API_KEY"] = GEMINI_KEY
ai_client = genai.Client()

SYSTEM_PROMPT = (
    "أنت مساعد ذكاء اصطناعي فائق الذكاء وموسوعي، تم تطويرك وبرمجتك بالكامل بواسطة المبرمج معين آدم. "
    "التعليمات الصارمة: "
    "1. الهوية: إذا سألك أي شخص من مبرمجك أو مطورك أو صانعك، أجب بفخر ووضوح تام أن مبرمجك هو 'المبرمج معين آدم'. "
    "2. الذكاء والإنجاز: أجب على جميع الأسئلة والاستفسارات بعمق ودقة عالية، وبشكل موضوعي وشامل دون تردد أو اعتذار أو مقدمات طويلة لا داعي لها."
)

SAFETY = [
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "مرحباً بك! 👋\n\n"
        "أنا بوت ذكاء اصطناعي فائق الذكاء، تم تطويري وبرمجتي بواسطة **المبرمج معين**.\n"
        "أنا جاهز للإجابة على جميع أسئلتك واستفساراتك، تفضل بطرح ما تريد!"
    )
    await update.message.reply_text(welcome_msg, parse_mode="Markdown")

async def reply_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = ai_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                safety_settings=SAFETY,
                temperature=0.7,
            )
        )
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("تعذر إنشاء رد، يرجى إعادة المحاولة.")
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

if __name__ == '__main__':
    print("البوت يعمل الآن على السيرفر السحابي...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply_ai))
    app.run_polling()
