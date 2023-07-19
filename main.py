import telebot
import re
import os

TOKEN = os.environ['token clean']
print('Бот запущен!')

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# ID администраторов для обхода бота
admin_ids = [878116536, 987654321]

blacklist = [
  "легально", "22", "требуются", "арбитражная", "cвязка", "гаранта", "гарант",
  "бирж", "биржа", "профит", "подработка", "вложений", "вложения"
]

# ID чата, в котором бот должен работать
allowed_chat_id = -1001577799075
# ид админа которому всё идёт
forward_chat_id = 878116536


@bot.message_handler(commands=['start'])
def handle_start_command(message):
  if message.chat.type == 'private':
    if message.from_user.id in admin_ids:
      bot.send_message(message.chat.id, "Бот работает!")
    else:
      bot.send_message(message.chat.id, "Съебал в страхе, это не для тебя")


@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
  if message.chat.id == allowed_chat_id:
    handle_blacklist(message)
    handle_links(message)


def handle_blacklist(message):
  if message.text is not None:
    for word in blacklist:
      if word in message.text.lower():
        if message.from_user.id not in admin_ids:
          chat_id = message.chat.id
          user_id = message.from_user.id
          bot.restrict_chat_member(chat_id,
                                   user_id,
                                   can_send_messages=False,
                                   can_send_media_messages=False,
                                   can_send_other_messages=False,
                                   can_add_web_page_previews=False)
          bot.delete_message(chat_id, message.message_id)
          username = message.from_user.username
          muted_message = f"@{username} был замучен. Администратор сообщён"
          bot.send_message(allowed_chat_id, muted_message)
          forwarded_message = f"@{username} отправил: {message.text}"
          bot.send_message(forward_chat_id, forwarded_message)
        break


def handle_links(message):
  if message.text is not None:
    # Поиск ссылок в тексте сообщения
    links = re.findall(
      r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
      message.text)

    if len(links) > 0:
      if message.from_user.id not in admin_ids:
        chat_id = message.chat.id
        user_id = message.from_user.id
        bot.restrict_chat_member(chat_id,
                                 user_id,
                                 can_send_messages=False,
                                 can_send_media_messages=False,
                                 can_send_other_messages=False,
                                 can_add_web_page_previews=False)
        bot.delete_message(chat_id, message.message_id)
        username = message.from_user.username
        muted_message = f"@{username} был замучен. Администратор сообщён"
        bot.send_message(allowed_chat_id, muted_message)
        forwarded_message = f"@{username} отправил ссылку: {' '.join(links)}"
        bot.send_message(forward_chat_id, forwarded_message)


# Запуск бота
bot.polling()
