import telebot
from openai import OpenAI

# لە جیاتی نیشانەکان، کۆدە راستەقینەکانی خۆت لە نێوان کەوانەکاندا دابنێ
TELEGRAM_BOT_TOKEN = "8763977900:AAEYu-yWlR7Oo5XHIpl8Z13hgLljv9z73_I"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        voice_path = "voice.ogg"
        with open(voice_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.reply_to(message, "گیانەکەم، گوێم لێبوو...")

        with open(voice_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt="ئەمە دەنگە بە زمانی کوردی سۆرانی."
            )
        user_text = transcript.text

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "تۆ یاریدەدەرێکی زیرەکی، بە کوردی سۆرانی زۆر شیرین و کورتی وەڵام بدەوە."},
                {"role": "user", "content": user_text}
            ]
        )
        ai_reply = response.choices[0].message.content

        bot.reply_to(message, ai_reply)

    except Exception as e:
        bot.reply_to(message, f"هەڵەیەک ڕوودا: {str(e)}")

print("بۆتەکە ئامادەیە...")
bot.infinity_polling()
