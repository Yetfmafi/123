import telebot
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Загрузка API токена
API_TOKEN = "7973051942:AAGoXJul4_G93tsVwOAsSi2CYYTZ9IYQ1CM"
bot = telebot.TeleBot(API_TOKEN)

# Список executors
executors = [
    {"name": "Xeno", "sUNC": "41%", "UNC": "81%", "level": 3, "hoho": "❌ Не поддерживает HoHo Hub"},
    {"name": "Solara", "sUNC": "51%", "UNC": "66%", "level": 3, "hoho": "❌ Не поддерживает HoHo Hub"},
    {"name": "Zorara", "sUNC": "41%", "UNC": "89%", "level": 3, "hoho": "❌ Не поддерживает HoHo Hub"},
    {"name": "JJSploit", "sUNC": "40%~", "UNC": "~", "level": 3, "hoho": "❌ Не поддерживает HoHo Hub"},
    {"name": "VegaX", "sUNC": "99%", "UNC": "UNC~", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Argon", "sUNC": "100%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Wave", "sUNC": "100%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Nihon", "sUNC": "100%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Cryptic", "sUNC": "100%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Seliware", "sUNC": "100%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "AWP.gg", "sUNC": "99%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Synapse Z", "sUNC": "~%", "UNC": "100%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Macsploit", "sUNC": "~%", "UNC": "98%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Swift", "sUNC": "93%", "UNC": "94%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
    {"name": "Trigon", "sUNC": "~%", "UNC": "~%", "level": 8, "hoho": "✅ Поддерживает HoHo Hub"},
]

# Загрузка скриптов из файла
SCRIPTS_FILE = "scripts.json"

def load_scripts():
    try:
        with open(SCRIPTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_scripts(scripts):
    with open(SCRIPTS_FILE, "w", encoding="utf-8") as file:
        json.dump(scripts, file, ensure_ascii=False, indent=4)

scripts = load_scripts()

# Главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("⚙️ Executors"), KeyboardButton("📜 Scripts"))
    return markup

# Меню "Executors"
def executors_menu():
    markup = InlineKeyboardMarkup()
    for idx, ex in enumerate(executors):
        markup.add(InlineKeyboardButton(ex["name"], callback_data=f"executor_{idx}"))
    return markup

# Меню "Scripts"
def scripts_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍 Поиск по хэштегам", callback_data="search_scripts"))
    for idx, script in enumerate(scripts):
        markup.add(InlineKeyboardButton(f"📜 {script['name']} - @{script['author']}", callback_data=f"script_{idx}"))
    markup.add(InlineKeyboardButton("➕ Добавить скрипт", callback_data="add_script"))
    return markup

# Старт
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать! Выберите категорию:",
        reply_markup=main_menu()
    )

# Показ Executors
@bot.message_handler(func=lambda message: message.text == "⚙️ Executors")
def show_executors(message):
    bot.send_message(
        message.chat.id,
        "⚙️ Список Executors:",
        reply_markup=executors_menu()
    )

# Выбор Executor
@bot.callback_query_handler(func=lambda call: call.data.startswith("executor_"))
def executor_details(call):
    idx = int(call.data.split("_")[1])
    ex = executors[idx]
    bot.send_message(
        call.message.chat.id,
        f"⚙️ **Executor:** {ex['name']}\n"
        f"🔸 sUNC: {ex['sUNC']}\n"
        f"🔹 UNC: {ex['UNC']}\n"
        f"📊 Level: {ex['level']}\n"
        f"{ex['hoho']}",
        parse_mode="Markdown"
    )

# Показ Scripts
@bot.message_handler(func=lambda message: message.text == "📜 Scripts")
def show_scripts(message):
    bot.send_message(
        message.chat.id,
        "📜 Список скриптов:",
        reply_markup=scripts_menu()
    )

# Добавление нового скрипта (шаг 1)
@bot.callback_query_handler(func=lambda call: call.data == "add_script")
def add_script_step1(call):
    bot.send_message(call.message.chat.id, "📝 Введите название скрипта:")
    bot.register_next_step_handler(call.message, add_script_step2)

# Шаг 2 - Описание
def add_script_step2(message):
    script_data = {"name": message.text, "author": message.from_user.username or "Аноним"}
    bot.send_message(message.chat.id, "📝 Введите описание скрипта:")
    bot.register_next_step_handler(message, add_script_step3, script_data)

# Шаг 3 - Хэштеги
def add_script_step3(message, script_data):
    script_data["description"] = message.text
    bot.send_message(message.chat.id, "🏷 Введите хэштеги (через запятую):")
    bot.register_next_step_handler(message, add_script_step4, script_data)

# Шаг 4 - Содержимое
# Шаг 4 - Содержимое
def add_script_step4(message, script_data):
    script_data["tags"] = [tag.strip() for tag in message.text.split(",") if tag.strip()]
    bot.send_message(message.chat.id, "💻 Вставьте содержимое скрипта:")
    bot.register_next_step_handler(message, add_script_finish, script_data)

# Завершение добавления (с проверкой уникальности)
def add_script_finish(message, script_data):
    # Добавляем содержимое скрипта в data
    script_data["content"] = message.text

    # Проверка уникальности содержимого
    if not is_unique_script_content(script_data["content"]):
        bot.send_message(
            message.chat.id,
            "❌ Этот скрипт уже существует, соблюдайте оригинальность!"
        )
        return  # Прерываем добавление скрипта, если содержимое не уникально

    scripts.append(script_data)
    save_scripts(scripts)
    bot.send_message(message.chat.id, "✅ Скрипт успешно добавлен!")


# Проверка на уникальность содержимого скрипта
def is_unique_script_content(content):
    for script in scripts:
        if script['content'] == content:
            return False  # Если найдено совпадение, возвращаем False
    return True  # Если совпадений нет, возвращаем True

# Поиск по хэштегам
@bot.callback_query_handler(func=lambda call: call.data == "search_scripts")
def search_scripts(call):
    bot.send_message(call.message.chat.id, "🔍 Введите хэштег для поиска:")
    bot.register_next_step_handler(call.message, perform_search)

def perform_search(message):
    tag = message.text.lower()
    found_scripts = [
        s for s in scripts if any(tag in t.lower() for t in s["tags"])
    ]
    if found_scripts:
        for idx, script in enumerate(found_scripts):
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "📜 Показать скрипт",
                    callback_data=f"show_script_{scripts.index(script)}"
                )
            )
            bot.send_message(
                message.chat.id,
                f"🔖 **{script['name']}**\n"
                f"✍️ Автор: @{script['author']}\n"
                f"🏷 Хэштеги: {', '.join(script['tags'])}",
                parse_mode="Markdown",
                reply_markup=markup
            )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Скрипты с таким хэштегом не найдены."
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("show_script_"))
def show_script_content_found(call):
    # Получаем индекс скрипта из callback_data
    idx = int(call.data.split("_")[-1])
    script = scripts[idx]
    bot.send_message(
        call.message.chat.id,
        f"📜 **Скрипт:** {script['name']}\n"
        f"✍️ Автор: @{script['author']}\n"
        f"🏷 Хэштеги: {', '.join(script['tags'])}\n\n"
        f"💻 Содержимое скрипта:\n```{script['content']}```",  # Используем тройные обратные кавычки для моноширного текста
        parse_mode="Markdown"
    )

# Показ скрипта при его выборе из меню
@bot.callback_query_handler(func=lambda call: call.data.startswith("script_"))
def show_script_content_list(call):
    idx = int(call.data.split("_")[1])  # Извлекаем индекс скрипта
    script = scripts[idx]  # Получаем скрипт по индексу
    bot.send_message(
        call.message.chat.id,
        f"📜 **Скрипт:** {script['name']}\n"
        f"✍️ Автор: @{script['author']}\n"
        f"🏷 Хэштеги: {', '.join(script['tags'])}\n\n"
        f"💻 Содержимое скрипта:\n```{script['content']}```",  # используем кодовое оформление для содержания
        parse_mode="Markdown"
    )

# Запуск бота
bot.polling()
